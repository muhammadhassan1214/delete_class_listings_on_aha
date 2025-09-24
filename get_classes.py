import requests
import json

def get_classes(page_number: int):
    url = f"https://atlas-api-gateway.heart.org/classManagement/v2/getClasses?size=100&page={page_number}&sort=startDateTime,desc"
    payload = json.dumps({
        "classFilters": {
            "parentId": 18260,
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
            "timeZone": "America/Chicago"
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
        'x-jwt-token': 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIyIiwic3ViIjoiQW1lcmljYW4gaGVhcnQgYXNzb2NpYXRpb24iLCJ1c2VyX2lkIjoiNyIsImZuIjoiQXRsYXMiLCJlbWFpbCI6ImF0bGFzX2FkbWluQG1haWwuY29tIiwibG4iOiJBZG1pbiIsInVzZXJfcm9sZXMiOiJbMiwgMTFdIiwidHlwZSI6ImxlYXJuZXIiLCJhZG1pbiI6ZmFsc2UsInNzb0lkIjoiZGFjYmY2NzgtZjBjZC00ZjQzLWFhZjAtN2NkNTA1OGZiOWY5Iiwicm9sZV9uYW1lcyI6IltwdWJsaWMsIGF0bGFzX2FkbWluXSIsImFwcElkIjoiQUhBLUF0bGFzIiwiY3QiOjIzODkxMjkzMjE4MTM2MzksImlhdCI6MTc1ODc0NTM3NSwiZXhwIjoxNzU4ODMxNzc1fQ.eCUO1dGl2Zo6ZtYeOmN9Ju5SB4LMqoIqd9-2NdrLhZk'
    }
    response = requests.post(url, headers=headers, data=payload)
    json_response = response.json()
    items = json_response['data']['items']
    return items

# Example usage:
# items = get_classes(1)
# print(items)
