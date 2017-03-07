import requests

url = "https://198.18.129.100/api/v1/host"

payload = "{\"username\":\"admin\",\n\"password\":\"C1sco12345\"}"
headers = {
    'content-type': "application/json",
    'x-auth-token': "ST-3-gfngyY6fkZ1uwVRGErEa-cas",
    'cache-control': "no-cache",
    'postman-token': "a8d5c214-5563-c79e-1da1-7ebe42f759c8"
    }

response = requests.request("GET", url, data=payload, headers=headers, verify=False)

print(response.text)