# dynamodb-entities

This repository contains helpers and guidance for a basic structure when designing a dynamodb single table.


## In a nutshell:

Design your database according to the best practices of single table design. Use _dynamodb-entities_ as a framework to structure your code and implement your queries to efficiently work with DynamoDB.

Highlights:
- simple definitions of attributes and compound keys
- generators for quick code scaffolding (e.g. from NoSQL Workbench export)
- 100% flexibility, from low level code to out of the box shortcuts, no need to learn a new syntax

# Quick Guide

1) Design your dynamodb single table (e.g. using NoSQL Workbench)
2) Convert your design into code
3) Define the queries and operations you need

## 1) Design your dynamodb single table

For designing your table follow the best practices. The result of your design should be a list of queries and a concept how to structure your partition key, sort key, and global secondary indicies. 

There are many great resources available:

The overview:
[awesome-dynamodb: A curated list by Alex de Brie of helpful resources](https://github.com/alexdebrie/awesome-dynamodb)

You prefer a video? [YouTube: Advanced data modeling with Amazon DynamoDB](https://www.youtube.com/watch?v=PVUofrFiS_A)

Or learning by example? [GitHub: aws-samples/amazon-dynamodb-design-patterns](https://github.com/aws-samples/amazon-dynamodb-design-patterns)

Tipp: Use NoSQL Workbench for modelling. Use this guide for preparing your database for the next step: [DesigningYourTable](./DesigningYourTable.md)


## 2) Convert your design into code



The library comes with a tool to convert your NoSQL Workbench export to code.

`dynamodb-entities-import -i path/to/workbenchexport.json -d /path/to/project`

`dynamodb-entities-create -d /path/to/project`

The output is a folder structure like this:

```
project-name
 ┣ entities
 ┃ ┣ _factory.py
 ┃ ┣ Entity1.py
 ┃ ┣ Entity2.py
 ┃ ┗ __init__.py
 ┣ datastore.py
 ┗ tablespecs.py
 ```

The folder `entities` contains one file per facet (if you use the NoSQL Workbench import). The file `_factory.py` contains the definitions for partition key name, sort key name, and their types. The defaults are "pk" and "sk" and both are strings (type is "S").

The file `datastore.py` is the abstraction layer for executing operations on the dynamodb table.

The file `_tablespecs.py` contains the definition of the table.



The next step is completing the code templates.

### DynamoDB Entities explained

An entity represents _a single business object_, e.g. an user, a task, an order, etc. 

Each Entity is represented as class. A minimal setup consists of the class definition and the primary key (and sort key).

```python

class MyEntity(Entity):
    
    @property
    def pk(self): # the name of the method must be the same as the attribute name of the partition key
        return "key"

```

The init function can be extended by providing specific attributes.

```python

class MyEntity(Entity):

    def __init__(self, username, **kwargs): #kwargs must be always present
        super().__init__(username=username, **kwargs)
        # same as:
        # self.username = username
        # You can also introduce additional pre processing
        self.username = username.lower()
        self.original_username = username
    
    @property
    def pk(self):
        return self.username

```

Example: a user profile.

The user profile 

```python

class UserProfile(Entity):

    def __init__(self, username, birthday, role, **kwargs): #kwargs must be always present
        super().__init__(username=username, **kwargs)
        # same as:
        # self.username = username
        # You can also introduce additional pre processing
        self.username = username.lower()
        self.original_username = username

    
    @property
    def pk(self):
        return self.username

    @property
    def sk(self):
        return "PROFILE"
    
    @property
    def gsi_1(self):
        return self.role


```


### The Datastore

The datastore is an abstraction to execute queries on the database.


```python

from dynamodbEntities import BaseDatastore

class Datastore(BaseDatastore):
    pass

# usage

import boto3

# using client and table name
client = boto3.client("dynamodb")
datastore = Datastore(client=client, table_name="my-datastore")

# using boto3 resources
ddb = boto3.resource('dynamodb')
table = ddb.Table('my-datastore')
datastore = Datastore(table=table)

# you can also provide session and endpoint_url as parameters
# all input is converted to use self.table for your operations.

```



## 3) Define the queries and operations you need

Extend the entity classes with functions to send queries to the table.

```python

from boto3.dynamodb.conditions import Key


class UserProfile(Entity):
    ...

    @classmethod
    def get_query_all_admins(cls):
        """
        return the params to query all users with the role admin
        """
        return dict(
            IndexName='gsi_1',
            KeyConditionExpression=Key('gsi_1').eq('admin'),
        )

class Datastore(BaseDatastore):
    ...

    def get_all_admins(self):

        return self.table.query(**UserProfile.get_query_all_admins())

    @add_convert_param({"UserProfile": UserProfile})
    def get_all_admins_with_conversion(self, **kwargs):
        """
        if convert = True is passed in the params, then all items are converted to UserProfile instances
        """
        return self.table.query(**UserProfile.get_query_all_admins())

```


## Samples

### Highscore Application

In this example we model a simple highscore. We assume that we have a little online game like pinball for single players. Each game is recorded, users should be able to see their most recent plays and also their best plays. Furthermore, there is a global highscore.

Read how to model and implement using dynamodb-entities including a full working sample here: [Highscore](./examples/highscore/README.md)


### Webshop

In this example we model a simple webshop. A customer can buy items and view recent orders.

Read how to model and implement using dynamodb-entities including a full working sample here: [Webshop](./examples/webshop/README.md)

### Recipe App

Future Work

### User Access Management

Future Work