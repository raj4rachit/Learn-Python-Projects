import time
import pyautogui
import pywhatkit as kit

# Replace with the recipient's phone number including the country code
phone_number = "+918128984766"

message = f"Hello, this is a test message from pywhatkit! 1"
kit.sendwhatmsg_instantly(phone_number, message)

# Function to send a message using pyautogui
def send_message_via_pyautogui(message):
    pyautogui.typewrite(message)
    pyautogui.press('enter')

# Function to close the current browser tab
def close_browser_tab():
    # Adjust the sleep time if necessary to give the browser enough time to open and send the message
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'w')

for i in range(4):
    # Send the message instantly
    try:
        message = f"Hello, this is a test message from test! {i+2}"
        send_message_via_pyautogui(message)
        print(f"Message {i+2}sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Wait for 5 seconds before sending the next message
    time.sleep(5)

close_browser_tab()
print("All messages sent.")
