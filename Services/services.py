import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# 🔹 Load .env properly
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("WARNING: API_KEY missing, app will run with fallback data")

'''def get_prices_data(crop=None, state=None, district=None):
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 1000
    }

    # API Filters
    if state:
        params["filters[state.keyword]"] = state

    if district:
        params["filters[district.keyword]"] = district

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        result = []

        for item in data.get("records", []):
            crop_name = item.get("commodity", "")
            state_name = item.get("state", "")
            district_name = item.get("district", "")
            market = item.get("market", "")
            price = item.get("modal_price", "")

            # Crop filter (local filter)
            if crop and crop.lower() not in crop_name.lower():
                continue

            result.append({
                "crop": crop_name,
                "state": state_name,
                "district": district_name,
                "market": market,
                "price": price
            })

        return result

    except Exception as e:
        print("ERROR:", e)
        return [] '''

def get_prices_data(crop=None, state=None, district=None):
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 1000,

        # 🔥 FORCE MAHARASHTRA FROM API
        "filters[state]": "Maharashtra"
    }

    # Optional district filter
    if district:
        params["filters[district]"] = district

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        result = []

        for item in data.get("records", []):
            crop_name = item.get("commodity", "")
            state_name = item.get("state", "")
            district_name = item.get("district", "")
            market = item.get("market", "")
            price = item.get("modal_price", "")

            # 🔍 Crop filter
            if crop and crop.lower() not in crop_name.lower():
                continue

            # 🔥 DOUBLE SAFETY CHECK (IMPORTANT)
            if state_name.strip() != "Maharashtra":
                continue

            result.append({
                "crop": crop_name,
                "state": state_name,
                "district": district_name,
                "market": market,
                "price": price
            })

        # 🔥 FALLBACK (if API still fails)
        if not result:
            return [
                {"crop": "Onion", "state": "Maharashtra", "district": "Pune", "market": "Pune", "price": "1500"},
                {"crop": "Wheat", "state": "Maharashtra", "district": "Nashik", "market": "Nashik", "price": "2100"}
            ]

        return result

    except Exception as e:
        print("ERROR:", e)
        return [
            {"crop": "Onion", "state": "Maharashtra", "district": "Pune", "market": "Pune", "price": "1500"},
            {"crop": "Wheat", "state": "Maharashtra", "district": "Nashik", "market": "Nashik", "price": "2100"}
        ]  


'''def get_prices_data(crop: str = None, state: str = "Maharashtra", district: str = None):
    """
    Fetch all crop prices from Data.gov.in API for Maharashtra (or optional state) using pagination.
    Optional crop and district filters.
    Returns a list of dicts with: crop, state, district, market, price, last_updated
    Always returns latest available mandi data.
    """
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    all_records = []
    limit = 1000
    offset = 0

    try:
        while True:
            params = {
                "api-key": API_KEY,
                "format": "json",
                "limit": limit,
                "offset": offset,
                "filters[state.keyword]": state
            }
            if district:
                params["filters[district.keyword]"] = district

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            batch = response.json().get("records", [])

            if not batch:
                break  # no more records

            all_records.extend(batch)
            offset += limit

        result = []

        for item in all_records:
            crop_name = item.get("commodity", "").strip()
            state_name = item.get("state", "").strip()
            district_name = item.get("district", "").strip()
            market = item.get("market", "").strip()
            price = item.get("modal_price", "").strip()
            arrival_date = item.get("arrival_date", "").strip()

            # Crop filter
            if crop and crop.lower() not in crop_name.lower():
                continue

            # State safety check
            if state_name.lower() != state.lower():
                continue

            # Price conversion
            try:
                price = int(price)
            except:
                price = 0

            # Format arrival date
            try:
                last_updated = datetime.strptime(arrival_date, "%Y-%m-%dT%H:%M:%S").strftime("%d-%m-%Y")
            except:
                last_updated = arrival_date or "N/A"

            result.append({
                "crop": crop_name,
                "state": state_name,
                "district": district_name,
                "market": market,
                "price": price,
                "last_updated": last_updated
            })

        # Sort by last_updated descending → latest first
        result.sort(key=lambda x: datetime.strptime(x["last_updated"], "%d-%m-%Y") if x["last_updated"] != "N/A" else datetime.min, reverse=True)

        # 🔹 Fallback if API returns empty
        if not result:
            result = [
                {"crop": "Onion", "state": "Maharashtra", "district": "Pune", "market": "Pune", "price": 1500, "last_updated": "02-04-2026"},
                {"crop": "Wheat", "state": "Maharashtra", "district": "Nashik", "market": "Nashik", "price": 2100, "last_updated": "02-04-2026"}
            ]

        return result

    except Exception as e:
        print("ERROR fetching prices:", e)
        # Return fallback if API fails completely
        return [
            {"crop": "Onion", "state": "Maharashtra", "district": "Pune", "market": "Pune", "price": 1500, "last_updated": "02-04-2026"},
            {"crop": "Wheat", "state": "Maharashtra", "district": "Nashik", "market": "Nashik", "price": 2100, "last_updated": "02-04-2026"}
        ] '''
