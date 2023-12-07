# Microservices docs

This project also includes multiple microservices that can act as stand-alone apps. These microservices are each maintained in their own corresponding repository.

- [Accounts](https://github.com/Ramin-RX7/RSS-MS-Accounts): Responsible for user account interactions
- [Authorization](https://github.com/Ramin-RX7/RSS-MS-Authorization): Responsible for user authentication and authorization
- [Podcasts](https://github.com/Ramin-RX7/RSS-MS-Podcasts): Responsible for Podcast related actions


All of these microservices include a dockerfile which makes them ready to deploy, however here, we have also maintained a [docker-compose file](https://github.com/Ramin-RX7/RSS-Feed/tree/develop/docs) to run all of them together. This docker-compose also contains `Redis` and `MongoDB` images.


In order to run all microservices through that `docker-compose.yml`:

1. You need to place all of these services directories beside the compose file.
2. Run `docker compose up -d --build`

> Note that all of these microservices have their own `.env` file and you need to have them all.
