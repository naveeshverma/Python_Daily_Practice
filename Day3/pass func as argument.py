def greet():
    msg="Hello guys, This is Naveesh"
    print(msg)

def call(xyz):
    xyz()

call(greet) # here greet function is passed as an argument to the call function and then it is called inside the call function.