



""" This example uses the Viber Python SDK to create a bot that can add users from a phone number list. 
The code snippet below shows how to use the add_contact() method to add a user to the bot's contact list. """



# Another snippet
import requests
import json
 
# Create a list of dependencies and libraries
dependencies = ["requests", "json"]
 
# Create a requirements.txt file
with open('requirements.txt', 'w') as f:
 for dependency in dependencies:
     f.write(dependency + "\n")
 
# Create chat dialog functions
def send_message(text, keyboard):
 data = {
     "text": text,
     "keyboard": keyboard
 }
 requests.post("https://example.com/bot/message", data=json.dumps(data))
 
# Keyboard samples
keyboard = [
 {
     "Type": "keyboard",
     "DefaultHeight": True,
     "Buttons": [
         {
             "Columns": 6,
             "Rows": 1,
             "BgColor": "#2db9b9",
             "ActionType": "reply",
             "ActionBody": "option1",
             "Text": "<font color=#ffffff><b>Option 1</b></font>"
         },
         {
             "Columns": 6,
             "Rows": 1,
             "BgColor": "#2db9b9",
             "ActionType": "reply",
             "ActionBody": "option2",
             "Text": "<font color=#ffffff><b>Option 2</b></font>"
         }
     ]
 }
]
 
# Send message
send_message(
 text='Hello! Please select an option:',
 keyboard=keyboard
)
 
def add_contact():
 contact = {
   'name': 'John Doe',
   'phone_number': '+123456789'
   }
 # Add contact to Viber
 requests.post("https://example.com/bot/contact", data=json.dumps(contact))
 
# Call add_contact function
add_contact()
 
# Print success message
print("Contact added successfully!")
  





