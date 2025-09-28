import requests
import json
from utils.payload import accounts

def fetch_details(acc: str):
    if acc not in accounts:
        raise ValueError("Invalid account identifier. Use 'acc_1' or 'acc_2'.")
    acc_data = accounts[acc]
    return acc_data['parent_id'], acc_data['time_zone'], acc_data['ext_id']


def get_classes(acc: str, page_number: int, token: str):
    parent_id, time_zone, ext_id = fetch_details(acc)
    url = f"https://atlas-api-gateway.heart.org/classManagement/v2/getClasses?size=100&page={page_number}&sort=startDateTime,desc"
    payload = json.dumps({
        "classFilters": {
            "parentId": parent_id,
            "courseId": None,
            "disciplineCodes": None,
            "seatAvailability": None,
            "langCode": None,
            "location": None,
            "classStatus": None,
            "isPrivate": None,
            "pageNumber": 0,
            "selectedSort": "startDateTime",
            "sortOrder": "desc",
            "applyFilter": False,
            "instructorIds": [],
            "timeZone": time_zone
        }
    })
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'contenttype': 'application/json',
        'ext_id': ext_id,
        'origin': 'https://atlas.heart.org',
        'priority': 'u=1, i',
        'referer': 'https://atlas.heart.org/',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'x-jwt-token': token
    }
    response = requests.post(url, headers=headers, data=payload)
    try:
        json_response = response.json()
    except Exception as e:
        print(f"Error parsing JSON response for page {page_number}: {e}\nRaw response: {response.text}")
        return []
    if not isinstance(json_response, dict) or 'data' not in json_response or 'items' not in json_response['data']:
        print(f"Unexpected response structure for page {page_number}: {json_response}")
        return []
    items = json_response['data']['items']
    is_last_page = json_response['data']['pagination']['isLast']
    return items, is_last_page
