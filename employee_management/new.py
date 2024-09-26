from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import requests
import sys


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login')
        layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Enter your email')
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.validate_credentials)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def validate_credentials(self):
        try:
            email = self.email_input.text()
            password = self.password_input.text()

            # Send a POST request to the API with form data
            response = requests.post('https://hrms.schedulesoftware.net/api/login', data={'email': email, 'password': password})
            print(response.json())
            if response.status_code == 200:
                # Assuming the API returns user information in the response
                user_info = response.json()
                QMessageBox.information(self, 'Success', 'Login successful!')
                # Proceed to the dashboard or the next step in your application
                # show_dashboard(user_info) # Uncomment and implement this function as needed
            else:
                QMessageBox.warning(self,'Error',f'An error occurred:{response.status_code}')
                # Show an error message
                QMessageBox.warning(self, 'Error', 'Invalid credentials!')
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the API request
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
        except Exception as e:
            # Handle other exceptions
            QMessageBox.critical(self, 'Error', f'An unexpected error occurred: {e}')


if __name__ == '__main__':
    app = QApplication([])
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
