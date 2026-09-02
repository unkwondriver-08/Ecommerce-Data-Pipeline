### A data pipeline is an automated flow that moves data through a series of processing steps to turn raw data into usable information.



### DATA INSPECTION Notes

## 1. Customers — `olist_customers_dataset.csv`

* Rows: **99,441**
* Columns: **5**
* Missing values: **None**
* Completely duplicated rows: **0**
* `customer_id` is unique across all 99,441 rows.
* `customer_id` connects the `customers` table to the `orders` table.

---

## 2. Geolocation — `olist_geolocation_dataset.csv`

* Rows: **1,000,163**
* Columns: **5**
* Missing values: **None**
* Completely duplicated rows: **261,831**
* Multiple records can exist for the same `geolocation_zip_code_prefix`.
* Multiple records for the same ZIP prefix are not necessarily errors because different coordinates can exist for the same ZIP prefix.
* Exact duplicate rows should be investigated before deciding whether to remove them.

---

## 3. Orders — `olist_orders_dataset.csv`

* Rows: **99,441**
* Columns: **8**
* Completely duplicated rows: **0**
* All columns are currently stored as `str`, including timestamp columns.

### Missing Values

| Column                          | Missing |
| ------------------------------- | ------: |
| `order_approved_at`             |     160 |
| `order_delivered_carrier_date`  |   1,783 |
| `order_delivered_customer_date` |   2,965 |

* Missing delivery-related dates may be legitimate depending on the order status.
* They should not automatically be filled or removed.

---

## 4. Order Items — `olist_order_items_dataset.csv`

* Rows: **112,650**
* Columns: **7**
* Missing values: **None**
* Completely duplicated rows: **0**
* `shipping_limit_date` is currently stored as `str`.
* `order_id` is repeated, meaning one order can contain multiple order-item records.
* `order_items` contains **98,666 unique orders**.
* `orders` contains **99,441 orders**.
* Therefore, **775 orders in `orders` have no corresponding record in `order_items`**.
* The reason for these 775 orders needs to be investigated later.

---

## 5. Order Payments — `olist_order_payments_dataset.csv`

* Rows: **103,886**
* Columns: **5**
* Missing values: **None**
* Completely duplicated rows: **0**
* `order_id` is repeated.
* **4,446 rows** have an `order_id` that appeared previously.
* This indicates that some orders have multiple payment records.

---

## 6. Order Reviews — `olist_order_reviews_dataset.csv`

* Rows: **99,224**
* Columns: **7**
* Completely duplicated rows: **0**

### Missing Values

| Column                   | Missing |
| ------------------------ | ------: |
| `review_comment_title`   |  87,656 |
| `review_comment_message` |  58,247 |

* Missing review text should not automatically be considered bad data.
* A review can exist without a title or detailed comment.
* `review_creation_date` and `review_answer_timestamp` are currently stored as `str`.
* `order_id` is repeated.
* **551 rows** have an `order_id` that appeared previously.
* This indicates that some orders have multiple review records.

---

## 7. Products — `olist_products_dataset.csv`

* Rows: **32,951**
* Columns: **9**
* Completely duplicated rows: **0**

### Missing Values

| Column                       | Missing |
| ---------------------------- | ------: |
| `product_category_name`      |     610 |
| `product_name_lenght`        |     610 |
| `product_description_lenght` |     610 |
| `product_photos_qty`         |     610 |
| `product_weight_g`           |       2 |
| `product_length_cm`          |       2 |
| `product_height_cm`          |       2 |
| `product_width_cm`           |       2 |

* The same **610 rows** are missing category/name/description/photo-related information.
* Only **2 rows** are missing physical product dimensions.
* These missing values need investigation before deciding how to handle them.

---

## 8. Sellers — `olist_sellers_dataset.csv`

* Rows: **3,095**
* Columns: **4**
* Missing values: **None**
* Completely duplicated rows: **0**
* `seller_zip_code_prefix` → `int64`
* Other ID/categorical columns are strings.

---

## 9. Category Translation — `product_category_name_translation.csv`

* Rows: **71**
* Columns: **2**
* Missing values: **None**
* Completely duplicated rows: **0**
* Contains the mapping between:

  * `product_category_name`
  * `product_category_name_english`


  <!-- Geolocation was not incorporated into the analytical dataset because customer and seller ZIP prefixes, cities, and states already provide sufficient geographic information for the planned analysis. Latitude/longitude data would only be required for spatial or distance-based analysis, which is outside the current scope. -->


  ### Additional Findings from Final Validation

#### 1. Missing English Category Translations

After merging `product_category_translation` into `item_analysis`, we found:

* `product_category_name` → **1,603 missing values**
* `product_category_name_english` → **1,627 missing values**

The additional **24 missing English translations** indicate that some records have a valid product category in the original category field, but that category does not have a corresponding entry in the English translation table.

Therefore, these 24 records were **not treated as data errors or removed**. The missing English category is retained as `NaN` because there is no reliable translation available in the source data.

---

#### 2. 942 Missing Reviews in `item_analysis`

The final `item_analysis` contains **942 item rows with no review information**.

This does not mean that 942 reviews are missing from the original review dataset.

Earlier, we found:

* Total orders = **99,441**
* Orders with reviews = **98,673**
* Therefore, **768 orders have no review record**

Because `item_analysis` is at the **order-item grain**, those 768 orders can correspond to more than 768 item rows. When represented at the item level, they result in **942 rows with missing review information**.

Therefore, the 942 `NaN` values in the review columns are an expected consequence of the item-level representation and indicate that **no review record was available for the corresponding order**.

These values should not be replaced with `0`, because a missing review is different from a review score of zero.
