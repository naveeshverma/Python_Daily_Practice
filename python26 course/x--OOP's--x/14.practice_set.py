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