from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        # Get user inputs from the form
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        travel_date = request.form['travel_date']
        return_date = request.form['return_date']

        chromedriver_path = "C:\\Users\\adith\Downloads\\chromedriver-win32\\chromedriver-win32\\chromedriver.exe"
        service = Service(executable_path=chromedriver_path)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        
        # Generate the flight search URL
        url = f"https://www.kayak.co.in/flights/{from_location}-{to_location}/{travel_date}-flexible-3days/{return_date}-flexible-3days?sort=bestflight_a"
        print(flight_rows)

        # Access the URL and scrape flight details (you can adapt this part from your original script)
        driver.get(url)
        flight_rows = driver.find_elements(By.CSS_SELECTOR, "div.yuAt.yuAt-pres-rounded")
        print(flight_rows)

        # Check if flights are found
        if flight_rows:
            # Extract and compile flight details
            flight_details = ''
            for rows in flight_rows[:3]:
                highs = rows.text
                flight_details += highs + '\n'

            # Additional content for the email
            additional_content = (
                "\n\t*Best and Cheapest price details using Web Scraping through Selenium*\n"
                f"\t\t\tFrom {from_location} to {to_location}\n"
                f"\t\t\tHave a safe journey\n"
                "Below are the flight details scraped from Kayak: \n"
            )

            # Configuration of email settings (you can adapt this part from your original script)
            sender_email = "adithya22110333@snuchennai.edu.in"
            receiver_email = "hashish22110440@snuchennai.edu.in"
            password = "AVM@2010"

            # Create an email message
            message = EmailMessage()
            message["Subject"] = "Flight Details"
            message["From"] = sender_email
            message["To"] = receiver_email
            message.set_content(additional_content + flight_details)

            # Establish a secure connection and send the email
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(message)

            return "Email with flight details sent successfully!"
        else:
            return "No flights found for the given destination."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)