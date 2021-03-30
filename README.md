# FLASK USER MANAGEMENT APP

## Create and Activate Virtual Environment

```shell
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies

```shell
pip install -r requirements.txt
```

## Database Requirement

Sqlite3 database is used for this application. Database technology can be changed before actual deployment to any other SQL database e.g PostgreSQL

## Running Note

All configuration values needed to make the application work are saved in the `.env` file. External credentials are also saved in the `.env`.

Third Party integrations in this application are:

- [Coinbase Commerce](https://commerce.coinbase.com/): This is the cryptocurrency payment gateway. All purchases made by users on the application are processed securely by Coinbase Commerce. Guide on setting up an account, product, obtaining an API and checkout ID can be [found here](https://commerce.coinbase.com/docs/)

- [SENDGRID](https://app.sendgrid.com/): This is the mailing service provider used in this application. All forms of emailing to users are handled by SENDGRID. Guide on setting up an account, obtaining an API Key and getting sender/verifying a domain can be [found here](https://sendgrid.com/docs/)

## Perform databases migration

To run application for the first time, perform database migration (creating datatables and rules) using the commands below at the root folder

- This is needed for the first time you're running the application only.

```shell
flask db init
flask db migrate
flask db upgrade
```

## Run application

```shell
export FLASK_APP=app
flask run
```

Visit [http://localhost:5000](http://localhost:5000) in your browser to continue to the application.

## Features List

- Registeration
- Login
- Account confirmation by Email
- Single Login Per Account at Once
- Logout
- Profile
- User Invitation by Email
- Payment with Cryptocurrency [BTC, USDC, ETH, LIT]
- Subscription
- Referrer Reward
