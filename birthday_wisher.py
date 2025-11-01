import json
import datetime
import pywhatkit
import time
import os

# --- IMPORTANT: SET YOUR FULL PATHS HERE ---
# Use \\ for backslashes if on Windows
# Example: "C:\\Users\\YourName\\Desktop\\MyProject\\birthdays.json"
JSON_FILE_PATH = "D:\\Coding\\Python\\AI\\BIRTHDAY\\birthdays.json"
# ----------------------------------------------

def load_contacts():
    """Loads contact data from the JSON file."""
    if not os.path.exists(JSON_FILE_PATH):
        print("File not found, creating a new 'birthdays.json'")
        return []
        
    try:
        with open(JSON_FILE_PATH, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error reading JSON file. It might be empty or corrupt.")
        return []
    except Exception as e:
        print(f"An error occurred loading file: {e}")
        return []

def save_contacts(contacts):
    """Saves the updated contacts list back to the JSON file."""
    try:
        with open(JSON_FILE_PATH, 'w') as f:
            json.dump(contacts, f, indent=2)
    except Exception as e:
        print(f"CRITICAL ERROR: Could not save updated contacts file: {e}")

def check_birthdays_and_send_messages(contacts):
    """
    Checks for birthdays and sends messages via WhatsApp.
    Will only send a message if it hasn't been sent in the current year.
    """
    
    # Get today's date and year
    today = datetime.date.today()
    today_str = today.strftime("%m-%d") # Format: "11-02"
    current_year = today.year          # Format: 2025
    
    print(f"--- Birthday Wisher running on {today} ---")
    print(f"Checking for birthdays on: {today_str}")

    found_birthday = False
    contacts_updated = False
    
    for person in contacts:
        # Check 1: Is today their birthday?
        if person['birthdate'] == today_str:
            found_birthday = True
            name = person['name']
            phone = person['phone']
            
            # Check 2: Have we already sent them a message this year?
            # .get() is a safe way to check if 'last_sent_year' exists
            if person.get('last_sent_year') != current_year:
                print(f"Found birthday for {name}! Sending message...")
                
                message = f"🎉 Happy Birthday! {name}🎂\nWishing you a day filled with laughter, love, and all the things that make you smile. May this year bring new adventures, exciting challenges, and beautiful memories."
                
                try:
                    pywhatkit.sendwhatmsg_instantly(
                        phone_no=phone,
                        message=message,
                        wait_time=25,  # 30 seconds should be safe
                        tab_close=True
                    )
                    print(f"Successfully sent message to {name}.")
                    
                    # IMPORTANT: Update the log
                    person['last_sent_year'] = current_year
                    contacts_updated = True
                    
                    time.sleep(15) # Wait before processing next person
                    
                except Exception as e:
                    print(f"Error sending message to {name}: {e}")
            
            else:
                # Birthday is today, but we already sent one
                print(f"Message already sent to {name} this year. Skipping.")

    if not found_birthday:
        print("No birthdays found today.")

    # If we updated any contact's "last_sent_year", save the file
    if contacts_updated:
        print("Saving updated 'last_sent_year' data to JSON file...")
        save_contacts(contacts)
    
    print("--- Script finished ---")

# --- Main part of the script ---
if __name__ == "__main__":
    contacts_list = load_contacts()
    if contacts_list:
        check_birthdays_and_send_messages(contacts_list)
    else:
        print("No contacts found in 'birthdays.json'. Exiting.")