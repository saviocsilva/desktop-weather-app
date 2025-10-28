import sys
import os
import requests
import pyttsx3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSplashScreen
)
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QBrush, QFontDatabase
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class AppClima(QWidget):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        self.cidade = QLabel("Digite o nome da cidade: ", self)
        self.cidade_input = QLineEdit(self)
        self.botao_clima = QPushButton("Ver clima", self)
        self.botao_previsao = QPushButton("Ver previsão", self)
        self.botao_voz = QPushButton("🔊 Ouvir previsão", self)
        self.temperatura = QLabel(self)
        self.emoji = QLabel(self)
        self.descricao = QLabel(self)
        self.previsao = QLabel(self)
        self.initUI()
        self.definir_localizacao_automatica()

    def initUI(self):
        self.setWindowTitle("Brisa")
        self.setWindowIcon(QIcon(resource_path("icone_clima.ico")))
        self.setFixedSize(400, 600)

        self.aplicar_fundo()
        self.aplicar_fonte()

        vbox = QVBoxLayout()
        vbox.addWidget(self.cidade)
        vbox.addWidget(self.cidade_input)
        vbox.addWidget(self.botao_clima)
        vbox.addWidget(self.botao_previsao)
        vbox.addWidget(self.botao_voz)
        vbox.addWidget(self.temperatura)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.descricao)
        vbox.addWidget(self.previsao)
        self.setLayout(vbox)

        for widget in [self.cidade, self.cidade_input, self.temperatura, self.emoji, self.descricao, self.previsao]:
            widget.setAlignment(Qt.AlignCenter)

        self.botao_clima.clicked.connect(self.ver_clima)
        self.botao_previsao.clicked.connect(self.ver_previsao)
        self.botao_voz.clicked.connect(self.ouvir_previsao)
        self.cidade_input.returnPressed.connect(self.ver_clima)
        self.cidade_input.setFocus()

    def aplicar_fundo(self):
        palette = QPalette()
        pixmap = QPixmap(resource_path("fundo_clima.png"))
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def aplicar_fonte(self):
        QFontDatabase.addApplicationFont(resource_path("Roboto-Regular.ttf"))
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: 'Roboto';
                color: white;
                background-color: rgba(0, 0, 0, 0);
            }
            QLabel#emoji {
                font-size: 100px;
                font-family: 'Segoe UI Emoji';
            }
            QLabel {
                font-size: 30px;
            }
            QLineEdit {
                font-size: 30px;
                background-color: rgba(255, 255, 255, 180);
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton {
                font-size: 25px;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 200);
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)

    def definir_localizacao_automatica(self):
        try:
            resposta = requests.get("http://ip-api.com/json/")
            dados = resposta.json()
            cidade = dados.get("city", "")
            lat = dados.get("lat")
            lon = dados.get("lon")
            if cidade and lat and lon:
                self.cidade_input.setText(cidade)
                self.obter_clima_por_coordenadas(lat, lon)
        except:
            pass

    def obter_clima_por_coordenadas(self, lat, lon):
        self.buscar_clima(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=ab9014a8413864f1e37b21de72cdaed6&lang=pt_br")

    def ver_clima(self):
        cidade = self.cidade_input.text()
        if cidade:
            self.buscar_clima(f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid=ab9014a8413864f1e37b21de72cdaed6&lang=pt_br")

    def buscar_clima(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()

            kelvin = dados["main"]["temp"]
            celsius = kelvin - 273.15
            clima_id = dados["weather"][0]["id"]
            descricao = dados["weather"][0]["description"]

            self.temperatura.setText(f"{celsius:.0f}°C")
            self.emoji.setText(self.mostrar_emoji(clima_id))
            self.descricao.setText(descricao.capitalize())
            self.previsao.clear()

            cor = "red" if celsius > 35 or celsius < 5 or clima_id < 800 else "white"
            self.temperatura.setStyleSheet(f"font-size: 75px; color: {cor};")

        except:
            self.temperatura.setText("Erro ao buscar clima.")
            self.emoji.clear()
            self.descricao.clear()
            self.previsao.clear()

    def ver_previsao(self):
        cidade = self.cidade_input.text()
        #INSERT API HERE

        try:
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()

            dias = {}
            for item in dados["list"]:
                data = item["dt_txt"].split(" ")[0]
                if data not in dias:
                    temp = item["main"]["temp"] - 273.15
                    desc = item["weather"][0]["description"]
                    dias[data] = f"{data}:\n{temp:.0f}°C, {desc.capitalize()}"
                if len(dias) == 3:
                    break

            texto = "\n\n".join(dias.values())
            self.previsao.setText(texto)

        except:
            self.previsao.setText("Erro ao buscar previsão.")

    def ouvir_previsao(self):
        texto = self.temperatura.text() + ", " + self.descricao.text()
        self.engine.say(texto)
        self.engine.runAndWait()

    def mostrar_emoji(self, clima_id):
        if 200 <= clima_id <= 232:
            return "⛈️"
        elif 300 <= clima_id <= 321:
            return "☁️"
        elif 500 <= clima_id <= 531:
            return "🌧️"
        elif 600 <= clima_id <= 622:
            return "❄️"
        elif 701 <= clima_id <= 741:
            return "🌫️"
        elif clima_id == 762:
            return "🌋"
        elif clima_id == 771:
            return "🍃"
        elif clima_id == 781:
            return "🌪️"
        elif clima_id == 800:
            return "☀️"
        else:
            return "🌤️"

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash_pix = QPixmap(resource_path("splash_brisa.png"))
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.FramelessWindowHint)
    splash.setEnabled(False)
    splash.show()

    fade = QPropertyAnimation(splash, b"windowOpacity")
    fade.setDuration(1500)
    fade.setStartValue(1)
    fade.setEndValue(0)
    fade.setEasingCurve(QEasingCurve.OutCubic)

    janela = AppClima()

    def iniciar_app():
        splash.close()
        janela.show()

    QTimer.singleShot(2000, lambda: fade.start())
    QTimer.singleShot(3500, iniciar_app)

    sys.exit(app.exec_())
