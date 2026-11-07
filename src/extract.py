import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CH_API_KEY")

if API_KEY is None:
    raise ValueError("No API Key")

BASE_URL = "https://api.company-information.service.gov.uk"
advanced = f"{BASE_URL}/advanced-search/companies"

sic_codes = ["82990", "96090", "64209"]
    
company_numbers = set()
for code in sic_codes:
    start_index = 0
    page = 1
    while True:
        response = requests.get(advanced, 
                                        auth=(API_KEY, ""), 
                                        params={"incorporated_from": "2025-01-01", "incorporated_to":"2025-01-14", "sic_codes": code, "size": 200, "start_index":start_index},
                                        timeout=10)
                
        if response.status_code != 200:
            print(response.text)
            raise ValueError
                
        data = response.json()

        os.makedirs("data/bronze/search", exist_ok=True)
        with open(f"data/bronze/search/{code}_page_{page}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        items = data.get("items", [])
        
        for item in items:
            company_numbers.add(item["company_number"])
            
        start_index += len(items)
        page +=1 
        
        if items == [] or start_index >= data["hits"]:
            break
        
with open("data/company_numbers.json", "w", encoding="utf-8") as f:
    json.dump(sorted(company_numbers), f, indent=2)

print(len(company_numbers))
