# The closer is the function(inner function) that is defined inside the outer function , it works is remenber the variables of the outer functio even after the outer function executing or destroyed.

def outer():
    name="The one and only Legend himself Naveesh"
    def inner():
        print(name)
    return inner 

# main

myfunc=outer() # outer func is executed and the inner function is returned to the variable myfunc
myfunc() # here inner function is called and print the value of variable name which present in the outer function.
