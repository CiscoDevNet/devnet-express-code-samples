import requests

url = "https://198.18.129.100/api/v1/host"

payload = "{\"username\":\"admin\",\n\"password\":\"C1sco12345\"}"
headers = {
    'content-type': "application/json",
    'x-auth-token': "ST-3-fObuCpRxPybwBbKh3RZe-cas",
    'cache-control': "no-cache",
    'postman-token': "1ac85e7f-924d-bde7-f2fd-f7ca48154f83"
    }

response = requests.request("GET", url, data=payload, headers=headers, verify=False)

print(response.text)