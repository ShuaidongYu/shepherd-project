# Table of contents
* [General information](#General-information)
* [Setup](#setup)
* [Usage](#usage)
## General information
This project is called "SHEPHERD-PROJECT" and it bascially consists of 4 folders and 1 application.
It is written mainly in Python 3.6.5 and Flask framework is used to build the API.

* "core" folder is a package folder, which contains the core modules to be imported in our flask application.
* "dat" folder contains the original "herd.xml" file and output files in .json and .db format. The JSON files contain the information of the stock and herd while the DB file stores all the unfulfilled orders.
* "templates" folder contains all html files that are used to generate some informaiton on the webpage.
* "tests" folder contains 2 tests separately for the class instantiation and our flask application.
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