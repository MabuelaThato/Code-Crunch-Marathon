import geocoder
import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

def get_coordinates():
    g = geocoder.ip("me")

    if g.latlng is not None:
        return g.latlng
    else:
        return None


def main():
    #Get coordinates
    coordinates = get_coordinates()
    if coordinates is not None:
        latitude, longitude = coordinates
    else:
        print("Unable to retrieve your GPS coordinates.")
    
    load_dotenv()
    #Get weather
    key = os.getenv("OPEN_KEY")
    short_url = os.getenv("OPEN_URL")
    url = f"{short_url}lat={latitude}&lon={longitude}&exclude=hourly,daily&appid={key}"
    response = requests.get(url).json()
    rainy = response["current"]["weather"][0]["main"]

    #Set up messaging
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    number = input("Enter you cell number. Eg +27794552808: ")

    #Send messages
    if rainy.lower() == "rain":
        message = client.messages.create(
                body="The weather is expected to rain.",
                from_=os.getenv("TWILIO_NUMBER"),
                to = number,
                )
        print(message.body)
    else:
        message = client.messages.create(
                body="The weather is not expected to rain.",
                from_=os.getenv("TWILIO_NUMBER"),
                to = number,
                )
        print(message.body)

if __name__ == "__main__":
    main()