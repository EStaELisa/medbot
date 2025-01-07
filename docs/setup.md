# Docker

Docker is an open-source platform designed to help developers and system administrators build, ship, and run applications in a standardized environment called containers. A container packages an application along with its dependencies, libraries, configuration files, and other necessary components, ensuring that the application runs consistently across different computing environments.

Especially in a group project with multiple people and computers, docker ensures consistency across the different environments. Therefore, the problems arising from differences in operating systems, library versions, configurations and conflicting software versions are circumvented.

In this project is a Dockerfile that defines the base image, dependencies, and steps to build your application and a docker-compose.yml file to define and manage multi-container applications. For a consistent development setup in the IDE a devcontainer.json was configured.

To start the docker container, install docker (<https://www.docker.com/>), start it and run the command “docker-compose up”.

# Makefile

A Makefile defines a set of tasks that can be executed using the make command. Here, tests should be run automatically with pytest, linting is checked with flake8 following the python conventions and the format is checked using black.
