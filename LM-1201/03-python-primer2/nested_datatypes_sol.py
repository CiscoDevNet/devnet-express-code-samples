food={"vegetables":["carrots","kale","cucumber","tomato"],"desserts":["cake","ice cream", "donut"]}
strVeg = "My favorite vegetable is "
strDes = "My favorite dessert is "
print(strVeg + food["vegetables"][0])
print(strVeg + food["vegetables"][1])
print(strVeg + food["vegetables"][2])
print(strVeg + food["vegetables"][3])
print(strDes + food["desserts"][0])
print(strDes + food["desserts"][1])
print(strDes + food["desserts"][2])

cars={"sports":{"Volkswagon":"Porsche","Dodge":"Viper","Chevy":"Corvette"},"classic":{"Mercedes-Benz":"300SL","Toyota":"2000GT","Lincoln":"Continental"}}
strSport = "My favorite sports car is a"
strClassic = "My favorite classic car is a"
print(strSport + " Dodge " + cars["sports"]["Dodge"])
print(strSport + " Chevy " + cars["sports"]["Chevy"])
print(strSport + " Volkswagon " + cars["sports"]["Volkswagon"])
print(strClassic + " Mercedes-Benz " + cars["classic"]["Mercedes-Benz"])
print(strClassic + " Toyota " + cars["classic"]["Toyota"])
print(strClassic + " Lincoln " + cars["classic"]["Lincoln"])


dessert={"iceCream":["Rocky Road","strawberry","Pistachio Cashew","Pecan Praline"]}
strCream = "My favorite ice cream is "
print(strCream + dessert["iceCream"][0])
print(strCream + dessert["iceCream"][1])
print(strCream + dessert["iceCream"][2])
print(strCream + dessert["iceCream"][3])


soup={"soup":{"tomato":"healthy","onion":"bleh!","vegetable":"good for you"}}
print("This tomato soup is " + soup["soup"]["tomato"])
print("This onion soup is " + soup["soup"]["onion"])
print("This vegetable soup is " + soup["soup"]["vegetable"])
