class Expense:

    owner=input("Enter your name:")
    Balance=float(input("Enter your balance:"))
    date=input("Enter the date:")

    def __init__(self,spend_amount,category):
        
        self.spend_amount=spend_amount
        
        self.category=category

    def show_detail(self):
        return (f"{self.spend_amount} in {self.category} category.")

    @classmethod
    def remaining_balance(cls,spend_amount):
        cls.Balance-=spend_amount

    def get_balance(self):
        return self.Balance


#_________main___________

item_list=[]

while True:
    
    category=input("Enter the category:")
    spend_amount=float(input("Enter the amount spent:"))
    aa=Expense(spend_amount,category)
    item_list.append(aa.show_detail())
    Expense.remaining_balance(spend_amount)
    if input("Do you want to add an expense? (yes->1/no->0)")!= "1":
        break

print("-"*50)
print((f"{Expense.owner} spent on {Expense.date} in:"))
print("-"*50)
for number,i in enumerate(item_list,start=1):  # enumerate() function add a serial number to the list and start from 1 (if we not use start=1 than it will start from 0)
    print(f"{number}. {i}")
if Expense.Balance<0:
    print("warning! You have exceeded your balance.")
print(f"Thank you! Your remaining balance is: {aa.get_balance()}")