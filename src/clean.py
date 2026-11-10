import os
import pandas as pd
import json
from pathlib import Path


##### companies
def build_companies_df(companies_folder, psc_folder):
    
    rows = []
    for company in companies_folder:
        
        psc = psc_folder / f"{company.stem}.json"

        with open(company, "r", encoding="utf-8") as f, open(psc, "r", encoding="utf-8") as g:
            profile = json.load(f)
            psc_ = json.load(g)

            row = {
                "company_number": company.stem,
                "company_name": profile.get("company_name"),
                "company_status": profile.get("company_status"),
                "company_status_detail": profile.get("company_status_detail"),
                "ro_address_line_1": profile.get("registered_office_address", {}).get("address_line_1"),
                "ro_postal_code": profile.get("registered_office_address", {}).get("postal_code"),
                "ro_city": profile.get("registered_office_address", {}).get("locality"),
                "incorporation_date": pd.to_datetime(profile.get("date_of_creation")),
                "company_type": profile.get("type"),
                "psc_register_found": psc_.get("_status") != 404,
                "psc_active_count": psc_.get("active_count", 0),
                "accounts_overdue": profile.get("accounts", {}).get("overdue", False),
                "confirmation_statement_overdue": profile.get("confirmation_statement", {}).get("overdue", False),
                "has_charges": profile.get("has_charges"),
                "has_insolvency_history": profile.get("has_insolvency_history"),
                "date_of_cessation": pd.to_datetime(profile.get("date_of_cessation")),
                "jurisdiction": profile.get("jurisdiction"),
                "sic_codes": ",".join(profile.get("sic_codes", []))
        }
            rows.append(row)
            
    companies_df = pd.DataFrame(rows)
    return companies_df

######## officer
def build_officers_df(officer_folder):
    
    rows = []
    for officer in officer_folder:
        with open(officer, "r", encoding="utf-8") as f:
                officer_ = json.load(f)

        for item in officer_.get("items", []):
                row = {
                            "officer_id": item.get("links", {}).get("officer", {}).get("appointments").split("/")[2],
                            "company_number": officer.stem,
                            "officer_name": item.get("name"),
                            "officer_dob_month": item.get("date_of_birth", {}).get("month"),
                            "officer_dob_year": item.get("date_of_birth", {}).get("year"),
                            "officer_nationality": item.get("nationality"),
                            "officer_role": item.get("officer_role"),
                            "officer_postal_code": item.get("address", {}).get("postal_code"),
                            "officer_locality": item.get("address", {}).get("locality"),
                            "appointed_on": item.get("appointed_on"),
                            "resigned_on": item.get("resigned_on"),
                            
                        }
                rows.append(row)

    officers_df = pd.DataFrame(rows)
    officers_df["officer_dob_month"] = officers_df["officer_dob_month"].astype("Int64")
    officers_df["officer_dob_year"] = officers_df["officer_dob_year"].astype("Int64")
    officers_df["appointed_on"] = pd.to_datetime(officers_df["appointed_on"])
    officers_df["resigned_on"] = pd.to_datetime(officers_df["resigned_on"])
    
    return officers_df

######## psc

def build_psc_df(psc_folder):
    rows = []
    for psc in psc_folder:
        with open(psc, "r", encoding="utf-8") as f:
            psc_ = json.load(f)

        for item in psc_.get("items", []):
            row = {
                    "psc_id": item.get("links", {}).get("self", "").split("/")[-1],
                    "company_number": psc.stem,
                    "psc_postal_code": item.get("address", {}).get("postal_code"),
                    "psc_name": item.get("name"),
                    "kind": item.get("kind", ""),
                    "natures_of_control": ",".join(item.get("natures_of_control", [])),
                    "ceased": item.get("ceased"),
                    "notified_on": item.get("notified_on"),
                    "ceased_on": item.get("ceased_on")
            }
            rows.append(row)

    psc_df = pd.DataFrame(rows)
    
    psc_df["kind"] = psc_df["kind"].str.replace("-person-with-significant-control", "")
    psc_df["notified_on"] = pd.to_datetime(psc_df["notified_on"])
    psc_df["ceased_on"] = pd.to_datetime(psc_df["ceased_on"])

    return psc_df

def dataframe_validation(df, df_name):
    if df_name == "Companies":
        print(df["company_status"].value_counts())
        print(df["psc_register_found"].value_counts())
        print(f"Unique {df_name}:", df["company_number"].nunique())
        print(f"Number of duplicated {df_name}:", df.duplicated(subset=["company_number"]).sum())
        df.info()

    if df_name == "Officers":
        key = ["company_number", "officer_id", "officer_role"]
        print(df["officer_role"].value_counts())
        print(f"Unique {df_name}:", df["officer_id"].nunique())
        print(f"Number of duplicated {df_name} :", df.duplicated(subset=["company_number", "officer_id", "officer_role", "appointed_on"]).sum())
        print(df[df.duplicated(subset=key, keep=False)].sort_values(key))
        df.info()

    if df_name == "PSC":
        print(df["kind"].value_counts())
        print(f"Unique {df_name}:", df["company_number"].nunique())
        print(f"Number of duplicated {df_name} :", df.duplicated(subset=["company_number", "psc_id"]).sum())
        df.info()

def load_silver_files(df, csv_filename):
     os.makedirs("data/silver", exist_ok=True)
     df.to_csv(f"data/silver/{csv_filename}.csv", index=False)
     

if __name__ == "__main__":
    profile_files = Path("data/bronze/profiles/").glob("*.json")
    officer_files = Path("data/bronze/officers/").glob("*.json")
    psc_files = Path("data/bronze/psc/").glob("*.json")
    psc_dir = Path("data/bronze/psc/")

    companies_df = build_companies_df(profile_files, psc_dir)
    officers_df = build_officers_df(officer_files)
    psc_df = build_psc_df(psc_files)
    
    dataframe_validation(companies_df, "Companies")
    dataframe_validation(officers_df, "Officers")
    dataframe_validation(psc_df, "PSC")

    dfs = [(companies_df, "companies"), (officers_df, "officers"), (psc_df, "psc")]

    for df in dfs:
         load_silver_files(df[0], df[1])

