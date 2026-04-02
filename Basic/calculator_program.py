operator = input("enter an operator (+ - * /): ")
num1 = float(input("enter the 1st number: "))
num2 = float(input("enter the 2nd number: "))

if operator == "+":
    result = num1 + num2
    print(round(result, 3))
elif operator == "-":
    result = num1 - num2
    print(round(result, 3))
elif operator == "*":
    result = num1 * num2
    print(round(result, 3))
elif operator == "/":
    result = num1 / num2
    print(round(result, 3))
else:
    print(f"{operator} is not a valid operator")
    
    
# output:
        #enter an operator (+ - * /): *
        #enter the 1st number: 3
        #enter the 2nd number: 15Pp
        #45.0