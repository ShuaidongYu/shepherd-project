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
### Running "GET" requests
"GET" requests could be run on a local browser.
For example, you can get the stock and herd info at day 13 by using these 2 URLs:
```
http://127.0.0.1:5000/yak-shop/stock/13
http://127.0.0.1:5000/yak-shop/herd/13
```
After the 2 "GET" requests, the corresponding info will also be saved in "stock_info.json" and "herd_info.json".
### Running "POST" requests
"POST" requests could be run, for example, by installing "Postman" API platform.
For example, you can post the order at day 13 at this URL:
```
http://127.0.0.1:5000/yak-shop/order/13
```
After this "POST" request, the fulfilled or partially fulfilled order will be returned, while the stock amount saved in "stock_info.json" will be updated based on the consumption. The unfulfilled order will be saved into "orders.db" for other shepherds to take.
