import geocoder
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from geopy.geocoders import Nominatim

# Define a function to get the current location (latitude, longitude)
def get_location():
    # Use geocoder to get IP-based latitude and longitude
    g = geocoder.ip('me')
    latitude = g.latlng[0] if g.latlng else None
    longitude = g.latlng[1] if g.latlng else None

    # Use geopy to reverse geocode and get more accurate location details (street, city, state)
    if latitude and longitude:
        geolocator = Nominatim(user_agent="_safety_bot")
        location = geolocator.reverse((latitude, longitude), language="en", exactly_one=True)
        if location:
            address = location.address
            address_parts = address.split(",")
            street = address_parts[0] if len(address_parts) > 0 else "Unknown"
            city = address_parts[1] if len(address_parts) > 1 else "Unknown"
            state = address_parts[2] if len(address_parts) > 2 else "Unknown"
            country = address_parts[-1] if len(address_parts) > 3 else "Unknown"
            return (latitude, longitude), street, city, state, country
        else:
            return None, None, "Unknown", "Unknown", "Unknown"
    return None, None, "Unknown", "Unknown", "Unknown"

# Define a function to send an SOS email
def send_sos_email(location, street, city, state, country, emergency_contact_email):
    sender_email = "your_email@gmail.com"  # Sender's email
    receiver_email = emergency_contact_email  # Receiver's email (SOS contact)
    password = "your_email_password"  # Sender's email password

    # Email subject and body
    subject = "URGENT: Safety SOS Activated!"
    body = f"Emergency Alert!\n\nA safety emergency was triggered.\nLocation details:\nLatitude: {location[0]}\nLongitude: {location[1]}\nStreet: {street}\nCity: {city}\nState: {state}\nCountry: {country}"

    # Setup email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Sending the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("SOS email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to handle chatbot conversation
def chatbot():
    print("Hello, I am your Safety Bot. How can I assist you today?")
    while True:
        user_input = input("You: ").lower()

        if "hello" in user_input:
            print("Bot: Hi! How can I help you?")
        
        elif "help" in user_input:
            print("Bot: I am here to help you with safety-related issues. You can say 'Emergency' to trigger SOS or ask for your location.")
        
        elif "emergency" in user_input or "help me" in user_input:
            print("Bot: Emergency triggered. Fetching your location...")
            location, street, city, state, country = get_location()
            if location:
                print(f"Bot: Your current location details are as follows:\nLatitude: {location[0]}\nLongitude: {location[1]}\nStreet: {street}\nCity: {city}\nState: {state}\nCountry: {country}")
            
                # Trigger SOS email
                emergency_contact_email = "emergency_contact_email@example.com"  # Replace with your emergency contact
                send_sos_email(location, street, city, state, country, emergency_contact_email)
                print("Bot: SOS has been sent to your emergency contact. Help is on the way!")
            else:
                print("Bot: Unable to retrieve your location. Please check your connection or try again.")
            break
        
        elif "location" in user_input:
            location, street, city, state, country = get_location()
            if location:
                print(f"Bot: Your current location is:\nLatitude: {location[0]}\nLongitude: {location[1]}\nStreet: {street}\nCity: {city}\nState: {state}\nCountry: {country}")
            else:
                print("Bot: Unable to retrieve your location. Please check your connection or try again.")
        
        elif "quit" in user_input:
            print("Bot: Goodbye! Stay safe!")
            break

        else:
            print("Bot: I'm sorry, I didn't understand that. Can you please rephrase?")

# Start the chatbot
if __name__ == "__main__":
    chatbot()
