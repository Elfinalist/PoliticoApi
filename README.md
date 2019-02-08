
[![Build Status](https://travis-ci.org/Elfinalist/PoliticoApi.svg?branch=develop)](https://travis-ci.org/Elfinalist/PoliticoApi) [![Coverage Status](https://coveralls.io/repos/github/Elfinalist/PoliticoApi/badge.svg?branch=develop)](https://coveralls.io/github/Elfinalist/PoliticoApi?branch=develop)

# Politico API

A flask powered voting api

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The apps core dependency is python, to get that up and running:

#### Mac OS
Assuming you've already setup homebrew:
```
brew install python
```

#### Windows
here's a guide to help you get started with python on windows
```
https://www.howtogeek.com/197947/how-to-install-python-on-windows/
```

### Installing

All app dependencies are captured in `requirements.txt` and once you have python up and running execute the following:

```
git clone https://github.com/Elfinalist/PoliticoApi.git
cd PoliticoAPI
pip install -r requirements.txt
```


### Running the app
To start the api server, while still in the app directory run:
```
python app.py
```

### Running the tests

To run the tests and confirm all is well, run:

```
pytest
```

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used


## Authors

* **Elvis Wanjohi** - (https://github.com/Elfinalist)

