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

```

# Sample: Highscore Application

In this example we model a simple highscore. We assume that we have a little online game like pinball for single players. Each game is recorded, users should be able to see their most recent plays and also their best plays. Furthermore, there is a global highscore.


## 1) Queries 

We start by modelling the queries that we need for our system:

- As a player I want to record the date and score of each play.
- As a player I want to see my 5 most recent results. (most recent dates)
- As a player I want to see my top 5 results. (highest points)
- As a player I want to know how many times I've played the game.
- As a user I want to see the the global top 10 results. (highest points)

## 2) Datastructure

We take every single querying and design a suitable datastructure.
For each query we pick a suitable partition key (PK), sort key (SK)

_As a player I want to record the date and score of each play._

PK = username, SK = irrelevant, DATA = {date, points}

_As a player I want to see my 5 (or more) most recent results. (most recent dates)_

PK = username, SK = date, DATA = {date, points}

_As a player I want to see my top 5 results. (highest points)_

PK = username, SK = score, DATA = {date, points}

_As a player I want to know how many times I've played the game._

PK = username, SK = statistics DATA = {totalPlays}

_As a user I want to see the the global top 10 results. (highest points)_

PK = ALL SCORE RESULTS, SK = score, DATA = {points, username}


Takeaway: Most of the quries are bound to a user. Therefore username is a good choice for the partition key (PK). There are use cases where results are sorted either by points or by date. Therefore we introduce a sort key for date and one for points: `DATE#YYYY-MM-DD HH:mm:ss` and `SCORE#00POINTS`. To maintain some statistics we introduce a sort key `"STATS"` that keeps the total number of plays and any other details we might want to save. The global high score is independent from each user, therefore we introduce a global secondary index (GSI_1) with the same sortkey (SK). We combine each scoring result with the GSI_1.

The derived output will be called entities.

- Entity 1: PlayScore (PK = {username}, SK = SCORE#{points}, GSI_1 = "SCORE")
- Entity 2: PlayDate (PK = {username}, SK = DATE#{date})
- Entity 3: UserStats (PK = {username}, SK = "STATS")

Example:

PK = "paszin", SK = "DATE#2024-12-12T14:36:22+00:00", DATA = {points: 512}
PK = "paszin", SK = "SCORE#000512", DATA = {points: 512}, GSI_1 = "SCORE"
PK = "paszin", SK = "STATS", DATA = {playCount: 1}


Discussion: each match


PK: USERNAME
SK: POINTS#points | DATE#timestamp | Stats

GSI_1: SCORE (konstant)
SK: POINTS#points

Queries:

- overall highscore: gsi1, sort by sk
- personal highscore: pk=user and sk begins with points desc 
- personal last 10 matches pk = user and sk begins with DATE desc
- personal statistics
- enter result of new play: increase stats, add points, add date
- personal number of matches during the last 30 days



