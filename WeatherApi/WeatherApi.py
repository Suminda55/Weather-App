import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget,QLabel,QPushButton,
                             QLineEdit,QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter City",self)
        self.setWindowIcon(QIcon("I:/myPythonFirstProject/WeatherApi/scattered-thunderstorms_1959321.png"))
        self.my_detail = QLabel("Made by :-  K.M.S.L.Kalupahana\nBSc in Computer Science\nTrincomalee campus")
        self.city_input = QLineEdit(self)
        self.check_button = QPushButton("Check",self)
        self.temperature_label1_F = QLabel(self)
        self.temperature_label2_K= QLabel(self)
        self.temperature_label3_C = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.check_button)
        vbox.addWidget(self.temperature_label1_F)
        vbox.addWidget(self.temperature_label2_K)
        vbox.addWidget(self.temperature_label3_C)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.my_detail,0,Qt.AlignRight | Qt.AlignBottom)


        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label1_F.setAlignment(Qt.AlignCenter)
        self.temperature_label2_K.setAlignment(Qt.AlignCenter)
        self.temperature_label3_C.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.my_detail.setAlignment(Qt.AlignRight)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label1_F.setObjectName("temperature_label1_F")
        self.temperature_label2_K.setObjectName("temperature_label2_K")
        self.temperature_label3_C.setObjectName("temperature_label3_C")
        self.check_button.setObjectName("check_button")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.my_detail.setObjectName("my_detail")

        self.setStyleSheet("""
            QLabel,QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size:30px;
                font-family:Berlin Sans FB;
            }
            QLineEdit#city_input{
                font-size: 30px;
            }
            QPushButton#check_button{
                font-size: 25px;
                font-weight: bold;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                letter-spacing: 1px;
            }
            QPushButton#check_button:hover{
                background-color: #1976D2;
                box-shadow: 0 6px 12px rgba(33, 150, 243, 0.3);
            }
            QPushButton#check_button:pressed{
                background-color: #1565C0;
                box-shadow: 0 3px 6px rgba(33, 150, 243, 0.3);
            }
            QPushButton#check_button:disabled{
                background-color: #BDBDBD;
                color: #757575;
            }
            QLabel#temperature_label3_C{
                font-size: 65px;
            }
            QLabel#temperature_label2_K{
                font-size: 65px;
            }
            QLabel#temperature_label1_F{
                font-size: 65px;
            }
            QLabel#emoji_label{
                font-size: 80px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 30px;
                font-family: Arial Rounded MT Bold;
            }
            QLabel#my_detail{
            font-size: 12px;
            color: gray;
            padding: 5px;
            }
            """)

        self.check_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "a4b8d96527370cd67119cb076ea24c26"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_Err:
                match response.status_code:  #https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status#informational_responses . I got below errors from this site
                    case 400:
                        self.display_error("Bad Request\ncheck your input!")
                    case 401:
                        self.display_error("Unauthorized\nInvalid API!")
                    case 403:
                        self.display_error("Forbidden\n Access is denied!")
                    case 404:
                        self.display_error("Not found\nCity Not found!")
                    case 500:
                        self.display_error("Internal Server Error\nplease try again later!")
                    case 502:
                        self.display_error("Bad Gateway\nInvalid respones from the server")
                    case 503:
                        self.display_error("Service Unavailable\ncSever is down!")
                    case 504:
                        self.display_error("Gateway Timeout\nNo respones from the server!")
                    case _:
                        self.display_error(f"HTTP error occured \n{http_Err}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error: \nCheck Your Connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error: \nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirection:\nCheck the URL ")
        except requests.exceptions.RequestException as Req_Err:
            self.display_error(f"Request Error:\n{Req_Err}")

    def display_error(self,message):

        self.temperature_label1_F.setStyleSheet("font-size:15px;"
                                             "font-family:Arial")
        self.temperature_label1_F.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.temperature_label3_C.clear()
        self.temperature_label2_K.clear()
    def display_weather(self,data):
        self.temperature_label1_F.setStyleSheet("font-size:50px;"
                                             "font-family:Arial;"
                                             "font-weight:bold;"
                                             "font-style:italic")
        self.temperature_label2_K.setStyleSheet("font-size:50px;"
                                                "font-family:Arial;"
                                                "font-weight:bold;"
                                                "font-style:italic")
        self.temperature_label3_C.setStyleSheet("font-size:50px;"
                                                "font-family:Arial;"
                                                "font-weight:bold;"
                                                "font-style:italic")

        temp_K = data["main"]["temp"]
        temp_C = temp_K -273.15
        temp_F = (temp_K * 9/5) - 459.67

        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label1_F.setText(f"{temp_F:.0f}°F")
        self.temperature_label2_K.setText(f"{temp_K:.0f}K")
        self.temperature_label3_C .setText(f"{temp_C:.0f}C°")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)


    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <=232:
            return "⛈️"
        elif 300<= weather_id <= 321:
            return "🌦️"
        elif 500<= weather_id <= 531:
            return "🌧️️"
        elif 600<= weather_id <= 622:
            return "❄️"
        elif 700<= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "⛅"
        elif 801<= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_())


