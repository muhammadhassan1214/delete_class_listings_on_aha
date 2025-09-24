import requests
import json
from payload import (
    acc_1_deletion_token,
    acc_2_deletion_token
)


def cancel_class(acc: str, class_id: int) -> int:
    url = f"https://atlas-api-gateway.heart.org/classManagement/v1/classes/{class_id}"
    payload = json.dumps({
        "class": {
            "isCancelled": True
        }
    })
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'contenttype': 'application/json',
        'ext_id': 'dacbf678-f0cd-4f43-aaf0-7cd5058fb9f9',
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
        'x-jwt-token': acc_1_deletion_token if acc == 'acc_1' else acc_2_deletion_token
    }
    response = requests.patch(url, headers=headers, data=payload)
    return response.status_code
