from functions import*
import requests

iChoice = 0
cChoice = 'y'
transactions = []
iceCreams = ["Mango Pop", "Organic Vanilla", "Strawberry Shortcake and Ice Cream", "Cold Coffee and Vanilla Float", "Black Current", "Cotton Candy Flavour Scoop", "Nuts and Caramel"]
iceCreamPrices = [2.5, 3.5, 5, 4, 2, 3, 4]
businessIT = [0, 0, 0, 0, 0, 0, 0]

print("Welcome to Tom and Jerry's Ice Cream Joint!")

# main menu
while cChoice == 'y' or cChoice == 'Y':
    # variables are reset for every new order
    tempPayment = tempTotal = index = count = 0
    total = 0
    numOrders = [0, 0, 0, 0, 0, 0, 0]
    order = ''
    sChoice = 'y'
    print("What would you like to do?")
    iChoice = int(input("1. View menu and order\n2. View lifelong transactions in database\n3. View business intelligence\n4. View menu database in API\n> "))

    if iChoice == 1:

        # asking for orders
        while sChoice == 'y':
            readMenuFromData() # lists the menu
            getOrder(numOrders, iceCreams, transactions)  # asks user for their order
            sChoice = input("Would you like to order another ice cream? y/n\n> ")

        # printing user's orders
        print("Your order(s): ")
        printOrders(numOrders, iceCreams, order, count)
        order = addOrder(numOrders, iceCreams, order, count) # adding order to a temp variable

        # computes the total and prompts user to pay
        total = computeTotal(total, iceCreamPrices, transactions, iceCreams)
        runCashRegister(total, tempTotal)

        # adds this order to a file
        orderToFile(order, total)

        # adds business data (total transactions) to file
        addArrayListToFile(transactions)

    # reading orders to console
    elif iChoice == 2:
        readTransactions()

    # reading businessIT to console
    elif iChoice == 3:
        readData(iceCreams, businessIT) # reads business data to console

    # reading menu database to console
    elif iChoice == 4:
        returnAPICall()

    cChoice = input("Return to menu(y/n): ")
