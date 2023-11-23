import requests

HOST_URL = 'https://oc.ag1.pro'

input = {
    "year": 2023,
    "month": 11,
    "day": 22,
    "hour": 20,
    "min": 18,
    "sec": 5
}

response = requests.post(f'{HOST_URL}/bazi', json=input)

data = response.json()
print(data)


# print(get_bazi_from_api(2023,11,22,20))