n=int(input("Enter a number to check weird or not: "))
if n%2!=0:
    print("Weird")
elif n%2==0:
    if 2<=n<=5:
        print("Not Weird")
    elif 6<=n<=20:
        print("Weird")
    elif n>20:
        print("Not Weird")
    