import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CH_API_KEY")
if API_KEY is None:

    raise ValueError("No API Key")


BASE_URL = "https://api.company-information.service.gov.uk"
advanced = f"{BASE_URL}/advanced-search/companies"

sic_codes = ["82990", "96090", "64209"]

for code in sic_codes:
    response = requests.get(url=advanced, 
                            auth=(API_KEY, ""), 
                            params={"incorporated_from": "2025-01-01", "incorporated_to":"2025-01-14", "sic_codes": code, "size": 1},
                            timeout=10)
    
    if response.status_code != 200:
        print(response.text)
        raise ValueError
    
    data = response.json()
    print(f"Num of hits for sic code(s) - {code}:", data["hits"])


