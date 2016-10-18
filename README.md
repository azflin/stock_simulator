# Stock Simulator
World's simplest and fastest stock simulator. Build portfolios and trade securities in real time powered by Yahoo Finance.  Back end is a fully RESTful API built with Django Rest Framework. Currently hosted at [acerag.pythonanywhere.com](https://acerag.pythonanywhere.com).

## Installation
1) git clone https://github.com/azflin/stock_simulator

2) pip install -r requirements.txt (Create a virtual environment first)

3) bower install

4) python manage.py migrate

Run "python manage.py runserver" to begin!

## API Usage

__/api/register/__  
* POST: Create a user. Payload must contain "username", "password", and optionally "email".  

__/api/login/__  
* POST: Login a user. Payload must contain "username" and "password".  

__/api/quote/\<tickers\>/__  
* GET: Get pricing quote info on a list of stock tickers. \<tickers\> is a comma delimited list of tickers.  

__/api/portfolios/__  
* GET: Get all portfolios. If a "username" query parameter is passed, then get that user's portfolios.  
* POST: Create a portfolio. Must be authenticated. JSON payload must contain "name".  

__/api/portfolios/\<portfolio_id\>/__  
* GET: Get one portfolio.  
* PUT: Edit a portfolio (can only edit name). Must be authenticated as owner of portfolio.  
* DELETE: Delete a portfolio. Must be authenticated as owner of portfolio.  

__/api/portfolios/\<portfolio_id\>/transactions/__  
* GET: Get list of portfolio's transactions.  
* POST: Create a transaction. Must be authenticated. JSON payload must contain:  
 * "ticker": Ticker of security you want to transact.  
 * "quantity": Number of units you want to transact.  
 * "transaction_type": Either "Buy" or "Sell"  

__/api/portfolios/\<portfolio_id\>/stocks/__  
* GET: Get portfolio's stock holdings.  

__/api/users/__  
* GET: Get all users.  

## Tests
Only tests for basic back end transactions are written.

```
python manage.py test
```
