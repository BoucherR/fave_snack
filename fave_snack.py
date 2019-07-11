import json
from urllib.request import urlopen

"""Simple script to search through two JSON files, and find if the favourite item of a customer is in stock

This python script searches through two JSON files, and determines if the favourite item of a customer is in stock,
and if so, prints the email of the user, the information for the product, and how much it would cost if all of the 
items for all of the customers were to be ordered. 

In other words, if user 'RyanBoucher@realemail.com' has a favourite food 'crunch bar', and 'crunch bar' is in the 
list of products as 'crunch bar' of price '5.00', the program will print a list containing 'RyanBoucher@realemail.com', 
print a list containing 'crunch bar', and print that the total would be $5.00

"""

# Final list that will contain entries of tuples in the form: (customer_email, favourite_food, cost)
final_list = []
# List of available products, that are also favourites of the available customers. Will not allow duplicates
product_list = set()
# List of customer emails, that have favourite foods that are currently being stocked by the company
email_list = []

# Simple function to parse a JSON file from a given URL
def get_data(url):
    return json.loads(urlopen(url).read())

# Takes a JSON that will represent the product list. Goes through the information, pulling out the name of each
# product, and the price. Stores this in a new list, and returns it.
# Example return: list_of_products = [('bread', 3.00), ('apple', 2.50), ('soda', 1.50)]
def generate_product_price_list(p_list):
    list_of_products = []
    for p in p_list["products"]:
        title = p['title']
        for a in p['variants']:
            price = a['price']
        list_of_products.append((title, price));
    return list_of_products

# Takes a JSON that will represent the customer list. Goes through the information, pulling out the name of each
# customer, and the favourite item of said customer. Stores this in a list, and returns it.
# Example return: cust_prod_list = [('cindy@notreal.com', 'soda'), ('alex@fake.com', 'blue berries'), ('me@me', 'beer')]
def generate_customer_snack_list(c_list):
    cust_prod_list = []
    for c in c_list:
        cust_prod_list.append((c['email'], c['fave_snack']))
    return cust_prod_list

# Function that takes a pair as an argument, from the list containing lists of customers, and their favourite snack,
# from generate_customer_face_snack_list(). Compares this against a product_list from generate_product_price_list().
# Returns a tuple if the customer has a favourite snack that is also in stock.
# Example return: ('cindy@notreal.com', 'soda', 1.50)
def customer_snack_in_product_list(customer_product_pair):
        for product in products:
            if product[0] == customer_product_pair[1]: # if the PRODUCT name == cust fave_snack
                return ((customer_product_pair[0], customer_product_pair[1], product[1]))
                # Return Explanation: (email, product, price) as tuple

# List of products that are available. Stored as tuples of (item_name, item_price)
products = generate_product_price_list(
    get_data("https://ca.desknibbles.com/products.json?limit=250"))
# List of customers and their favourite item. Stored as tuples of (customer_email, favourite_food)
cust_and_snack = generate_customer_snack_list(
    get_data("https://s3.amazonaws.com/misc-file-snack/MOCK_SNACKER_DATA.json"))

# Final list, that will store tuples that contain customer emails of customers that favourite food is available,
# and the cost of food.
# Entry example: ('cindy@notreal.com', 'soda', 1.50)
final_list = []

# Mapping the customer_snack_in_product_list function with list of customers and their fave snack
for result in map(customer_snack_in_product_list, cust_and_snack):
    if not result == None:
        final_list.append(result)

total_price = 0
for cust in final_list:
    email_list.append(cust[0])
    product_list.add(cust[1])
    total_price += float(cust[2])

print("---------------------------------------------------------------------")
print("List of products that are 'faves' by customers and are also in stock:")
print(product_list)
print("---------------------------------------------------------------------")
print("List of emails of customers that have 'faves' that are in stock:")
print(email_list)
print("---------------------------------------------------------------------")
print(f"If all of these items were to be ordered, the total cost would be: ${total_price}")
print("---------------------------------------------------------------------")
