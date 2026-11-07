import requests
import os
from dotenv import load_dotenv

load_dotenv()

def extract_company_data(api_key, url):
    sic_codes = ["82990", "96090", "64209"]
    
    numbers = {}
    for code in sic_codes:
        start_index = 0
        page = 1
        
        while True:
            response = requests.get(url=url, 
                                    auth=(api_key, ""), 
                                    params={"incorporated_from": "2025-01-01", "incorporated_to":"2025-01-14", "sic_codes": code, "size": 200},
                                    timeout=10)
            
            if response.status_code != 200:
                print(response.text)
                raise ValueError
            
            data = response.json()

    return data[0]

if __name__=="__main__":

    API_KEY = os.getenv("CH_API_KEY")
    
    if API_KEY is None:
        raise ValueError("No API Key")

    BASE_URL = "https://api.company-information.service.gov.uk"
    advanced = f"{BASE_URL}/advanced-search/companies"
    
    
    
    
    
