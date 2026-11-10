def decorator(func):
    def inner(name):
        print("msg before the original message")
        func(name)
        print("msg after the original message")
    return inner

def original(name):
    print(f"Hello {name}, This is Naveesh")

myfunc=decorator(original) 
myfunc("Elder Brother")