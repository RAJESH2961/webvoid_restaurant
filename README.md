# Restaurant Suggestion Website
## Project Overview
The Restaurant Suggestion Website helps users discover and review restaurants based on their location. Users can browse menus, read and write reviews, and get recommendations tailored to their preferences.

## Features
- Browse and search for restaurants
- View detailed restaurant information
- Browse menus and menu items
- Read and write reviews
- Location-based restaurants
- Responsive design for mobile and desktop

## Technologies Used
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, Fontawesome(cdn) for sociamedia-icons&Fonts
- **Database**: MYSql (for development)
- **APIs**: Nominatim OpenStreetMap API for getting user location

## Prerequisites
- Python 3.x
- Django 3.x
- pip (Python package installer)


## Installation
###### - pip install django == 5.0.6
###### - pip install mysqlclient == 2.2.4
###### - pip install pillow == 10.3.0
###### - pip install jazzmin (optional) to change UI of admin panel -> if installed Un comment INSTALLED_APPS = ['jazzmin']

## Databases
- Install a Mysql database
- create a database : 'webvoid_restaurant'
- password : '' set password if required makesure password is updated in settings.py(DATABASES={ password })
   


### 1. Clone the repository
[git clone [https://github.com/yourusername/restaurant-suggestion-website.git](https://github.com/RAJESH2961/webvoid_restaurant.git)
cd webvoid_restaurant](https://github.com/RAJESH2961/webvoid_restaurant.git) 

### How to run this project
python3 manage.py runserver **or** python manage.py runserver **or** py manage.py runserver




