# Django TechCrunch Scraper 
## Overview
This project is a web application built with Django, utilizing the requests and Beautiful Soup 4 (bs4) libraries for web scraping. It allows users to sign up, log in, and enter a specific Goodreads URL. The application then scrapes 
post, category, author information from the techcrunch website and store the to database and user can see them in django admin panel. 
## Features
- User authentication (sign up and login).
- Input form for entering Keyword and page num.
- Web scraping functionality to gather all information from techcrunch.
## Requirements
All required libraries are listed in the requirements.txt file. Install them using the following command: 

```
pip install -r requirements.txt
```

## Configuration 
Before running the application, you must configure your local settings. Copy sample_setting.py to local_setting.py and follow the instructions within to set up your database connection and other necessary settings. 
## Setting Up the Database
Run the following commands to set up your database: 
```
python manage.py makemigrations
```
```
python manage.py migrate
```

## Running the Application 
To start the server, run: 
```
python manage.py runserver
```

Navigate to http://127.0.0.1:8000/ in your web browser to
view the application. Users can sign up or log in from the homepage.
Once logged in, users can enter a keyword and page number to scrape information.

## Contributing
Contributions to this project are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.
