class A:
    school_name="xyz"
    def __init__(self,n1):
        self.n1=n1

    def add(self,other):
        return self.n1+other.n1

# main
num1=int(input("Enter num1 value : "))
num2=int(input("Enter num2 value : "))
aa=A(num1)
bb=A(num2)

print(aa.add(bb))

#-------------------------------------

class addition1:
    num1=int(input("Enter the 1st number:"))
    num2=int(input("Enter the 2nd number:"))
    def add(self):
        return self.num1+self.num2
    
#---------main-----------------
aa=addition1()

result=aa.add()
print(f"The sum of two numbers is : {result}")
print(f"num1 value is : {aa.num1}")  