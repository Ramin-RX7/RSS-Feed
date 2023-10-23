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
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Setup and Deploy steps](#setup-and-deploy-steps)
  - [Contributing](#contributing)
  - [Licence](#licence)



## About the Project
This project is a web application built with `Django Rest Framework` for content aggregation from RSS Feeds. This README file will guide you through the setup process, provide instructions for running the project, and explain how to contribute to its development.



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
`RSS-Feed` is maintained under MIT license (read more [here](/LICENSE))
