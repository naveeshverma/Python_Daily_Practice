def modifier(func):
    def inner(self):   # yaha self hai kyoki origin me self pass ho raha hai
        print("hello this message is before the original message")
        func(self)  # ye mannually krna pdta hai
        print("meaasge after original")
    return inner

class Student:
    def __init__(self,name):
        self.name=name
    @modifier   # remove if call mannually
    def origin(self):
        print(f" Hi I am {self.name}")

# call with using keyword @modifier
ss=Student("Nav")
# ss.my_func=modifier(ss.origin) only add this for mannul work
ss.origin()  # here origin change to my_func (we can use origin but u need to use origin in upper line )  i am using my_func or other to reduse confusion
