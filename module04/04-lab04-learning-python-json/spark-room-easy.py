import json
import requests

accessToken = "MGU0OWNkNzAtNjg2OC00NjAxLWI5MWYtMjcyYzJjMGIzZDMyNjBmZjFiOWYtMDE1" #put your access token here between the quotes.


accessToken_hdr = 'Bearer ' + accessToken
spark_header = {'Authorization': accessToken_hdr}
uri = 'https://api.ciscospark.com/v1/rooms'
resp = requests.get(uri, headers=spark_header)
print("Spark Rooms you belong to: ")	
print(resp.text)

print()
print("Spark Rooms in easier to read format - pretty format:")
print (json.dumps(resp.json(), indent=4, separators=(',', ': ')))

