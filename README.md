## This project is a application tracker system implemented with django & postgres, a very basic CRUD project, with full text search functionality.

### Steps to install:

### download project
> git clone https://github.com/May4nk/tracker.git

### keep your DB ready (postgres)
> CREATE ROLE pac WITH LOGIN PASSWORD 'pacman';
> CREATE DATABASE tracker OWNER pac;

### create virtualenv
> python3 -m venv venv

### install requirements
> python3 -r requirements.txt
