
# Table Relationships 


## Customers → Orders

 `customers.customer_id` has 99,441 unique values.
 `orders.customer_id` has 99,441 unique values.
 Every `orders.customer_id` exists in `customers.customer_id`.
 `orders` contains 99,441 rows.
 Therefore, each customer appears exactly once in `orders`.
 Observed relationship: 1:1

---

## Orders → Order Items

 Every `order_items.order_id` exists in `orders.order_id`.
 `order_items` has 98,666 unique orders.
 `orders` has 99,441 orders.
 Therefore, 775 orders have no corresponding order-item record.
 Repeated `order_id`s in `order_items` show that an order can contain multiple items.
 Observed relationship: 1:many

---

## Order Items → Products

 `order_items.product_id` has 32,951 unique values.
 `products` has 32,951 rows.
 Every `order_items.product_id` exists in `products.product_id`.
 Therefore, there are no invalid product references from `order_items`.

---

## Order Items → Sellers

 Every `order_items.seller_id` exists in `sellers.seller_id`.
 Repeated seller IDs in `order_items` indicate that a seller can be associated with multiple order items.

---

## Orders → Payments

 Every `order_payments.order_id` exists in `orders.order_id`.
 `order_id` is repeated in payments (4,446 repeated rows).
 Therefore, some orders have multiple payment records.
 Observed relationship: 1:many

---

## Orders → Reviews

 Every `order_reviews.order_id` exists in `orders.order_id`.
 `order_id` is repeated in reviews (551 repeated rows).
 Therefore, some orders have multiple review records.
 Observed relationship: 1:many

---

## Products → Category Translation

 13 product rows have categories that don't appear in the translation table.
 These 13 rows belong to 2 unique categories:

   `portateis_cozinha_e_preparadores_de_alimentos` → 10 rows
   `pc_gamer` → 3 rows
 These categories currently have no corresponding English translation.

 ---

### Products → Order Items

- Every `product_id` in `order_items` exists in `products`.
- All 32,951 products in `products` appear at least once in `order_items`.
- `product_id` is repeated in `order_items` (79,699 repeated rows).
- Therefore, one product can appear in multiple order-item records.
- Relationship observed: 1:many.

---
#### MISSING ORDER
- Missing order dates were investigated against `order_status`.
- Most missing dates are consistent with the order's lifecycle/status and should remain `NaT`.
- 24 orders have `order_status = delivered` but at least one expected date is missing.
- These missing values are retained rather than imputed because the original values cannot be reliably reconstructed.

---
### MISSING PRODUCT INFORMATION
- 611 product rows contain at least one missing value.
- All 611 of these products appear in `order_items`.
- These products account for 1,604 order-item records.
- Therefore, these rows should not be dropped without further consideration because they are referenced by actual orders.
- The 2 products with missing physical dimensions appear in actual orders.
- One appears in 17 order-item records and the other appears in 1 record.
- Their physical measurements cannot be reliably reconstructed from the available data.
- Missing physical dimensions will therefore be retained rather than arbitrarily imputed or causing the products to be removed.





### For payment_type:
<!-- 
3 records have payment_type = 'not_defined' and payment_value = 0.0. These appear to represent orders where no payment method/value was recorded. The value is retained because the actual payment type cannot be reliably inferred. -->

<!-- 2 payment records have credit_card as the payment type and a positive payment value, but payment_installments = 0 and payment_sequential = 2. These are source-data anomalies. No correction was applied because the correct installment count cannot be reliably determined. -->

<!-- Item Total vs Payment Total: Compared the total order amount (price + freight_value) from order_items with the total payment_value from order_payments for each order_id. Initially found 19,737 mismatches due largely to floating-point precision. After rounding differences to 2 decimal places, 576 orders showed genuine differences. Sample investigation confirmed that these differences are not necessarily data errors, so no corrections were made. -->


### FOR SELLER TABLE

Seller ZIP prefixes: 1,027 values appeared as 4 digits because the ZIP-prefix column was stored numerically, causing leading zeros to be omitted. Standardized the column to 5-character strings using zero-padding (zfill(5)). No records were removed.

The correct data type to store ZIP codes or postal codes is a string or text data type because storing it as int will remove the intial 0, eg 011123 becomes 11123, simillarly zip codes in UK, Canada also have alphabets, some places it also have - etc


### Orders without order-item records
------------------
775 orders in the orders table have no corresponding
records in order_items.

603 → unavailable
164 → canceled
5   → created
2   → invoiced
1   → shipped

These records are retained because they represent valid
order records and may be relevant to order-status analysis.
They will naturally be excluded from item-level analysis
because no order-item records exist for them.



### Why create three delivery features?

Although `delivery_delay_days`, `is_delivered_late`, and `delivery_status` are based on the same delivery information, they serve different analytical purposes:

* **`delivery_delay_days`** → gives the exact numerical difference between actual and estimated delivery, useful for measuring *how early or late* an order was.
* **`is_delivered_late`** → converts this into a simple binary indicator (`0/1/NaN`), making it easy to calculate late-delivery rates and use in statistical analysis.
* **`delivery_status`** → provides a human-readable category such as `delivered_early`, `delivered_on_time`, `delivered_late`, or `not_delivered`, which is more useful for business reporting and visualizations.

Thus, they contain related information but provide **different levels of detail and usability** rather than being redundant.


<!-- Seller-level features were created using seller_id to capture seller volume and performance. seller_item_count measures total items handled, seller_order_count measures distinct orders, and seller_total_sales measures total item value. Seller-level validation identified 3,095 sellers and showed a strongly right-skewed distribution, with a small number of high-volume sellers contributing substantially more orders and sales. -->



freight_percentage was created to measure shipping cost relative to product price. Extremely high values were observed for low-priced products where freight charges substantially exceeded the item price. These values were validated as mathematically correct and were retained as they may provide useful insights into shipping-cost inefficiency.