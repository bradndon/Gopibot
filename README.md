# Gopibot

A hipchat bot to help you find food trucks in Bellevue

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:bradndon/Gopibot.git
$ cd Gopibot

$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```

## Required Environment Variables

DEVELOPER_KEY: A google developer key that has access to the sheets api

HIPCHAT_URL: A url given by hipchat for a integration to work from

## Endpoints

/trucks: List all trucks in Bellevue for today according to google sheet

/recommend: Get a recommendation of where to eat from Gopibot

/about: Learn about Gopibot

To use these with hipchat I made them slash commands named respectively after
their endpoints.
