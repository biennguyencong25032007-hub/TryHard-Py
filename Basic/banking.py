def show_balance(balance):
    print("**************************")
    print(f"your balace is ${balance:2f}")
    print("**************************")
    
def deposit():
    print("****************************")
    amount = float(input("enter an amount to be deposited: "))
    print("****************************")
    if amount < 0:
        print("**************************")
        print("that is not a valid amount")
        print("**************************")
        return 0
    else:
        return amount

def withdraw(balance):
    print("**************************")
    amount = float(input("amount must be greater than 0"))
    print("**************************")
    
    if amount > balance:
        print("**************************")
        print("insufficient funds")
        print("**************************")
        return 0
    elif amount < 0:
        print("**************************")
        print("amount must be greater than 0")
        print("**************************")
        return 0
    else:
        return amount
    
def main():
    
    balance = 0
    is_running = True

    while is_running:
        print("*********************")
        print("   banking program   ")
        print("*********************")

        print("1.show balance")
        print("2.deposit")
        print("3.withdraw")
        print("4.exit")
        print("*********************")
        
        choice = input("enter your choice (1-4): ")
    
        if choice == '1':
           show_balance(balance)
        elif choice == '2':
            balance += deposit()
        elif choice == '3':
            balance -= withdraw(balance)
        elif choice == '4':
            is_running = False
        else:
            print("**************************")
            print("that is not a valid choice")
            print("**************************")
            
    print("***************************")        
    print("thank yoU! have a nice day!")
    print("***************************")
    
if __name__ == "__name__":
   main()  
    