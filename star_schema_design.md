# Star Schema Design

## 1. Schema Overview
**Fact Table: `fact_sales`**
* **Grain:** Line Item level (one row per product in an order).
* **Measures:** `quantity_sold`, `unit_price`, `total_amount`, `discount_amount`.
* **Foreign Keys:** `date_key`, `product_key`, `customer_key`.

**Dimensions:**
* **`dim_date`:** Enriches analysis with attributes like Quarter, Month Name, Weekend Indicator.
* **`dim_product`:** Contains slowly changing attributes like Category and Product Name.
* **`dim_customer`:** Contains Customer Geography (City, State) and Segment.

## 2. Design Decisions
* **Surrogate Keys:** We use `product_key` (Internal DW ID) instead of `product_id` (Operational ID). This handles cases where a product is deleted from the source but needs to be kept in history.
* **Granularity:** Choosing "Line Item" granularity allows the most detailed slicing. If we only stored "Daily Sales," we couldn't analyze which specific customers bought which products.

## 3. Data Flow Example
**Source Transaction:** User John buys a Laptop on Jan 15.
**Warehouse Transformation:**
1.  Look up John's current record in `dim_customer` -> Key: 501.
2.  Look up Laptop in `dim_product` -> Key: 12.
3.  Convert date to Integer Key -> 20240115.
**Insert into `fact_sales`:** `{ 20240115, 501, 12, 1, $50000 }`.