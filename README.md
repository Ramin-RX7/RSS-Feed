# RSS Feed Django Project
`RSS-Feed` is Parser/API written in Django and compatible with multiple RSS feed schemas.


## Build With
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=802d2d&labelColor=2c2c2c)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![ElasticSearch](https://img.shields.io/badge/-ElasticSearch-005571?style=for-the-badge&logo=elasticsearch)
![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Minio](https://img.shields.io/badge/Minio-c72c48.svg?style=for-the-badge&logo=minio&logoColor=white)



## Table of Contents
- [RSS Feed Django Project](#rss-feed-django-project)
  - [Build With](#build-with)
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
    - [What does it do?](#what-does-it-do)
    - [Related apps](#related-apps)
    - [Upcoming updates](#upcoming-updates)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Setup and Deploy steps](#setup-and-deploy-steps)
  - [Contributing](#contributing)
  - [Licence](#licence)



## About the Project

This project is a web application built with `Django Rest Framework` for content aggregation from RSS Feeds. This README file will guide you through the setup process, provide instructions for running the project, and explain how to contribute to its development.

### What does it do?
This project is designed to parse different types of RSS feeds and save them in the database (postgresql by default).

> Although this project is desinged based on podcast rss feeds but the code is highly extendable and can be easily converted to a project for another category of feeds. Also the parser itself does not need any changes since it automatically fills the database.

Different types of rss feeds can be easily added from django admin panel. All podcasts are automatically checked for updates (default to every 15 minutes) using celery-beat.

This project also uses jwt as the main authentication for users. Users must login with their username/password and will be given access/refresh token to be used as the login method after that. Their tokens will be saved in cache (default to Redis) and in each request needing authentication, the tokens will be checked. Some actions that require jwt authentication are `like`, `subscribe`, `comment`. Users can also see their active sessions and logout from each one they want. In the case that user forgot their password they can reset it via email.

Users can see the podcast (RSS) details, items and can also have some social interactions such as liking items, subscribing to feeds, and commenting on items. They can set notification for updates of their favorite feeds so they'll get a notification (default to Email) to be notified on updates.

This project uses elastic search to save the logs of most events happening on the server. Every api call, authentication actions by user, podcast update actions will be stored in elastic search database. The logs follow acceptable logging practices to have an easy to use logging mechanism (specially through Kibana).

Also Since `nginx`, `gunicorn` and `minio` are used, the project is complete to be deployed on any server.
> Even though everything is implemented, you may need to consider separating different consumers defined in `src/consumers.py` into multiple docker-compose services to have better performance

This project is intended to only be used as an API, it does not include a frontend server on it's own but can be easily connected to one by adding the server to docker-compose services (You may also want to nginx ports)


### Related apps

Althoug this project can be considered a complete project, I have also managed to make 3 microservices out of it that can interact with it.

The idea in these microservices is that `RSS-Feed` be only used to save podcast details and their corressponding episodes and our microservices be in charge of other actions.

So beside this project, we have:

- [Authorization](https://github.com/Ramin-RX7/RSS-MS-Authorization) which is responsible for authentication and autherization of users.
- [Accounts](https://github.com/Ramin-RX7/RSS-MS-Accounts) which is responsible for account of users and all interactions of users.
- [Podcasts](https://github.com/Ramin-RX7/RSS-MS-Podcasts) which is responsible for providing external API for podcasts.

> It worth mentioning that these microservices are written FastAPI and use MongoDB for database.


### Upcoming updates
- Playlists (listen later)
- Complete notification handler
- Faster rss adding using celery workers
- Less usage of word `podcast` to make the code even more extendable.
- Tests
- API rate limit for users (if project is intended to be only an API, not a complete project with frontend server)



## Setup

### Prerequisites
Before setting up the RSS Feed Django project, ensure that you have the following prerequisites installed on your machine:

- Python
- Docker (and docker-compose)


### Setup and Deploy steps
Follow these steps to set up the project:


**1. Clone the repository using Git:**

```
git clone https://github.com/Ramin-RX7/RSS-Feed.git
```


**2. Setup `.env` file**

inside `src` directory create a `.env` file with variable structure similar to `.env.dist` file.


Congratulations! The RSS Feed Django project has been successfully set up on your machine.

**3. Run the docker compose file**
```
docker compose -f "docker-compose.yml" up -d --build
```



## Contributing

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

Now make any changes you want.

Finally create a pull request and mention all the changes of your branch.



## Licence

`RSS-Feed` is maintained under `GNU General Public License v3.0` license (read more [here](/LICENSE))
