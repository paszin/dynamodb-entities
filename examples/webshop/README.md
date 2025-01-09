# Sample: Simple Webshop with Customers, Items, and Orders


In this example we model a simple webshop. A customer can buy items and view recent orders.

## 1) Queries

We start by modelling the queries that we need for our system:

- As a customer I want to view all items of the shop
- As a customer I want to place an order
- As a customer I want to see my most recent orders
- As a customer I want to maintain address and payment information
- As a shop administrator I want to add items to the shop
- As a shop administrator I want to update the stock of items or edit item details
- As a shop administrator I want to see all pending orders

Limitations:
We don't consider filtering and searching of items. Let's assume it is a small webshop.

## 2) Datastructure

We take every single querying and design a suitable datastructure.
For each query we pick a suitable partition key (PK), sort key (SK)

_As a customer I want to view all items of the shop_

PK = "ITEM" SK = "<itemId>"

_As a customer I want to place an order_

PK = username, SK = "ORDER#<oderId> 

_As a customer I want to see my most recent orders_

PK = username, SK = "ORDER#<date>"

_As a customer I want to maintain address and payment information_ 

PK = username, SK = "PROFILE"

_As a shop administrator I want to add items to the shop_

PK = "ITEM", SK = "<itemId>" (To access ALL products they must be associated with static key. The partition key could be also the global secondary index. But if there is no better use for the partition key we can also use this key.)

_As a shop administrator I want to update the stock of items or edit item details_

PK = "ITEM", SK = "<itemId>"

_As a shop administrator I want to see all pending orders_

PK = <shippingStatus> (we will use a global secondary index for that)


The derived entities can be the following:

- Entity 1: Item (PK = "ITEM", SK = "<itemId>")
- Entity 2: Customer Profile (PK = username, SK = "PROFILE")
- Entity 3: Order: (PK = username, SK=ORDER#<date>#<orderId>, GSI1=<shippingStatus>)

## 3) Model your structure in NoSQLWorkbench

## 4) Convert model to dynamodb-entities code