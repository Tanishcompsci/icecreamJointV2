import psycopg2
import requests
import requests
# function for returning index
def returnFirstIndex(target, arr):
    for i in range(len(arr)):
        if arr[i] == target:
            return i

def returnAPICall():
    BASE = "http://127.0.0.1:5000/"

    flavorsPrice = [{'name': "Mango Pop", 'price': 2.5},
                    {'name': "Organic Vanilla", 'price': 3.5},
                    {'name': "Strawberry Shortcake and Ice Cream", 'price': 5},
                    {'name': "Cold Coffee and Vanilla Float", 'price': 4},
                    {'name': "Black Current", 'price': 2},
                    {'name': "Cotton Candy Flavour Scoop", 'price': 3},
                    {'name': "Nuts and Caramel", 'price': 4}]
    for i in range(len(flavorsPrice)):
        response = requests.put(BASE + "iceCream/" + str(i), flavorsPrice[i])
        print(response.json())
# functions takes total and prompts user for payment
def runCashRegister(total, tempTotal):
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


# finds the total price based on iceCream prices and the orders the user has
def computeTotal(total, iceCreamPrices, transactions, iceCreams):
    for i in range(len(transactions)):
        index = returnFirstIndex(transactions[i], iceCreams)
        total = total + iceCreamPrices[index]
    return total


# void function reads the transactions from orders file
def readTransactions():
    print("\nLifelong transactions: \n")
    f = open("orders.txt", "r")
    print(f.read())


# reads the menu from aiven database
def readMenuFromData():
    # Connecting to the icecreams database
    conn = psycopg2.connect(host='icecream-icecream.aivencloud.com',  # using aiven database services
                            port='22708',
                            database='iceCreams',  # specifically in iceCreams database
                            user='avnadmin',
                            password='AVNS_R9N_4KAlqMV5lzzRw3N',
                            sslmode='require')

    cur = conn.cursor()
    cur.execute('SELECT * FROM ice')
    rows = cur.fetchall()
    count = 1
    for row in reversed(rows):
        print(str(count) + ". ", end="")
        print(f"{'$' + str(row[0])} | {row[1]}")  # printing the content with a $ next to the price
        count+=1
    # Closing the connection
    conn.close()


# prints the orders that the user made
def printOrders(numOrders, iceCreams, order, count):
    for i in range(len(numOrders)):
        if numOrders[i] > 0:
            print(numOrders[i], ' ', iceCreams[i])

# adds each order to the orders.txt file
def addOrder(numOrders, iceCreams, order, count):
    for i in range(len(numOrders)):
        if numOrders[i] > 0:
            if count == 0:
                order += str(numOrders[i]) + ' ' + iceCreams[i]
            else:
                order += ' and ' + str(numOrders[i]) + ' ' + iceCreams[i]
            count += 1
    return order
def orderToFile(order, total):
    order += '; and provides $' + str(total) + ' for payment'
    writer = open("orders.txt", "a")  # a = write to, r = read to
    writer.write(order + '\n')
    writer.close()


# reads business data from a fule and prints it
def readData(iceCreams, businessIT):
    fa = open("data.txt", "r")
    contents = fa.read()

    for i in range(len(iceCreams)):
        if iceCreams[i] in contents:
            count = contents.count(iceCreams[i])
            businessIT[i] = count
    print("Ice cream type: Quantity sold")
    for i in range(len(businessIT)):
        print(iceCreams[i] + ': ' + str(businessIT[i]))


def addArrayListToFile(transactions):
    data = open("data.txt", "a")  # a = write to, r = read to
    for i in range(len(transactions)):
        data.write(transactions[i] + '\n')
    data.close()


def listOptions(iceCreams, iceCreamPrices):
    for i in range(len(iceCreams)):
        print(str(i + 1) + ". " + iceCreams[i] + ': $', end="")
        print("%.2f" % iceCreamPrices[i])


def getOrder(numOrders, iceCreams, transactions):
    iChoice = int(input("Enter the numer associated with your ice cream choice: "))
    numOrders[iChoice - 1] += 1
    transactions.append(iceCreams[iChoice - 1])
