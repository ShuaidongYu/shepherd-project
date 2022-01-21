# Table of contents
* [General information](#General-information)
* [Setup](#setup)
* [Usage](#usage)
## General information
This project is called "SHEPHERD-PROJECT" and it bascially consists of 4 folders and 1 application.
It is writen mainly in Python 3.6.5 and Flask framework is used to build the API.

* "core" folder is a package folder, which contains the core modules to be imported in app.py.
* "dat" folder contains the original "herd.xml" file and other output files in .json or .db format.
* "templates" folder contains all html files that are used to generate some informaiton on the webpage.
* "tests" folder contains 2 tests for the class instantiation and our flask application.
* "app.py" is our flask application.
## Setup
To run this project, install the requirements.txt first:

```
pip install -r requirements.txt
```
## Usage
Run app.py at the root directory.
"GET" requests could be run on a local browser.
"POST" requests could be run, for example, by installing "Postman" API platform.