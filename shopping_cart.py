import os 
import dotenv
dotenv.load_dotenv()
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

TAX_RATE = os.getenv("TAXRATE")

# shopping_cart.py

products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71


# TODO: write some Python code here to produce the desired output

#print(products)


# INFO CAPTURE / INPUT

total_price = 0
selected_ids = []

while True:
    selected_id = input("Please input a product identifier, or 'DONE' if there are no more items:") #> "9" (string)
    if selected_id.upper() == "DONE":
        break
    else:
        try:
            if int(selected_id) not in list(range(1,21)):
                print ("Please input item identifier 1-20. Please start over.")
                exit()
        except Exception as err:
            #print(type(err))
            #print(err)
            print ("Please input item identifier 1-20. Please start over.")
            exit()
        selected_ids.append(selected_id)
# INFO DISPLAY / OUTPUT



receipt="---------------------------------\n" + "GREEN FOODS GROCERY\n" + "WWW.GREEN-FOODS-GROCERY.COM\n" + "---------------------------------\n"

# date and time
import datetime;
ct = datetime.datetime.now()
ct = ct.strftime("%Y-%m-%d %H:%M:%S") # Y-m-d H:M:S format
receipt = receipt + "CHECKOUT AT: " + ct + "\n---------------------------------\n"

# list items and price 
receipt = receipt + "SELECTED PRODUCTS:\n" 
for selected_id in selected_ids:
    matching_products = [p for p in products if str(p["id"]) == str(selected_id)]
    matching_product = matching_products[0]
    total_price = total_price + matching_product["price"]
    receipt = receipt + "..." + matching_product["name"] + " (" + to_usd(matching_product["price"]) + ")\n"

receipt = receipt + "---------------------------------\n"
receipt = receipt + "Subtotal: " + to_usd(total_price) + "\n"
tax=total_price*float(TAX_RATE)
receipt = receipt + "Tax: " + to_usd(tax) + "\n"
receipt = receipt + "Total: " + to_usd(tax+total_price) + "\n"
# Thanks message
receipt = receipt + "---------------------------------\n"
receipt = receipt + "THANKS, SEE YOU AGAIN SOON!\n"
receipt = receipt + "---------------------------------\n"
print(receipt)

#Writing Receipts to File
filename = "./receipt/" + ct + ".txt"
with open(filename, "w") as file: # "w" means "open the file for writing"
    file.write(receipt)

# Send receipt to customer email
def sendemail(email):
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
    SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")

    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))

    subject = "Your Receipt from the Green Grocery Store"

    html_content = receipt
    print("HTML:", html_content)

    # FYI: we'll need to use our verified SENDER_ADDRESS as the `from_email` param
    # ... but we can customize the `to_emails` param to send to other addresses
    message = Mail(from_email=SENDER_ADDRESS, to_emails=email, subject=subject, html_content=html_content)

    try:
        response = client.send(message)

        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        print(response.body)
        print(response.headers)

    except Exception as err:
        print(type(err))
        print(err)

email = input("Do you want a copy of receipt to your email address? If yes, please input your email. If no, please input no:\n") 
if email != "no":
    sendemail(email)