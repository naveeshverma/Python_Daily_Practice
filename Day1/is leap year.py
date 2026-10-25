# These are the some rules to determine whether a year is a leap year or not.
"""
In the Gregorian calendar, three conditions are used to identify leap years:

The year can be evenly divided by 4, is a leap year, unless:
    The year can be evenly divided by 100 (jab tak year evenly 100 se divide na ho tab tk leap year h), it is NOT a leap year, unless:
        The year is also evenly divisible by 400. Then it is a leap year
"""

def is_leap(year):

    if year%4==0:
        if year%100==0:
            if year%400==0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

input_year = int(input("Enter a year to check if it is a leap year or not: "))
if is_leap(input_year):
    print(f"{input_year} is a leap year.")
else:
    print(f"{input_year} is not a leap year.")


# another way to check leap year is using the calendar module in python
def is_leapp(year):
    leap = False
    
    # Rule 1: Agar 400 se pura divide ho (jaise 2000)
    if year % 400 == 0:
        leap = True
        
    # Rule 2: Agar 400 se nahi hua, par 100 se ho gaya (jaise 1900)
    elif year % 100 == 0:
        leap = False
        
    # Rule 3: Agar 100 se bhi nahi hua, par 4 se ho gaya (jaise 2024)
    elif year % 4 == 0:
        leap = True
        
    # Baaki sab saal apne aap leap=False rahenge
    
    return leap

year = int(input())
print(is_leapp(year))

# nav