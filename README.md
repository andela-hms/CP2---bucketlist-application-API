# CP2-bucketlist-application-API
This is an API for an online Bucket List service using Flask.

[![Humphrey Musonye](https://img.shields.io/badge/BucketList%20API-Humphrey%20Musonye-brightgreen.svg)]()

# BucketList API
A bucket list is a list of the things that you want to do before you reach a certain age, or before you die for instance: Maasai Mara is one of the few places on my bucket list.
This is a RESTful API built on the `Flask` microframework. It allows us to create, update and delate bucket lists and items that belong to them. The APi implements token-based Authentication and stores its data in a sqlite database.

## Installation
Clone this repo:
```
$ git clone https://github.com/andela-hms/CP2-bucketlist-application-API.git
```

Navigate into the app's  directory:
```
$ cd CP2-bucketlist-application-API-develop
```

Create a vitual environment:
> Use [this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to create and activate a virtual environment.

Install the required packages:
```
$ pip install -r requirements.txt
```
Set the required environment configuration key e.g:
```
export FLASK_CONFIG = 'development'
```
 *OR*

For production:

```
export FLASK_CONFIG = 'ProductionConfig'
```

Set the required environment secret key e.g. :
```
export SECRET_KEY ='some-secret-key'
```
>Create the database by running migrations as follows :

1. ```python migrate.py db init```

2. ```python migrate.py db migrate```

3. ```python migrate.py db upgrade```

>Now the project is fully set up with the database in place


## Usage

Run  
```
python migrate.py runserver
```

To test the API endpoints, use [Postman](https://www.getpostman.com/).

### API Endpoints 


| Actions        | Description           | Requires Authentication |
| ------------- |:-------------:| -------------:|
| POST /auth/login/    | Logs in a user | False |
| POST /auth/register/     | Register a new user | False |
| POST api/v1.0/bucketlists/ | Create a new bucket list   | True |
| GET api/v1.0/bucketlists/      | List all created bucket lists | True |
| GET api/v1.0/bucketlists/?q=`<query_string>`      | Search for a bucket list by name | True |
| GET api/v1.0/bucketlists/?limit=`<limit>`      | Paginates bucket list results | True |
| GET api/v1.0/bucketlists/`<bucketlist_id>`     | get single bucket list | True |
| PUT api/v1.0/bucketlists/`<bucketlist_id>` | update single bucket list | True |
| DELETE api/v1.0/bucketlists/`<bucketlist_id>`      | Delete a single bucket list | True |
| POST api/v1.0/bucketlists/`<bucketlist_id>`/items/      | Create a new item in a bucket list | True |
| PUT api/v1.0/bucketlists/`<bucketlist_id>`/items/`<item_id>` | Update an item in a bucket list | True |
| DELETE api/v1.0/bucketlists/`<bucketlist_id>`/items/`<item_id>`      | Delete an item in a bucket list | True |

- **Register a new user**

append **api/v1.0/register**  to the tail end of the link. i.e:
**http://127.0.0.1:5000/api/v1.0/register**

- Ensure the dropdown to the left of the URL bar is a POST request

- In the body tab on Postman, enter a username and password in JSON format i.e:

```
{
    "username" : "new_user",
    "email" : "new_user@email.com",
    "password" : "new_user_pass"
}
```

A `successful` registeration should return the new user's username, i.e.

```
{"message":"Registration successful"}
```

- **Login User**

This time the link changes to:
**http://127.0.0.1:5000/api/v1.0/auth/login**

- Ensure the request method is POST.

```
{"email":"new_user@email.com", "password":"new_user_pass"}
```

A successful login should return an authentication token i.e:

```
{
    'message': 'Login Successful',
    'auth_token': "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4NjM4NTM2MiwiaWF0IjoxNDg2MzgxNzYyfQ.eyJpZCI6MX0.OOnheGKkPzVB3ounLZiOIhUbT6l3DVSlxkcPBk3E_Dc"
}
```
Copy the token to be used for Authentication.

- **Create a bucketlist**

This project utilizes **Token Based Authentication** to restrict access to certain resources. Absence of the token header on calls to resources will result in **401: Unauthorized Access** error.

To create a bucketlist, make a **POST** request to this URI:
**http://127.0.0.1:5000/api/v1.0/bucketlists/**

Go to the Authorization tab then to the "type" dropdown option, select Basic Auth and add your token in the username field.

Give your Bucketlist a name and hit send, i.e:

```
{
"bucketlist_name": "Beaches and Holiday Homes"
}
```

A successful request will return the bucket list you just created:

```
{
"bucketlist_name": "Beaches and Holiday Homes"
}
```

To view bucketlists make a **GET** request to the bucketlist URI with the bucketlist_id appended:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/**.


- **Update or Delete a bucketlist**

To **UPDATE** a bucketlist ping the following URL:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/** with the **PUT** method.

In the body tab, provide your information as follows:

```
{
    "bucketlist_name": "Beaches in Kenya"
}
```
A successful update should return the renamed bucketlist and status code `200`.

- **Creating a bucket list item**

To create a bucketlist item ping the following URL:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/** with **POST** request method.

>1 is the bucketlist_id you want to add items to.

Add your content:

```
{
    "item_name": "Swimming in the Indian Ocean",
    "done" : "False"
}
```
A successful POST request should return the following:

```
{
    "item_id" : 1,
    "item_name": "Swimming in the Indian Ocean",
    "created_by" : 1,
    "date_created": "Mon, 10 Apr 2017 04:58:13 -0000",
    "date_modified": "Mon, 10 Apr 2017 04:58:13 -0000",
    "bucketlist_id" : 1,
    "done": False   
}
```

- **Updating a bucket list item**

To update an item pass the bucketlist id and item id and on the body tab pass the info to be updated:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1/**

```
{
    "item_name": "Attend Malindi Festival",
}
```

To **DELETE** a bucketlist item ping the following URL:

**http://127.0.0.1:5000/api/v1.0/bucketlists/1/items/1/** with the method for the URL as **DELETE**.

A successful request should return a HTTP `200` status code.

- **Paginantion and Search**
Result are paginated based on the `limit` number specified.

To filter results to a given criteria use:

**http://127.0.0.1:5000/api/v1.0/bucketlists/?limit=10**

Search using the **q** parameter:

**http://127.0.0.1:5000/api/v1.0/bucketlists/?q=beaches**


# TESTS

To run tests on the API endpoints use the following command:

```
nosetests --with-coverage
```



