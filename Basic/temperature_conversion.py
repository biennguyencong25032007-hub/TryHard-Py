unit = input("is this temperature in Celsius or Fahrenheit (c/F): ")
temp = float(input("enter the temperature: "))

if unit == "C":
    temp = round((9 * temp)/ 5 + 32, 1)
    print(f"the temerature in Fahrenheit is: {temp} 'F ")
elif unit == "F":
    temp = round((temp - 32) * 5 / 9, 1)
    print(f"the temperature in Celsius is: {temp} 'C ")
else:
    print(f"{unit} is an invalid unit of measurement ")
    
    
#output:
       #is this temperature in Celsius or Fahrenheit (c/F): C
       #enter the temperature: 36
       #the temerature in Fahrenheit is: 96.8 'F 