foods = []
prices = []
total = 0

while True:
    food = input("enter a food to buy (q to quit): ")
    if food.lower() == "q":
        break
    else:
        price = float(input(f"enter the price of a {food}: $"))
        foods.append(food)
        prices.append(price)
print("__________Your Cart___________")


#output:
       #enter a food to buy (q to quit): banana
       #enter the price of a banana: $12
       #enter a food to buy (q to quit): q
       #__________Your Cart___________