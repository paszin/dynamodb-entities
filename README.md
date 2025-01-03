# dynamodb-single-table-entities

This repository contains helpers and guidance for a basic structure when designing a dynamodb single table.

## In a nutshell:

Design your database according to the best practices of single table design. Use _dynamodb-single-table-entities_ as a framework to structure your code and implement your queries to efficiently work with DynamoDB.

Highlights:
- simple definitions of attributes and compound keys
- generators for quick code scaffolding (e.g. from NoSQL Workbench export)
- 100% flexibility, from low level code to out of the box




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


## Implementation

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



