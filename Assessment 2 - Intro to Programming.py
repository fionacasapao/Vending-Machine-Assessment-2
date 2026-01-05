import os #command use for text to speech
import platform #command to identify if its windows, macos or linux

print("Welcome to BLACK COFFEE vending machine") #Display as greeting when the program is use


def speak_text(text): #text to speech 
    try:
        system = platform.system()
        if system == "Windows":
            os.system(
                f'powershell -command "Add-Type -AssemblyName System.Speech;'
                f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;'
                f'$synth.Speak(\'{text}\');"'
            )
        elif system == "Darwin":  # it uses macOS
            os.system(f"say '{text}'")
        elif system == "Linux":#it uses Linux
            os.system(f"espeak '{text}'")
    except:
        pass #it ignores any error so the program will continue working

#MENU
def show_menu(items):
    print("\n======= MENU =======") #It is the header for the menu
    for code, item in items.items(): #loop for every item in the menu
        print(f"[{code}] {item['name']} - AED {item['price']:.2f} (Stock: {item['stock']})") #item code, name, price and remaining stock
    print("====================")


#CHANGE
def calculate_change(amount_paid, total_amount): #it calculates the change
    change = round(amount_paid - total_amount, 2) #round (,2) is use to avoid any decimal error
    change_breakdown = {} #it is use to store denomination like 10AED x 2
    denominations = [100, 50, 20, 10, 5, 1, 0.50, 0.25] #current UAE currency

    for d in denominations:
        while change >= d: #continues subtracting until it's possible
            change_breakdown[d] = change_breakdown.get(d, 0) + 1 # it counts the denomination
            change = round(change - d, 2) #subtract denomination

    return change_breakdown #sends the breakdown to back from the program


#RECEIPT
def generate_receipt(items, items_bought, total_amount, amount_paid, change): #use to create a receipt 
    receipt = "\n======= RECEIPT =======\n"
    for code, qty in items_bought.items(): #loop for purchased products
        receipt += f"{items[code]['name']} x{qty} - AED {items[code]['price'] * qty:.2f}\n" # displays name, quantity and price

    receipt += f"\nTotal: AED {total_amount:.2f}" #displays total amount
    receipt += f"\nPaid: AED {amount_paid:.2f}" #displays amount to be paid
    receipt += f"\nChange: AED {amount_paid - total_amount:.2f}\n" #displays the change

    if change:
        receipt += "\nChange Breakdown:\n"
        for d, c in change.items():
            receipt += f"AED {d}: {c}\n" # use to list down denominations

    receipt += "Thank you for your purchase!\n======================"
    return receipt


def vending_machine(): #uses dictionary to store the data
    items = {
        "I1": {"name": "White Mocha", "price": 20.00, "stock": 10},
        "I2": {"name": "Caramel Machiato", "price": 20.00, "stock": 10},
        "I3": {"name": "Espresso Shot", "price": 5.00, "stock": 10},
        "I4": {"name": "Latte", "price": 18.00, "stock": 10},
        "I5": {"name": "Tea", "price": 1.50, "stock": 10},
        "I6": {"name": "Brownie", "price": 7.00, "stock": 20},
        "I7": {"name": "Chocolate Cookie", "price": 7.00, "stock": 25},
        "I8": {"name": "Caramel Cookie", "price": 7.00, "stock": 25},
        "I9": {"name": "Oats and Raisin", "price": 8.00, "stock": 25},
        "I10": {"name": "Croissant", "price": 5.00, "stock": 30},
    }

    items_bought = {}
    total_amount = 0.0

    speak_text("Welcome to Black Coffee vending machine")

    while True:
        show_menu(items)
        item_code = input("Enter item code (DONE to checkout, CANCEL to cancel): ").upper() # If the store doesn't want to continue the order, they can cancel it

        if item_code == "DONE":
            break # it ends the order and direct to payment

        if item_code == "CANCEL":
            print("Order cancelled.") # choice if the user wants to cancel
            speak_text("Order cancelled")
            for code, qty in items_bought.items():
                items[code]["stock"] += qty # it restores stock
            return

        if item_code not in items: #checking if the item is in the list
            print("Invalid item code.")
            speak_text("Invalid item code")
            continue

        if items[item_code]["stock"] == 0: #checking if the item is still in stock
            print("Item out of stock.")
            speak_text("Item out of stock")
            continue

        try:
            qty = int(input("Enter quantity: ")) #allow the user to choose quantity
            if qty <= 0 or qty > items[item_code]["stock"]:
                print("Invalid quantity.")
                speak_text("Invalid quantity")
                continue
        except ValueError:
            print("Please enter a number.")
            speak_text("Please enter a number")
            continue

        items_bought[item_code] = items_bought.get(item_code, 0) + qty #added the item to the basket or cart
        items[item_code]["stock"] -= qty #reduces the stock so it will remain accurate
        total_amount += items[item_code]["price"] * qty #displays the total amount

        print(f"Added {qty} {items[item_code]['name']}")
        print(f"Current total: AED {total_amount:.2f}")

        speak_text(f"{qty} {items[item_code]['name']} added")
        speak_text(f"Your current total is {total_amount:.2f} dirhams")

    if not items_bought:
        print("No items purchased.")
        speak_text("No items purchased")
        return

    
    speak_text(f"Your total amount to pay is {total_amount:.2f} dirhams") #text to speech - it will say the total amount to be paid

    while True:
        try:
            amount_paid = float(input(f"Enter payment (AED {total_amount:.2f}): ")) #accept the payment
            if amount_paid < total_amount: #it disables invalid payment
                print("Insufficient amount.")
                speak_text("Insufficient amount")
            else:
                break
        except ValueError:
            print("Invalid input.")
            speak_text("Invalid input")

    change = calculate_change(amount_paid, total_amount)

    receipt = generate_receipt(items, items_bought, total_amount, amount_paid, change)
    print(receipt) # it shows the receipt for the overall order

    speak_text("Payment successful. Thank you for your purchase") # text to speech - it will announce that payment is successful



if __name__ == "__main__":
    vending_machine()



              

               



