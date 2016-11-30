food={"vegetables":["carrots","kale","cucumber","tomato"],"desserts":["cake","ice cream", "donut"]}
for hungry in food["vegetables"]:
	print(hungry)
for hungry in food["desserts"]:
	print(hungry)

cars={"sports":{"Volkswagon":"Porsche","Dodge":"Viper","Chevy":"Corvette"},"classic":{"Mercedes-Benz":"300SL","Toyota":"2000GT","Lincoln":"Continental"}}
for auto in cars["sports"]:
	print(cars["sports"][auto])
for auto in cars["classic"]:
	print(cars["classic"][auto])

dessert={"iceCream":["Rocky Road","strawberry","Pistachio Cashew","Pecan Praline"]}
for yummy in dessert["iceCream"]:
	print(yummy)

soup={"soup":{"tomato 1":"healthy","onion":"bleh!","vegetable":"good for you"}}
for tastey in soup["soup"]:
	print(soup["soup"][tastey])
