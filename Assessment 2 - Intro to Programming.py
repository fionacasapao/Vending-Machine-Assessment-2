import os #command use for text to speech
import platform #command to identify if its windows, macos or linux

print("Welcome to BLACK COFFEE vending machine") #Display as greeting when the program is use


def speak_text(text): #text to speech 
    try:
        system = platform.system() #something which return name of operating system (e.g. windows, Darwin, Linux).
        if system == "Windows": #In case the operating system is Windows, it uses PowerShell to create speech. 
            os.system( #Runs a PowerShell command, which involves the use of System.Speech assembly to read the text.
                f'powershell -command "Add-Type -AssemblyName System.Speech;'
                f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;'
                f'$synth.Speak(\'{text}\');"'
            )
        elif system == "Darwin":  #In case of the MacOS system it is using the say command.
            os.system(f"say '{text}'") #Runs the built in say vot.
        elif system == "Linux":#In case of Linux OS, it requires the use of the espeak command.
            os.system(f"espeak '{text}'") #Runs the espeak command and reads out the text.
    except:
        pass #This section deals with the possible errors of the text-to-speech. When something goes wrong, the pass statement will just ignore it and the program will not crash.

#MENU
def show_menu(items):
    print("\n======= MENU =======") #Could display a title of the menu
    for code, item in items.items(): #Home artificial sequences through every single item in the items dictionary. items.items() produces a view object that competes a list of the key
        print(f"[{code}] {item['name']} - AED {item['price']:.2f} (Stock: {item['stock']})") #Prints item code, name, price (rounded out to two decimal points), and stock.
    print("====================") #Prints a menu bottom.


#CHANGE
def calculate_change(amount_paid, total_amount): #it calculates the change
    change = round(amount_paid - total_amount, 2) #Computes the difference between the amount paid and total amount and rounds off to two decimal places
    change_breakdown = {} #It is an empty dictionary that is used to create the breakdown of change denominations.
    denominations = [100, 50, 20, 10, 5, 1, 0.50, 0.25] #Determines a list of possible denominations in UAE currency (in Fils).

    for d in denominations:
        while change >= d: #continues subtracting until it's possible
            change_breakdown[d] = change_breakdown.get(d, 0) + 1 # it counts the denomination
            change = round(change - d, 2) #subtract denomination

    return change_breakdown #sends the breakdown to back from the program


#RECEIPT
def generate_receipt(items, items_bought, total_amount, amount_paid, change): #use to create a receipt 
    receipt = "\n======= RECEIPT =======\n" 
    for code, qty in items_bought.items(): #Loop on how many items were bought.
        receipt += f"{items[code]['name']} x{qty} - AED {items[code]['price'] * qty:.2f}\n" # displays name, quantity and price

    receipt += f"\nTotal: AED {total_amount:.2f}" #displays total amount
    receipt += f"\nPaid: AED {amount_paid:.2f}" #displays amount to be paid
    receipt += f"\nChange: AED {amount_paid - total_amount:.2f}\n" #displays the change

    if change: #Checks whether there is any change to be returned
        receipt += "\nChange Breakdown:\n" #This is added to the receipt to show the change breakdown.
        for d, c in change.items(): #Adds a line to the receipt with the denomination and the number.
            receipt += f"AED {d}: {c}\n" # use to list down denominations

    receipt += "Thank you for your purchase!\n======================" #The receipt is augmented with a thank you message and a footer.
    return receipt #returns the string 


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

    items_bought = {} #creates an empty dictionary. This will be holding the purchase and quantity that the consumer makes.
    total_amount = 0.0 #Records the price of all the items picked.

    speak_text("Welcome to Black Coffee vending machine") #The voice text -to-speech option.

    while True: #Starts an infinite loop. Deactivates the vending machine upon completion or cancellation of the user.
        show_menu(items) #Calls are another feature that can be used to show all items and prices.
        item_code = input("Enter item code (DONE to checkout, CANCEL to cancel): ").upper() # If the store doesn't want to continue the order, they can cancel it

        if item_code == "DONE": #When the user enters the button DONE, the loop comes to an end.
            break # it ends the order and direct to payment

        if item_code == "CANCEL": #Checks whether user would like to cancel order or not.
            print("Order cancelled.") # choice if the user wants to cancel
            speak_text("Order cancelled")
            for code, qty in items_bought.items():
                items[code]["stock"] += qty # it restores stock
            return

        if item_code not in items: #checking if the item is in the list
            print("Invalid item code.")
            speak_text("Invalid item code") #Fades away and reads the cancellation message.
            continue

        if items[item_code]["stock"] == 0: #Recovers the stock deducted all along.
            print("Item out of stock.") #Maintains the accuracy of inventory.
            speak_text("Item out of stock")
            continue

        try:
            qty = int(input("Enter quantity: ")) #allow the user to choose quantity
            if qty <= 0 or qty > items[item_code]["stock"]: #Validates that the code entered is valid in the items dictionary.
                print("Invalid quantity.")
                speak_text("Invalid quantity")
                continue #restarts the loop
        except ValueError:
            print("Please enter a number.")
            speak_text("Please enter a number")
            continue

        items_bought[item_code] = items_bought.get(item_code, 0) + qty #added the item to the basket or cart
        items[item_code]["stock"] -= qty #reduces the stock so it will remain accurate
        total_amount += items[item_code]["price"] * qty #displays the total amount

        print(f"Added {qty} {items[item_code]['name']}") #confirms if the item is added
        print(f"Current total: AED {total_amount:.2f}") #shows the on-going total

        speak_text(f"{qty} {items[item_code]['name']} added") 
        speak_text(f"Your current total is {total_amount:.2f} dirhams") #it announces the total order by speech

    if not items_bought: #it check if the user bought nothing
        print("No items purchased.")
        speak_text("No items purchased") #it ends the function if cart is empty
        return

    
    speak_text(f"Your total amount to pay is {total_amount:.2f} dirhams") #text to speech - it will say the total amount to be paid

    while True:
        try:
            amount_paid = float(input(f"Enter payment (AED {total_amount:.2f}): ")) #accept the payment
            if amount_paid < total_amount: #it disables invalid payment
                print("Insufficient amount.")
                speak_text("Insufficient amount") #it request more amount to be added
            else:
                break #end the loop if the order process is valid
        except ValueError: #it analyze if the input is letters or numbers
            print("Invalid input.")
            speak_text("Invalid input")

    change = calculate_change(amount_paid, total_amount) #call out the function to compute changeS

    receipt = generate_receipt(items, items_bought, total_amount, amount_paid, change)
    print(receipt) # it shows the receipt for the overall order

    speak_text("Payment successful. Thank you for your purchase") # text to speech - it will announce that payment is successful



if __name__ == "__main__":
    vending_machine()



              

               



