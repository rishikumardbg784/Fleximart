# NoSQL Analysis: Why MongoDB for FlexiMart?

## Section A: Limitations of RDBMS
The current SQL database is too rigid for our expanding catalog.
1.  **Schema Rigidity:** If we introduce "Shoes", we need to add a `size` column. This column will be NULL for all "Electronics" rows, wasting space and complicating queries.
2.  **Schema Evolution:** Adding new product types requires `ALTER TABLE` commands, which can lock the database and cause downtime.

## Section B: NoSQL Benefits
MongoDB offers a **Flexible Document Model**:
1.  **Polymorphism:** We can store a Laptop (with `ram`, `cpu`) and a Shoe (with `size`, `material`) in the same collection without altering the schema.
2.  **Embedded Reviews:** Storing reviews *inside* the product document (`reviews: [{user: "A", rating: 5}]`) allows us to fetch a product page and all its reviews in a single read operation, improving performance.

## Section C: Trade-offs
1.  **Lack of Joins:** MongoDB is not designed for complex analytics that require joining multiple collections (e.g., Sales vs Inventory vs User Logs).
2.  **Consistency:** In a distributed setup, MongoDB offers "Eventual Consistency," which might not be suitable for real-time inventory locking compared to MySQL's ACID guarantees.