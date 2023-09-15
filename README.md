[![Django][django.js]][django-url]
[![Django Rest Framework][Django Rest Framework.js]][Django Rest Framework-url]


# RSS Feed Django Project
`RSS-Feed` is Parser/API written in Django and compatible with multiple RSS feed schemas.


## Table of Contents
- [RSS Feed Django Project](#rss-feed-django-project)
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
  - [Licence](#licence)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Project](#running-the-project)
    - [Contributing](#contributing)



## About the Project
This project is a web application built with `Django Rest Framework` for content aggregation from RSS Feeds. This README file will guide you through the setup process, provide instructions for running the project, and explain how to contribute to its development.


## Licence
`RSS-Feed` is maintained under MIT license (read more [here](/LICENSE))



## Setup

### Prerequisites
Before setting up the RSS Feed Django project, ensure that you have the following prerequisites installed on your machine:

- Python
- Django


### Installation
Follow these steps to set up the project:

Clone the repository using Git:

```bash
git clone https://github.com/Ramin-RX7/RSS-Feed.git
```
Change into the project directory:
```bash
cd RSS-Feed/src
```
Create a virtual environment (optional but recommended):
```bash
python -m virtualenv .venv
```

Activate the virtual environment:

```bash
.\.venv\Scripts\activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Set up the database:

```bash
python manage.py migrate
```
This will apply the database migrations and create the necessary tables.

Create a superuser account (admin):

```bash
python manage.py createsuperuser
```
Follow the prompts to set a phone number and password for the admin account.

Congratulations! The RSS Feed Django project has been successfully set up on your machine.


### Running the Project
To run the RSS Feed Django project, follow these steps:

Activate the virtual environment (if not already activated):

For Windows:

```bash
env\Scripts\activate
```
For macOS/Linux:

```bash
source env/bin/activate
```
Start the server:

```bash
python manage.py runserver
```


### Contributing
We welcome contributions to the `RSS-Feed` Django project.
We use git-flow branching methods to contribute to `RSS-Feed`
If you'd like to contribute, please follow these steps:

Fork the repository on GitHub.

Clone your forked repository to your local machine:

```bash
git clone https://github.com/Ramin-RX7/RSS-Feed.git
```
Create a new branch for your changes:


```bash
git checkout -b feature/your-feature-name
```
