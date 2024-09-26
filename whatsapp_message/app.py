import pywhatkit as kit
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def send_whatsapp_message_with_pdf(recipient_phone_number, message, pdf_path):
    # Send an initial message to open the chat
    kit.sendwhatmsg_instantly(recipient_phone_number, message)

    # Wait for WhatsApp Web to open and the message to be sent
    time.sleep(15)  # Adjust the sleep time based on your internet speed

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=./User_Data")  # Keeps the WhatsApp session logged in
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com")

    # Wait for WhatsApp Web to load
    time.sleep(10)  # Adjust the sleep time based on your internet speed

    # Locate the attachment icon and click it
    attachment_icon = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="clip"]')
    attachment_icon.click()
    time.sleep(2)

    # Locate and click the document option
    document_option = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    document_option.send_keys(pdf_path)
    time.sleep(2)

    # Click the send button
    send_button = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="send"]')
    send_button.click()


    # Close the WebDriver
    time.sleep(5)
    driver.quit()


# Example usage
recipient_phone_number = "+918128984766"  # Replace with the recipient's phone number
message = "Here is your document."
pdf_path = "131_Nike.pdf"  # Replace with the path to your PDF document

send_whatsapp_message_with_pdf(recipient_phone_number, message, pdf_path)
