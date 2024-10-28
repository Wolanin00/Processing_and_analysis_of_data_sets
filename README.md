# Processing and analysis of large data sets

Project for completing the course "Przetwarzanie i analiza dużych zbiorów danych"

## Project preview

<h3>Live: https://processing-and-analysis-of-data-sets.vercel.app/  </h3>

```diff
-After click wait some time (10 second) to deploy app.
```

## Table Relationships

### `Owner` Table
- **Columns**: `id`, `name`, `surname`, `age`, `email`
- **Relationships**:
  - One (`Owner`) to many (`FranchiseLocation`)
  - Relationship: `locations` - an owner can have multiple franchise locations.

### `FranchiseType` Table
- **Columns**: `id`, `name`, `description`
- **Relationships**:
  - One (`FranchiseType`) to many (`FranchiseLocation`)
  - Relationship: `locations` - a franchise type can have multiple locations.
  - One (`FranchiseType`) to many (`Dish`)
  - Relationship: `dishes` - a franchise type can have multiple dishes assigned to it.

### `Dish` Table
- **Columns**: `id`, `name`, `description`, `price`, `franchise_type_id`
- **Relationships**:
  - Many (`Dish`) to one (`FranchiseType`)
  - Relationship: `franchise_type` - each dish belongs to a specific franchise type.

### `FranchiseLocation` Table
- **Columns**: `id`, `address`, `city`, `owner_id`, `franchise_type_id`
- **Relationships**:
  - Many (`FranchiseLocation`) to one (`Owner`)
  - Relationship: `owner` - each location is associated with an owner.
  - Many (`FranchiseLocation`) to one (`FranchiseType`)
  - Relationship: `franchise_type` - each location belongs to a specific franchise type.

## Relationship Diagram

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
