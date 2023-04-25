import os
from math import*
import psycopg2

# function for returning index
def returnIndex(target, arr):
    for i in range(len(arr)):
        if arr[i] == target:
            return i



iChoice = 0
cChoice = 'y'
tempPayment = 0
tempTotal = 0
index = 0
total = 0
count = 0
transactions = []
sChoice = 'y'
order = ''
iceCreams = ["Mango Pop", "Organic Vanilla", "Strawberry Shortcake and Ice Cream", "Cold Coffee and Vanilla Float", "Black Current", "Cotton Candy Flavour Scoop", "Nuts and Caramel"]
iceCreamPrices = [2.5, 3.5, 5, 4, 2, 3, 4]
numOrders = [0, 0, 0, 0, 0, 0, 0]
businessIT = [0, 0, 0, 0, 0, 0, 0]

print("Welcome to Tom and Jerry's Ice Cream Joint!")

while(cChoice == 'y'):
    print("What would you like to do?")
    iChoice = int(input("1. View menu and order\n2. View lifelong transactions in database\n3. View business intelligence\n4. View menu database\n> "))

    if iChoice == 1:
        while(sChoice == 'y'):
            for i in range(len(iceCreams)):
                print(str(i+1) + ". " + iceCreams[i] + ': $', end="")
                print("%.2f" % iceCreamPrices[i])
            iChoice = int(input("Enter the numer associated with your ice cream choice: "))
            numOrders[iChoice-1] += 1
            transactions.append(iceCreams[iChoice - 1])
            sChoice = input("Would you like to order another ice cream? y/n\n> ")

        print("Your order(s): ")
        for i in range(len(numOrders)):
            if numOrders[i] > 0:
                print(numOrders[i], ' ', iceCreams[i])
                if count == 0:
                    order += str(numOrders[i]) + ' ' + iceCreams[i]

                else:
                    order += 'and' + str(numOrders[i]) + ' ' + iceCreams[i]
                count+=1
        for i in range(len(transactions)):
            index = returnIndex(transactions[i], iceCreams)
            total += iceCreamPrices[index]
        print("\nTotal: $", end="")
        print("%.2f" % total)

        while tempTotal < total:
            tempPayment = int(input("Enter payment: "))
            tempTotal += tempPayment

            if tempTotal > total:
                change = tempTotal - total
                print("Change: $", end="")
                print("%.2f" % change)
                break
            if tempTotal == total:
                print("No change")

        # adds order to file
        order += '; and provides $' + str(tempTotal) + ' for payment'
        writer = open("orders.txt", "a") # a = write to, r = read to
        writer.write(order + '\n')
        writer.close()

        # adds data to file
        data = open("data.txt", "a")  # a = write to, r = read to
        for i in range(len(transactions)):
            data.write(transactions[i] + '\n')
        data.close()

    # reading orders to console
    elif iChoice == 2:
        print("\nLifelong transactions: \n")
        f = open("orders.txt", "r")
        print(f.read())

    # reading businessIT to console
    elif iChoice == 3:
        fa = open("data.txt", "r")
        for i in range(len(iceCreams)):
            if fa.readline() == iceCreams[i]:
                businessIT[i] = businessIT[i] + 1
        print("Ice cream type: Quantity sold")
        for i in range(len(businessIT)):
            print(iceCreams[i] + ': ' + str(businessIT[i]))
    elif iChoice == 4:
        # Connecting to the icecreams database
        conn = psycopg2.connect(host='icecream-icecream.aivencloud.com',# using aiven database services
                                port='22708',
                                database='iceCreams',# specifically in iceCreams database
                                user='avnadmin',
                                password='AVNS_R9N_4KAlqMV5lzzRw3N',
                                sslmode='require')

        cur = conn.cursor()
        cur.execute('SELECT * FROM ice')
        rows = cur.fetchall()
        for row in rows:
            print(f"{'$' + str(row[0])} | {row[1]}")# printing the content with a $ next to the price

        # Closing the connection
        conn.close()

    cChoice = input("Return to menu(y/n): ")









