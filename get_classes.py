import requests
import json
from payload import *

def fetch_details(acc: str):
    if acc == 'acc_1':
        return acc_1_parent_id, acc_1_time_zone, acc_1_ext_id, acc_1_token
    elif acc == 'acc_2':
        return acc_2_parent_id, acc_2_time_zone, acc_2_ext_id, acc_2_token
    else:
        raise ValueError("Invalid account identifier. Use 'acc_1' or 'acc_2'.")


def get_classes(acc: str, page_number: int):
    parent_id, time_zone, ext_id, token = fetch_details(acc)
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
    json_response = response.json()
    items = json_response['data']['items']
    return items
