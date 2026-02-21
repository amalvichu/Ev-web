# Evon - Web Application

This repository contains the source code for Evon, a web application built with Django.

## About The Project

Evon is a web application that appears to manage users, and potentially has features related to payments and student data.

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

*   Python 3.x
*   MySQL

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/amalvichu/Ev-web.git
    ```
2.  Install Python packages. I noticed that `Django` and a MySQL driver like `mysqlclient` are not in your `requirements.txt`. You may need to install them manually.
    ```sh
    pip install -r requirements.txt
    pip install Django mysqlclient
    ```
3.  Set up your MySQL database. Create a database named `evon_db` and update the credentials in `Evon/settings.py` if needed.
4.  Apply database migrations
    ```sh
    python manage.py migrate
    ```
5.  Run the development server
    ```sh
    python manage.py runserver
    ```

## Technologies Used

*   Django
*   Python
*   MySQL
*   HTML
*   CSS
*   JavaScript