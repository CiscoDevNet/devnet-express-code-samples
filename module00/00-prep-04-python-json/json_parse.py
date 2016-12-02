myvar1={"type":"donut","flavors":{"flavor":[{"type":"chocolate","id":1001}, {"type":"glazed","id":1002},{"type":"sprinkled","id":1003}]}}
print("Id: " + str(myvar1["flavors"]["flavor"][0]["id"]) + " type: " + myvar1["flavors"]["flavor"][0]["type"])
for f in myvar1["flavors"]["flavor"]:
	print("Id is: " + str(f["id"]) + " type is: " + f["type"])
