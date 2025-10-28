# desktop-weather-app
Brisa - Desktop Weather App
Brisa is a clean, simple, and user-friendly desktop weather application built with Python. It provides real-time weather data, a 7-day forecast, and location-based search, all powered by the OpenWeatherMap API.

Key Features
Real-Time Weather: Get instant access to current temperature, humidity, and wind speed.

7-Day Forecast: Plan your week with a detailed forecast for the next seven days.

Dynamic City Search: Find weather information for any city in the world.

Automatic Geolocation: The app can automatically detect the user's location to provide local weather instantly.

Polished User Interface: A custom-designed interface with unique icons and fonts for a pleasant user experience.

Tech Stack & Implementation
This project was built from the ground up, demonstrating a full software development lifecycle.

Backend Logic: Python

Graphical User Interface (GUI): Tkinter (Python's native GUI library)

API Integration: Requests library to fetch data from the OpenWeatherMap API.

Executable Packaging: PyInstaller was used to convert the Python script into a standalone Windows executable (.exe).

Installer Creation: Inno Setup was used to create a professional, user-friendly installer for easy distribution.

Setup and Installation
There are two ways to run this application.

For Users
A ready-to-install version of the application is available.

Go to the (link-to-your-releases-page) page of this repository.

Download the Brisa_Installer.exe file.

Run the installer and follow the on-screen instructions.

(Note: You will create the "Releases" page in the final step).

For Developers
If you want to run the script from the source code:

Clone the repository: git clone https://github.com/YOUR_USERNAME/desktop-weather-app.git

Navigate to the project directory: cd desktop-weather-app

Install the required libraries: pip install -r requirements.txt

Run the application: python src/brisa.py
