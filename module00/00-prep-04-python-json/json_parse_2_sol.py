var={"donut":{"flavors":["chocolate","jelley","maple","plain"]}}
print(var["donut"]["flavors"][0])
print("My favorite donut flavors are:", end=" ")
for f in var["donut"]["flavors"]:
	print(f, end=" ")
print()
print()

var1={"type":"donut","flavors":{"flavor":[{"type":"chocolate","id":1001}, {"type":"glazed","id":1002},{"type":"sprinkled","id":1003}]}}
print("Id: " + str(var1["flavors"]["flavor"][0]["id"]) + " type: " + var1["flavors"]["flavor"][0]["type"])
for f in var1["flavors"]["flavor"]:
	print("Id: " + str(f["id"]) + " type: " + f["type"])
print()
print()
	
#Using the examples above write code to print one value of each JSON structure and a loop to print all values.	
myvar={"exercise":{"high impact":["running","jumping","jump rope","running down stairs","skiing"]}}
print(myvar["exercise"]["high impact"][0])
print("My favorite high impact exercises are:", end=" ")
for f in myvar["exercise"]["high impact"]:
	print(f, end=" ")
print()
print()

myvar={"foods":{"healthy":["yogurt","nuts","vegetables","fruits","beans"]}}
print(myvar["foods"]["healthy"][0])
print("My favorite healthy foods are:", end=" ")
for f in myvar["foods"]["healthy"]:
	print(f, end=" ")
print()
print()
	
myvar1={"author":"Stephen King","famous works":{"novels":[{"title":"The Shining","id":1001}, {"title":"Carrie","id":1002},{"title":"It","id":1003},{"title":"Misery","id":1004},{"title":"Night Shift","id":1005}]}}
print("id: " + str(myvar1["famous works"]["novels"][0]["id"]) + " novel: " + myvar1["famous works"]["novels"][0]["title"])
for f in myvar1["famous works"]["novels"]:
	print("Id: " + str(f["id"]) + " novel: " + f["title"])
print()
print()


myvar1={"type":"car","cars":{"sports":[{"make":"Chevrolet", "model":"Corvette", "id":1001},{"make":"Chevrolet", "model":"Camaro", "id":1002},{"make":"Ford", "model":"Mustang", "id":1003},{"make":"Dodge", "model":"Viper", "id":1004},{"make":"Porsche", "model":"911", "id":1005}]}}
print("id: " + str(myvar1["cars"]["sports"][0]["id"]) + " make: " + myvar1["cars"]["sports"][0]["make"] + " model: " + myvar1["cars"]["sports"][0]["model"])
for f in myvar1["cars"]["sports"]:
	print("id: " + str(f["id"]) + " make: " + f["make"] + " model: " + f["model"])

