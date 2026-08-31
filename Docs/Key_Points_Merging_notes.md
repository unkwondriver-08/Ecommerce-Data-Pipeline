## Payment & Review Data Modeling

### 1. Payment Data

The `order_payments` dataset contains multiple payment records for some orders, so its grain is **one row per payment record**, not one row per order.

We checked the number of payment records per order and found that some orders have multiple payment records, with a maximum of **29 payment records for a single order**.

We also found that **2,246 orders use two different payment types**, which means selecting only the first payment record would result in loss of information.

For example, one order contained:

* Credit card → 665.41
* Voucher → 45.17
* Total → 710.58

Therefore, `order_payments` was not joined directly to the item-level dataset. Instead, it was aggregated to **one row per `order_id`**.

The following attributes were created:

| Attribute                  | Aggregation                       | Purpose                                    |
| -------------------------- | --------------------------------- | ------------------------------------------ |
| `total_payment_value`      | Sum of `payment_value`            | Total payment amount for the order         |
| `payment_types`            | Unique payment types combined     | Preserve multiple payment methods          |
| `max_payment_installments` | Maximum of `payment_installments` | Capture the highest installment count used |
| `payment_count`            | Count of payment records          | Number of payment records actually present |

We also investigated `payment_sequential`. It represents the sequence number of a payment record within an order, but it was **not used as a payment-count measure** because 80 orders had a mismatch between their maximum sequence number and the actual number of payment records.

Therefore, the actual number of payment rows was used to create `payment_count`.

The resulting `payment_summary` contains **99,440 orders and 5 columns**, including `order_id`.

---

### 2. Review Data

The `order_reviews` dataset is also not strictly one-to-one with orders. Most orders have one review, but some orders have multiple review records.

We found:

* **98,673 orders** have review records.
* The maximum number of review records for an order is **3**.
* **98,471 orders** have only one distinct review score.
* **202 orders** have two distinct review scores.
* `review_score` has no missing values.

We also investigated `review_id` and found **814 repeated occurrences**, involving **1,603 rows**. These repeated IDs can occur across different orders, so `review_id` was not treated as a unique key and duplicate review IDs were not blindly removed.

Because multiple reviews can belong to the same order, the review table was aggregated to **one row per `order_id`** before joining it to the item-level dataset.

The following attributes were created:

| Attribute          | Aggregation               | Purpose                                     |
| ------------------ | ------------------------- | ------------------------------------------- |
| `review_count`     | Count of review records   | Number of reviews associated with the order |
| `review_score_avg` | Mean of `review_score`    | Overall average review score                |
| `review_score_min` | Minimum of `review_score` | Lowest score received                       |
| `review_score_max` | Maximum of `review_score` | Highest score received                      |

For example, if an order has scores `5` and `4`:

```text
review_count      = 2
review_score_avg  = 4.5
review_score_min  = 4
review_score_max  = 5
```

This preserves information from multiple reviews without arbitrarily selecting one review.

---

### 3. Why Aggregation Was Necessary

Our analytical dataset uses the following grain:

> **One row = one order item (`order_id` + `order_item_id`)**

Both payments and reviews can contain multiple records for the same `order_id`.

Directly joining either table to `item_analysis` could therefore multiply rows and break the intended grain.

The correct approach was:

```text
Payment records
      ↓
Aggregate to order level
      ↓
One row per order
      ↓
LEFT JOIN
      ↓
Item-level analytical dataset
```

and similarly:

```text
Review records
      ↓
Aggregate to order level
      ↓
One row per order
      ↓
LEFT JOIN
      ↓
Item-level analytical dataset
```

This allows payment and review information to be added while preserving the **112,650-row item-level grain**.

### Final Result

After adding order, product, seller, payment, and review information, `item_analysis` contains:

**112,650 rows × 34 columns**

The row count remained unchanged throughout the joins, confirming that the analytical grain was preserved.
