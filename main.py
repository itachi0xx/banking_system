from customers import *

customers = {}

for i in range(2):
    name = input("name: ")
    email = input("email: ")
    contact = input("contact: ")

id = input("ID: ")


register_customer(customers, name, email, contact)
