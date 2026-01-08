# Database Schema Documentation

## 1. Entity-Relationship Description
* **Entity: Customers**
    * **Purpose:** Stores profile information for registered users.
    * **Attributes:** `customer_id` (PK), `email` (Unique), `first_name`, `last_name`, `phone`, `city`.
    * **Relationship:** One Customer can place MANY Orders (1:N).

* **Entity: Products**
    * **Purpose:** Catalog of items available for sale.
    * **Attributes:** `product_id` (PK), `name`, `category`, `price`, `stock`.
    * **Relationship:** One Product can appear in MANY Order Items (1:N).

## 2. Normalization Explanation (3NF)
The design adheres to **Third Normal Form (3NF)**:
1.  **1NF:** All attributes are atomic. We split `first_name` and `last_name` instead of keeping a "full_name" column.
2.  **2NF:** All non-key attributes (like `price`) depend on the full primary key (`product_id`).
3.  **3NF:** We removed transitive dependencies. For example, the `city` is stored with the Customer, not repeated in every Order record. This prevents **Update Anomalies** (if a user moves, we only update one record).

3. Sample Data
| customer_id | first_name | email             | city      |
|-------------|------------|-------------------|-----------|
| 101         | Aarav      | aarav@email.com   | Mumbai    |
| 102         | Sarah      | sarah@email.com   | Bangalore |