import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CH_API_KEY")

if API_KEY is None:
    raise ValueError("No API Key")

company_number = "00048839"

BASE_URL = "https://api.company-information.service.gov.uk"
company_url = f"{BASE_URL}/company/{company_number}"

response = requests.get(url=company_url, auth=(API_KEY, ""), timeout=10)

if response.status_code != 200:
    print(response.text)
    raise ValueError

data = response.json()

print("Company Name:", data.get("company_name"))
print("Company Status:", data.get("company_status"))
print("Company Incorporation Date:", data.get("date_of_creation"))
print("Company SIC codes:", data.get("sic_codes"))
print("Company Office Address:", data.get("registered_office_address", {}).get("postal_code"))



