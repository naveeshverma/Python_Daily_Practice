def decorator(func):
    num1=int(input("Enter the first number: "))
    def wrapper(num2,num3):
        x=num1+func(num2,num3)
        print(f"the addition of {num1} and {num2} and {num3} is {x}")
    return wrapper

@decorator
def addition(num2,num3):
    return num2+num3

num2=int(input("Enter the 2nd number: "))
num3=int(input("Enter the 3rd number: "))
addition(num2,num3)
