import json
import re


NUMBER_PATTERN = r"^0\d{10}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
INFO = "name: {name}\nnumber: {number}\nemail: {email}"
TEXT = """
Enter 1 to "Add a new contact"
Enter 2 to "Edit a contact"
Enter 3 to "Remove a contact by their name"
Enter 4 to "Get the list of all contacts"
Enter 5 to "Get contact by name"
Enter anything else to Exit...
"""    
    

# Create and Read data from the JSON file
try:
    with open('data.json') as f:
        data = json.load(f)
except:
    try:
        open('data.json', 'x').close()
    except:
        pass
    data = {}
    
# Actions
def add_contact():
    name = input("\nEnter contact's name: ")
    
    if data.get(name, False):
        print("contact with the same name already exists!")
        return
    
    number = input(f"Enter {name}'s phone number: ")
    email = input(f"Enter {name}'s email address: ")
    
    while not re.match(NUMBER_PATTERN, number):
        number = input("please enter a valid number: ")
    
    while not re.match(EMAIL_PATTERN, email):
        email = input("please enter a valid email: ")
    
    data[name] = {
        "number": number,
        "email": email,
    }

    print(f"contact \"{name}\" successfuly added")
    

def edit_contact():
    name = input("\nEnter contact's name: ")

    if not data.get(name, False):
        print(f"contact with name \"{name}\" doesn't exist!")
        return
    
    new_name = input(f"Enter {name}'s new name (leave blank if hasn't changed): ")

    while new_name != "" and new_name in data:
        new_name = input("Contact with this name already exists; choose another name (or leave it blank): ")
    
    new_number = input(f"Enter {name}'s new phone number (leave blank if hasn't changed): ")
    new_email = input(f"Enter {name}'s new email address (leave blank if hasn't changed): ")

    while new_number and not re.match(NUMBER_PATTERN, new_number):
        new_number = input("Please enter a valid number: ")
    
    while new_email and not re.match(EMAIL_PATTERN, new_email):
        new_email = input("Please enter a valid email: ")
    
    data[name] = {
        "number": (new_number or data[name]["number"]),
        "email": (new_email or data[name]["email"]),
    }

    if new_name != "":
        data[new_name] = data.pop(name)

    print(f"contact \"{name}\" successfuly updated")
    

def remove_by_name():
    name = input("\nEnter contact's name: ")

    if not data.get(name, False):    
        print(f"contact with name \"{name}\" doesn't exist!")

    number = data.pop(name)
    print(f"contact {name} with number {number} successfuly removed")


def get_contacts():
    # Sort by name
    print()
    print(*[INFO.format(name=name, number=data["number"], email=data["email"]) for name, data in sorted(data.items(), key=lambda item: item[0])], sep="\n\n")


def get_contact_by_name():
    name = input("\nEnter contact's name: ")

    if data.get(name, False):
        number = data[name]["number"]
        email = data[name]["email"]
        print(f"name: {name}\nnumber: {number}\nemail: {email}")
        return
    
    print(f"contact with name \"{name}\" doesn't exist!")


def save_data():
    with open('data.json', 'w') as f:
        json.dump(data, f)


ACTIONS = [
    add_contact, 
    edit_contact, 
    remove_by_name,
    get_contacts, 
    get_contact_by_name,
]

print(TEXT)

while True:
    user_input = input("Enter the action number: ")
    
    if not ("1" <= user_input <= "5"):
        break
    
    ACTIONS[int(user_input)-1]()
    print()
    save_data()
