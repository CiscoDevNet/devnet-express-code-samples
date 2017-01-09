var={"car":"volvo", "fruit":"apple"}
print(var["fruit"])
for f in var:	
	print("key: " + f + " value: " + var[f])
print()
print()

var1={"donut":["chocolate","glazed","sprinkled"]}
print(var1["donut"][0])
print("My favorite donut flavors are:", end= " ")
for f in var1["donut"]:
	print(f, end=" ")
print()
print()

#Using the examples above write code to print one value of each JSON structure and a loop to print all values below.	
var={"vegetable":"carrot", "fruit":"apple","animal":"cat","day":"Friday"}
print(var["vegetable"])
for f in var:	
	print("key: " + f + " value: " + var[f])
print()
print()

var1={"animal":["dog","cat","fish","tiger","camel"]}
print(var1["animal"][0])
print("My favorite animals are:", end= " ")
for f in var1["animal"]:
	print(f, end=" ")
print()
print()

myvar={"dessert":"ice cream", "exercise":"push ups","eyes":"blue","gender":"male"}
print(myvar["exercise"])
for f in myvar:	
	print("key: " + f + " value: " + myvar[f])
print()
print()	

myvar1={"dessert":["cake","candy","ice cream","pudding","cookies"]}
print(myvar1["dessert"][0])
print("My favorite desserts are:", end= " ")
for f in myvar1["dessert"]:
	print(f, end=" ")
