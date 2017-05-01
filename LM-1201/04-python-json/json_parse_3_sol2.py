food={"vegetables":["carrots","kale","cucumber","tomato"]}
for veg in food["vegetables"]:
	print(veg)

cars={"sports":{"Porsche":"Volkswagon","Viper":"Dodge","Corvette":"Chevy"}}
for auto in cars["sports"]:
	print(auto, cars["sports"][auto])

dessert={"iceCream":["Rocky-Road","strawberry","Pistachio-Cashew","Pecan-Praline"]}
for yummy in dessert["iceCream"]:
	print(yummy)

soup={"soup":{"tomato":"healthy","onion":"bleh!","vegetable":"goodForYou"}}
for s in soup["soup"]:
	print(s, soup["soup"][s])

ticket={"response": {"serviceTicket": "ST-16891-ugqKRVvCfPJcEaGXnGEN-cas","idleTimeout": 1800,"sessionTimeout": 21600},"version": "1.0"}
for auth in ticket["response"]:
	print(auth, ticket["response"][auth])
        
network={"Network":{"router":{"ipaddress":"192.168.1.21","mac_address":"08:56:27:6f:2b:9c"}}}
for net in network["Network"]["router"]:
	print(net,network["Network"]["router"][net])


hosts={"response": [{"id": "4c60d6a7-4812-40d6-a337-773af2625e56","hostIp": "65.1.1.86","hostMac": "00:24:d7:43:59:d8","hostType": "wireless"},{"id": "3ef5a7c3-7f74-4e57-a5cb-1448fbda5078","hostIp": "207.1.10.20","hostMac": "5c:f9:dd:52:07:78","hostType": "wired"},{"id": "12f9c920-24fa-4d32-bf39-4c63813aecd8","hostIp": "212.1.10.20","hostMac": "e8:9a:8f:7a:22:99","hostType": "wired"}],"version": "1.0"}

#Partial looping solution: iterates through response data returning each value.  Note that the version key is skipped, so must hard code.
for host in hosts["response"]:
	for val in host:			
		print(val,host[val])	
print("version", hosts["version"])

#Full looping solution: iterates through all data returning each value
for key in hosts:
	if isinstance(hosts[key],list):		
		for host in hosts[key]:
			for val in host:		
				print(val,host[val])
	else:
		print(key,hosts[key])



devices={"response": [
    {
      "family": "Switches and Hubs",
      "type": "Cisco Catalyst 2960C-8PC-L Switch",
      "serialNumber": "FOC1637Y3FJ",
      "role": "CORE",
      "reachabilityStatus": "Reachable",    
      "instanceUuid": "2dc30cac-072e-4d67-9720-cc302d02695a",
      "id": "2dc30cac-072e-4d67-9720-cc302d02695a"
    },
    {
      "family": "Unified AP",
      "type": "Cisco 3500I Unified Access Point",
      "serialNumber": "FGL1548S2YF",
      "role": "ACCESS",
      "reachabilityStatus": "Reachable",
      "instanceUuid": "17184480-2617-42c3-b267-4fade5f794a9",
      "id": "17184480-2617-42c3-b267-4fade5f794a9"
    }
  ],
  "version": "1.0"
}
#Partial looping solution: iterates through response data returning each value.  Note that version key is skipped, so must hard code.
for dev in devices["response"]:
	for val in dev:			
		print(val,dev[val])	
print("version", devices["version"])

#Full looping solution: iterates through all data returning each value
for key in devices:
	if isinstance(devices[key],list):		
		for dev in devices[key]:
			for val in dev:		
				print(val,dev[val])
	else:
		print(key,devices[key])

