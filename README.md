# LifeTrack  
LifeTrack is a health awareness app developed in Python, featuring a Flet-based user interface and a MongoDB database.

## Requirements  
To run LifeTrack, ensure you have the following packages installed:  

```sh
pip install flet==0.26.0 googlemaps requests pymongo fastapi pydantic bcrypt cloudinary httpx urllib3 datetime uvicorn
```
## Components
To complete this application, we used Python as our programming language.

**Dependencies**

We used Flet, a Python-based library to create our user interface. We use MongoDB to store data as well as Cloudinary to store image files. 

**APIs Used**

To connect MongoDB to our Flet UI, we used FastAPI as a centralized API. To fetch data, we also used:

  Google Cloud: Places API and Air Quality API

  OpenWeather: OneCall API
  
  GNEws: News API
  
## Running the Application
To run this application, clone the **main** branch into your local directory using a terminal like **PowerShell**. Make sure you have git installed on your device before cloning.
```sh
git clone https://github.com/allendalangin/LifeTrack.git
```
This is the folder structure of LifeTrack upon cloning:
```sh
LifeTrack/
│── LifeTrack.py       # Main application file
│── api.py             # FastAPI backend
│── src/               # Source code directory
│── admin/             # Admin code directory
│── README.md          # Documentation
```
To run the LifeTrack Application, the centralized API must be initialized first.
**FastAPI Initialization** 
Execute api.py from the LifeTrack.py under the src directory.
```sh
python api.py
```

The terminal should have this output:
```sh
INFO:     Started server process [30064]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**LifeTrack App Initialization**
You can run LifeTrack by executing LifeTrack.py under the src directory.
```sh
python LifeTrack.py
```

## Features
**Login and Sign Up**

You can Authenticate a user's Username and Password

**Dashboard**

The Dashboard reflects the username and the current air quality, temperature, humidity, UV index, and wind speed.

Within the Dashboard, you can access the following: 

  **Vaccination Schedules**
  
  You can view future vaccination schedules, from the location, date, and time.
  
  **Health Resources**
  
  You can search for nearby hospitals/pharmacies, or view available hotlines of different health departments.
  
  **Statistics**
  
  You can view health statistics in the Philippines based on your chosen category.
  
  **Infographics**
  
  You can view infographics about certain diseases.
  
  **News Articles**
  
  You can view current news about health as well as reflect the news content.

