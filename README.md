# RSS Feed Django Project
`RSS-Feed` is Parser/API written in Django and compatible with multiple RSS feed schemas.


## Table of Contents
- [RSS Feed Django Project](#rss-feed-django-project)
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
