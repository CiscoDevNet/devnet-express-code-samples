print ("I'm not a function")

def my_function():
	print("Hey I'm a function!")
        

def brett(val):
	for i in range(val):
		print("I'm a function with args!")
    
def new_func(data):
	data2= "my data is " + str(data)
	return (data2)

def calc(num,num2):
	var=num * num2
	print(var)
    
my_function()
brett(5)
my_data=new_func("happy")
print(my_data)
calc(5,10)

