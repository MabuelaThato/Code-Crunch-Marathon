import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import smtplib

def send_email(name, email):
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.ehlo()
    server.starttls
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("PASSWORD")  
    server.login(sender, password)
    server.sendmail(sender, email , 
    f"""Heyy {name}!
    Happy birthday, wishing you many more!

    Regards 
    Thato Mabuela
    """)
    server.quit()
    


def main():
    #Get spread sheet
    load_dotenv()
    end_point = os.getenv("SHEETY_END_POINT")
    response = requests.get(end_point).json()["sheet1"]

    #Get current date
    current_date = datetime.now()
    month = current_date.month
    day = current_date.day
    date = f"{day}/{month}"

    for person in response:
        name = person["name"]
        email = person["email"]
        dob= person["dob"]

        if dob == date:
            send_email(name, email)
        else:
            print("Dont send email")

if __name__ == "__main__":
    main()