# Processing and analysis of large data sets

Project for completing the course "Przetwarzanie i analiza dużych zbiorów danych"

This project manages franchise-related data for different owners, franchise types, dishes, and franchise locations using a SQLite database and a Flask web application.

## Project preview

<h3>Live: https://processing-and-analysis-of-data-sets.vercel.app/  </h3>

```diff
-After click wait some time (10 second) to deploy app.
```

## Database Schema

The database consists of four main tables: `Owner`, `FranchiseType`, `Dish`, and `FranchiseLocation`. Below is an overview of each table and their relationships.

### Tables

- **Owner**
  - Columns: `id`, `name`, `surname`, `age`, `email`
  - Relationships: 
    - One-to-Many with `FranchiseLocation` (an owner can have multiple franchise locations)

- **FranchiseType**
  - Columns: `id`, `name`, `description`
  - Relationships: 
    - One-to-Many with `FranchiseLocation` (a franchise type can have multiple locations)
    - One-to-Many with `Dish` (a franchise type can have multiple dishes)

- **Dish**
  - Columns: `id`, `name`, `description`, `price`, `franchise_type_id`
  - Relationships: 
    - Many-to-One with `FranchiseType` (each dish belongs to a specific franchise type)

- **FranchiseLocation**
  - Columns: `id`, `address`, `city`, `owner_id`, `franchise_type_id`
  - Relationships: 
    - Many-to-One with `Owner` (each location has one owner)
    - Many-to-One with `FranchiseType` (each location belongs to a specific franchise type)

### Entity-Relationship Diagram

Here's a UML-style ER diagram representing the database relationships:

```plaintext
+----------------+          +------------------+
|     Owner      |          |  FranchiseType   |
|----------------|          |------------------|
| id (PK)        |          | id (PK)          |
| name           |          | name             |
| surname        |          | description      |
| age            |          |                  |
| email          |          |                  |
+----------------+          +------------------+
         |                            |
         |                            |
        [1]                          [*]
         |                            |
         v                            |
+-------------------+                 |
| FranchiseLocation |-----------------+
|-------------------|
| id (PK)           |
| address           |
| city              |
| owner_id (FK)     |
| franchise_type_id |
+-------------------+
         |
         |
        [*]
         |
         v
+------------------------+
|          Dish          |
|------------------------|
| id (PK)                |
| name                   |
| description            |
| price                  |
| franchise_type_id (FK) |
+------------------------+
```
