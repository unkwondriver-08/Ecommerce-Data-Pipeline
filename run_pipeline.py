# %%
import os

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] += os.pathsep + r"C:\hadoop\bin"

print("HADOOP_HOME:", os.environ["HADOOP_HOME"])

# %%
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Olist_ETL")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .config("spark.hadoop.fs.permissions.umask-mode", "000")
    .getOrCreate()
)

print("Spark version:", spark.version)

# %%
from pathlib import Path

# Main project directory
project_path = Path(r"C:\MY ALL\Analytics Study\Project\Ecommerce Data Pipeline")

# Input and output paths
raw_path = str(project_path / "Data" / "raw")

output_path = str(
    project_path / "Data" / "analytics_ready" / "spark" / "olist_item_analysis"
)

# Logging path
log_path = str(project_path / "logs" / "validation.log")

# %%
import logging
from pathlib import Path

# Create log directory if it does not exist
Path(log_path).parent.mkdir(parents=True, exist_ok=True)

# Configure logger
logger = logging.getLogger("olist_pipeline")
logger.setLevel(logging.INFO)
logger.handlers.clear()

# Create log file
file_handler = logging.FileHandler(
    log_path,
    mode="a",
    encoding="utf-8"
)

# Define log format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False


from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    TimestampType
)


# 1. Customers
customers_schema = StructType([
    StructField("customer_id", StringType(), True),
    StructField("customer_unique_id", StringType(), True),
    StructField("customer_zip_code_prefix", StringType(), True),
    StructField("customer_city", StringType(), True),
    StructField("customer_state", StringType(), True)
])


# 2. Orders
orders_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("order_status", StringType(), True),
    StructField("order_purchase_timestamp", TimestampType(), True),
    StructField("order_approved_at", TimestampType(), True),
    StructField("order_delivered_carrier_date", TimestampType(), True),
    StructField("order_delivered_customer_date", TimestampType(), True),
    StructField("order_estimated_delivery_date", TimestampType(), True)
])


# 3. Order Items
order_items_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("order_item_id", IntegerType(), True),
    StructField("product_id", StringType(), True),
    StructField("seller_id", StringType(), True),
    StructField("shipping_limit_date", TimestampType(), True),
    StructField("price", DoubleType(), True),
    StructField("freight_value", DoubleType(), True)
])


# 4. Payments
payments_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("payment_sequential", IntegerType(), True),
    StructField("payment_type", StringType(), True),
    StructField("payment_installments", IntegerType(), True),
    StructField("payment_value", DoubleType(), True)
])


# 5. Reviews
reviews_schema = StructType([
    StructField("review_id", StringType(), True),
    StructField("order_id", StringType(), True),
    StructField("review_score", IntegerType(), True),
    StructField("review_comment_title", StringType(), True),
    StructField("review_comment_message", StringType(), True),
    StructField("review_creation_date", TimestampType(), True),
    StructField("review_answer_timestamp", TimestampType(), True)
])


# 6. Products
products_schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_category_name", StringType(), True),
    StructField("product_name_lenght", IntegerType(), True),
    StructField("product_description_lenght", IntegerType(), True),
    StructField("product_photos_qty", IntegerType(), True),
    StructField("product_weight_g", IntegerType(), True),
    StructField("product_length_cm", IntegerType(), True),
    StructField("product_height_cm", IntegerType(), True),
    StructField("product_width_cm", IntegerType(), True)
])


# 7. Sellers
sellers_schema = StructType([
    StructField("seller_id", StringType(), True),
    StructField("seller_zip_code_prefix", StringType(), True),
    StructField("seller_city", StringType(), True),
    StructField("seller_state", StringType(), True)
])


# 8. Category Translation
category_translation_schema = StructType([
    StructField("product_category_name", StringType(), True),
    StructField("product_category_name_english", StringType(), True)
])


# 9. Geolocation
geolocation_schema = StructType([
    StructField("geolocation_zip_code_prefix", StringType(), True),
    StructField("geolocation_lat", DoubleType(), True),
    StructField("geolocation_lng", DoubleType(), True),
    StructField("geolocation_city", StringType(), True),
    StructField("geolocation_state", StringType(), True)
])

# %%
def load_csv(file_path, schema, dataset_name, **read_options):
    logger.info(f"Loading dataset: {dataset_name}")

    try:
        df = (
            spark.read
            .option("header", True)
            .option("mode", "FAILFAST")
            .options(**read_options)
            .schema(schema)
            .csv(file_path)
        )

        logger.info(f"Successfully loaded dataset: {dataset_name}")
        print(f"{dataset_name}: Loading initiated successfully.")

        return df

    except Exception:
        logger.exception(f"Failed to load dataset: {dataset_name}")
        raise

# %%
dataset_configs = {
    "Customers": {
        "file": "olist_customers_dataset.csv",
        "schema": customers_schema
    },
    "Orders": {
        "file": "olist_orders_dataset.csv",
        "schema": orders_schema
    },
    "Order Items": {
        "file": "olist_order_items_dataset.csv",
        "schema": order_items_schema
    },
    "Payments": {
        "file": "olist_order_payments_dataset.csv",
        "schema": payments_schema
    },
    "Reviews": {
        "file": "olist_order_reviews_dataset.csv",
        "schema": reviews_schema,
        "options": {
            "multiLine": True,
            "quote": '"',
            "escape": '"'
        }
    },
    "Products": {
        "file": "olist_products_dataset.csv",
        "schema": products_schema
    },
    "Sellers": {
        "file": "olist_sellers_dataset.csv",
        "schema": sellers_schema
    },
    "Category Translation": {
        "file": "product_category_name_translation.csv",
        "schema": category_translation_schema
    },
    "Geolocation": {
        "file": "olist_geolocation_dataset.csv",
        "schema": geolocation_schema
    }
}

datasets = {}

for name, config in dataset_configs.items():
    file_path = f"{raw_path}/{config['file']}"

    datasets[name] = load_csv(
        file_path=file_path,
        schema=config["schema"],
        dataset_name=name,
        **config.get("options", {})
    )

# %%
customers = datasets["Customers"]
orders = datasets["Orders"]
order_items = datasets["Order Items"]
payments = datasets["Payments"]
reviews = datasets["Reviews"]
products = datasets["Products"]
sellers = datasets["Sellers"]
category_translation = datasets["Category Translation"]
geolocation = datasets["Geolocation"]

# %%
for name, df in datasets.items():
    print(f"\n========== {name} ==========")
    df.printSchema()


# %%
from pyspark.sql import functions as F
def validate_primary_key(df, table_name, key_columns):

    # Check for NULL values
    null_condition = None

    for column in key_columns:
        condition = F.col(column).isNull()
        null_condition = condition if null_condition is None else null_condition | condition

    null_count = df.filter(null_condition).count()

    # Check for duplicate keys
    duplicate_count = (
        df.groupBy(*key_columns)
          .count()
          .filter(F.col("count") > 1)
          .count()
    )

    if null_count > 0 or duplicate_count > 0:
        raise ValueError(
            f"{table_name}: Primary key validation failed. "
            f"NULL records: {null_count}, "
            f"Duplicate keys: {duplicate_count}"
        )

    print(f"{table_name}: Primary key validation passed.")

# %%
# VALIDATE PRIMARY KEYS

validate_primary_key(
    customers,
    "Customers",
    ["customer_id"]
)
validate_primary_key(orders, "Orders", ["order_id"])

validate_primary_key(
    order_items, "Order Items",
    ["order_id", "order_item_id"]
)

validate_primary_key(
    payments, "Payments",
    ["order_id", "payment_sequential"]
)


validate_primary_key(products, "Products", ["product_id"])

validate_primary_key(sellers, "Sellers", ["seller_id"])

validate_primary_key(
    category_translation,
    "Category Translation",
    ["product_category_name"]
)
validate_primary_key(reviews, "Reviews", ["review_id", "order_id"])

# %%
# %%
# 1. Orders → Customers
orphan_orders = orders.join(
    customers,
    on="customer_id",
    how="left_anti"
)

# 2. Order Items → Orders
orphan_order_items = order_items.join(
    orders,
    on="order_id",
    how="left_anti"
)

# 3. Order Items → Products
orphan_products = order_items.join(
    products,
    on="product_id",
    how="left_anti"
)

# 4. Order Items → Sellers
orphan_sellers = order_items.join(
    sellers,
    on="seller_id",
    how="left_anti"
)

# 5. Payments → Orders
orphan_payments = payments.join(
    orders,
    on="order_id",
    how="left_anti"
)

# 6. Reviews → Orders
orphan_reviews = reviews.join(
    orders,
    on="order_id",
    how="left_anti"
)

# Display validation results
fk_results = [
    ("Orders → Customers", orphan_orders),
    ("Order Items → Orders", orphan_order_items),
    ("Order Items → Products", orphan_products),
    ("Order Items → Sellers", orphan_sellers),
    ("Payments → Orders", orphan_payments),
    ("Reviews → Orders", orphan_reviews)
]

for relationship, orphan_df in fk_results:
    count = orphan_df.count()
    status = "PASSED" if count == 0 else "FAILED"

    print(
        f"{relationship}: {status} | "
        f"Orphan records: {count}"
    )

# %%
null_checks = {
    "Customers": (customers, ["customer_id", "customer_unique_id"]),
    "Orders": (orders, ["order_id", "customer_id", "order_status", "order_purchase_timestamp"]),
    "Order Items": (order_items, ["order_id", "product_id", "seller_id", "price", "freight_value"]),
    "Payments": (payments, ["order_id", "payment_sequential", "payment_type", "payment_value"]),
    "Reviews": (reviews, ["review_id", "order_id", "review_score"]),
    "Products": (products, ["product_id"]),
    "Sellers": (sellers, ["seller_id"]),
    "Category Translation": (category_translation, ["product_category_name"])
}

for table_name, (df, columns) in null_checks.items():

    null_condition = None

    for column in columns:
        condition = F.col(column).isNull()
        null_condition = condition if null_condition is None else null_condition | condition

    null_count = df.filter(null_condition).count()

    status = "PASSED" if null_count == 0 else "FAILED"

    print(f"{table_name}: {status} | NULL records: {null_count}")

# %%
value_checks = {
    "Order Items - Invalid price": (
        order_items,
        F.col("price") <= 0
    ),
    "Order Items - Invalid freight": (
        order_items,
        F.col("freight_value") < 0
    ),
    "Payments - Invalid payment value": (
        payments,
        F.col("payment_value") < 0
    ),
    "Payments - Invalid installments": (
        payments,
        F.col("payment_installments") < 0
    ),
    "Reviews - Invalid review score": (
        reviews,
        ~F.col("review_score").between(1, 5)
    ),
    "Order Items - Invalid item ID": (
        order_items,
        F.col("order_item_id") <= 0
    )
}

for check_name, (df, condition) in value_checks.items():

    invalid_count = df.filter(condition).count()

    status = "PASSED" if invalid_count == 0 else "FAILED"

    print(
        f"{check_name}: {status} | "
        f"Invalid records: {invalid_count}"
    )

# %%
date_checks = {
    "Approval before purchase": (
        F.col("order_approved_at") < F.col("order_purchase_timestamp")
    ),
    "Carrier pickup before approval": (
        F.col("order_delivered_carrier_date") < F.col("order_approved_at")
    ),
    "Customer delivery before carrier pickup": (
        F.col("order_delivered_customer_date") < F.col("order_delivered_carrier_date")
    ),
    "Customer delivery before purchase": (
        F.col("order_delivered_customer_date") < F.col("order_purchase_timestamp")
    )
}

for check_name, condition in date_checks.items():

    invalid_count = orders.filter(condition).count()

    status = "PASSED" if invalid_count == 0 else "FAILED"

    print(
        f"{check_name}: {status} | "
        f"Invalid records: {invalid_count}"
    )

# %% [markdown]
# Creation of reusable function for all the checks 

# %%
def validate_primary_key(df, table_name, key_columns):

    # Check for NULL values
    null_condition = None

    for column in key_columns:
        condition = F.col(column).isNull()
        null_condition = condition if null_condition is None else null_condition | condition

    null_count = df.filter(null_condition).count()

    # Check for duplicate keys
    duplicate_count = (
        df.groupBy(*key_columns)
          .count()
          .filter(F.col("count") > 1)
          .count()
    )

    if null_count > 0 or duplicate_count > 0:

        error_message = (
            f"{table_name}: Primary key validation failed. "
            f"NULL records: {null_count}, "
            f"Duplicate keys: {duplicate_count}"
        )

        logger.error(error_message)
        raise ValueError(error_message)

    success_message = f"{table_name}: Primary key validation passed."

    logger.info(success_message)
    print(success_message)

# %%
primary_keys = {
    "Customers": ["customer_id"],
    "Orders": ["order_id"],
    "Order Items": ["order_id", "order_item_id"],
    "Payments": ["order_id", "payment_sequential"],
    "Products": ["product_id"],
    "Sellers": ["seller_id"],
    "Category Translation": ["product_category_name"],
    "Reviews": ["review_id", "order_id"]
}

# %%
#Create the foreign-key validation function
def validate_foreign_key(child_df, parent_df, child_column, parent_column, relationship):

    orphan_count = (
        child_df.select(F.col(child_column).alias("_fk"))
        .join(
            parent_df.select(F.col(parent_column).alias("_pk")),
            F.col("_fk") == F.col("_pk"),
            "left_anti"
        )
        .count()
    )

    if orphan_count > 0:
        error_message = (
            f"{relationship}: Foreign key validation failed. "
            f"Orphan records: {orphan_count}"
        )
        logger.error(error_message)
        raise ValueError(error_message)

    success_message = f"{relationship}: Foreign key validation passed."

    logger.info(success_message)
    print(success_message)

# %%
foreign_key_checks = [
    {
        "child_df": orders,
        "parent_df": customers,
        "child_column": "customer_id",
        "parent_column": "customer_id",
        "relationship": "Orders → Customers"
    },
    {
        "child_df": order_items,
        "parent_df": orders,
        "child_column": "order_id",
        "parent_column": "order_id",
        "relationship": "Order Items → Orders"
    },
    {
        "child_df": order_items,
        "parent_df": products,
        "child_column": "product_id",
        "parent_column": "product_id",
        "relationship": "Order Items → Products"
    },
    {
        "child_df": order_items,
        "parent_df": sellers,
        "child_column": "seller_id",
        "parent_column": "seller_id",
        "relationship": "Order Items → Sellers"
    },
    {
        "child_df": payments,
        "parent_df": orders,
        "child_column": "order_id",
        "parent_column": "order_id",
        "relationship": "Payments → Orders"
    },
    {
        "child_df": reviews,
        "parent_df": orders,
        "child_column": "order_id",
        "parent_column": "order_id",
        "relationship": "Reviews → Orders"
    }
]

# %%
#Reusable not null validation function

def validate_not_null(df, table_name, required_columns):

    null_condition = None

    for column in required_columns:
        condition = F.col(column).isNull()
        null_condition = (
            condition if null_condition is None
            else null_condition | condition
        )

    null_count = df.filter(null_condition).count()

    if null_count > 0:
        error_message = (
            f"{table_name}: NULL validation failed. "
            f"NULL records: {null_count}"
        )
        logger.error(error_message)
        raise ValueError(error_message)

    success_message = f"{table_name}: NULL validation passed."

    logger.info(success_message)
    print(success_message)

# %%
#Reusable numerical validation function

def validate_values(df, check_name, condition):

    invalid_count = df.filter(condition).count()

    if invalid_count > 0:
        error_message = (
            f"{check_name}: Value validation failed. "
            f"Invalid records: {invalid_count}"
        )
        logger.error(error_message)
        raise ValueError(error_message)

    success_message = f"{check_name}: Value validation passed."

    logger.info(success_message)
    print(success_message)
    

# %%
# Validate date checks function

def validate_dates(df, check_name, condition):

    invalid_count = df.filter(condition).count()

    if invalid_count > 0:
        warning_message = (
            f"{check_name} | Anomalies: {invalid_count}"
        )
        logger.warning(warning_message)
        print(f"WARNING: {warning_message}")

    else:
        success_message = f"{check_name}: Passed."

        logger.info(success_message)
        print(success_message)

# %% [markdown]
# The central validation function

# %%
tables = {
    "Customers": customers,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Products": products,
    "Sellers": sellers,
    "Category Translation": category_translation
}

# %%
def validate_all_data():

    logger.info("========== DATA VALIDATION STARTED ==========")
    print("========== DATA VALIDATION STARTED ==========")

    try:

        # 1. Primary Key Validation
        for table_name, key_columns in primary_keys.items():
            validate_primary_key(
                tables[table_name],
                table_name,
                key_columns
            )

        # 2. Foreign Key Validation
        for check in foreign_key_checks:
            validate_foreign_key(**check)

        # 3. NULL Validation
        for table_name, (df, columns) in null_checks.items():
            validate_not_null(df, table_name, columns)

        # 4. Numerical Validation
        for check_name, (df, condition) in value_checks.items():
            validate_values(df, check_name, condition)

        # 5. Date Validation
        for check_name, condition in date_checks.items():
            validate_dates(orders, check_name, condition)

        logger.info("========== DATA VALIDATION COMPLETED ==========")
        print("========== DATA VALIDATION COMPLETED ==========")

    except Exception:
        logger.exception("DATA VALIDATION FAILED")
        raise

# %%
validate_all_data()

# %%

log_file = Path(log_path)

print("Log file exists:", log_file.exists())

print("\nLatest log entries:\n")
print(log_file.read_text(encoding="utf-8"))

# %%
from pyspark.sql.functions import col

reviews = (
    reviews
    .withColumn("review_creation_date", col("review_creation_date").cast("timestamp"))
    .withColumn("review_answer_timestamp", col("review_answer_timestamp").cast("timestamp"))
)

# %%
reviews = reviews.select("order_id", "review_score")

# %%
from pyspark.sql.functions import col

order_items = order_items.withColumn(
    "item_total",
    col("price") + col("freight_value")
)

# %%
order_items.select("item_total").show(5)

# %%
order_items = order_items.join(
    orders,
    on="order_id",
    how="left"
)

# %%
order_items.show(5)

# %%
order_items = order_items.join(
    customers,
    on="customer_id",
    how="left"
)

# %%
print(order_items.count(), len(order_items.columns))

# %%
order_items = order_items.join(
    products,
    on="product_id",
    how="left"
)

# %%
print(order_items.count(), len(order_items.columns))

# %%
order_items = order_items.join(
    sellers,
    on="seller_id",
    how="left"
)

# %%
print(order_items.count(), len(order_items.columns))

# %%
from pyspark.sql.functions import sum

payment_summary = payments.groupBy("order_id").agg(
    sum("payment_value").alias("total_payment_value")
)

# %%
from pyspark.sql.functions import collect_set, concat_ws

payment_types = payments.groupBy("order_id").agg(
    concat_ws(", ", collect_set("payment_type")).alias("payment_types")
)

# %%
payment_types.orderBy("order_id", ascending=False).show(5)

# %%
from pyspark.sql.functions import max

payment_installments = payments.groupBy("order_id").agg(
    max("payment_installments").alias("max_payment_installments")
)

# %%
from pyspark.sql.functions import sum, collect_set, concat_ws, max, count

payment_summary = payments.groupBy("order_id").agg(
    sum("payment_value").alias("total_payment_value"),
    concat_ws(", ", collect_set("payment_type")).alias("payment_types"),
    max("payment_installments").alias("max_payment_installments"),
    count("*").alias("payment_count")
)

# %%
order_items = order_items.join(
    payment_summary,
    on="order_id",
    how="left"
)
# %%
reviews = reviews.select(
    "order_id",
    col("review_score").cast("integer").alias("review_score")
)

# %%

from pyspark.sql.functions import count, avg, min, max
review_summary = reviews.groupBy("order_id").agg(
    count("*").alias("review_count"),
    avg("review_score").alias("review_score_avg"),
    min("review_score").alias("review_score_min"),
    max("review_score").alias("review_score_max")
)

# %%
order_items = order_items.join(
    review_summary,
    on="order_id",
    how="left"
)

# %%
order_items = order_items.join(
    category_translation,
    on="product_category_name",
    how="left"
)

# %%
order_summary = order_items.groupBy("order_id").agg(
    count("*").alias("order_item_count"),
    sum("item_total").alias("order_total_value"),
    sum("freight_value").alias("order_total_freight")
)

# %%
order_items = order_items.join(
    order_summary,
    on="order_id",
    how="left"
)
# %%
from pyspark.sql.functions import datediff

order_items = order_items.withColumn(
    "delivery_days",
    datediff("order_delivered_customer_date", 
            "order_purchase_timestamp")
)


# %%
order_items = order_items.withColumn(
    "estimated_delivery_days",
    datediff(
        "order_estimated_delivery_date",
        "order_purchase_timestamp"
    )
)
# %%
order_items = order_items.withColumn(
    "delivery_delay_days",
    datediff(
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    )
)

# %%
from pyspark.sql.functions import when

order_items = order_items.withColumn(
    "is_delivered_late",
    when(col("delivery_delay_days") > 0, 1).otherwise(0)
)
# %%
order_items = order_items.withColumn(
    "delivery_status",
    when(col("delivery_delay_days").isNull(), "Not Delivered")
    .when(col("delivery_delay_days") > 0, "Late")
    .when(col("delivery_delay_days") == 0, "On Time")
    .otherwise("Early")
)


# %%
from pyspark.sql.functions import countDistinct

customer_order_summary = order_items.groupBy("customer_id").agg(
    countDistinct("order_id").alias("customer_order_count")
)

# %%
customer_order_values = order_items.select(
    "customer_id",
    "order_id",
    "order_total_value"
).dropDuplicates(["customer_id", "order_id"])

customer_spend_summary = customer_order_values.groupBy("customer_id").agg(
    sum("order_total_value").alias("customer_total_spend")
)


# %%
customer_summary = customer_order_summary.join(
    customer_spend_summary,
    on="customer_id",
    how="left"
)

customer_summary = customer_summary.withColumn(
    "customer_is_repeat",
    when(col("customer_order_count") > 1, 1).otherwise(0)
)

# %%
order_items = order_items.join(
    customer_summary,
    on="customer_id",
    how="left"
)

from pyspark.sql.functions import count, countDistinct, sum, col

seller_summary = order_items.groupBy("seller_id").agg(
    count("*").alias("seller_item_count"),
    countDistinct("order_id").alias("seller_order_count"),
    sum("item_total").alias("seller_total_sales")
)

seller_summary = seller_summary.withColumn(
    "seller_avg_order_value",
    col("seller_total_sales") / col("seller_order_count")
)

order_items = order_items.join(
    seller_summary,
    on="seller_id",
    how="left"
)
# %%
order_items = order_items.withColumn(
"customer_avg_order_value",
col("customer_total_spend") / col("customer_order_count")
)

# %%
order_items = order_items.withColumn(
"freight_percentage",
(col("freight_value") / col("price")) * 100
)

# %%
from pyspark.sql.functions import year

order_items = order_items.withColumn(
"order_year",
year("order_purchase_timestamp")
)
# %%
from pyspark.sql.functions import month

order_items = order_items.withColumn(
"order_month",
month("order_purchase_timestamp")
)

# %%
final_columns = [
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id",
    "shipping_limit_date",
    "price",
    "freight_value",
    "item_total",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "seller_zip_code_prefix",
    "seller_city",
    "seller_state",
    "total_payment_value",
    "payment_types",
    "max_payment_installments",
    "payment_count",
    "review_count",
    "review_score_avg",
    "review_score_min",
    "review_score_max",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state",
    "product_category_name_english",
    "order_item_count",
    "order_total_value",
    "order_total_freight",
    "delivery_days",
    "estimated_delivery_days",
    "delivery_delay_days",
    "is_delivered_late",
    "delivery_status",
    "customer_order_count",
    "customer_total_spend",
    "customer_is_repeat",
    "seller_item_count",
    "seller_order_count",
    "seller_total_sales",
    "freight_percentage",
    "customer_avg_order_value",
    "seller_avg_order_value",
    "order_year",
    "order_month"
]

item_analysis_spark = order_items.select(final_columns)

# %%
item_analysis_spark_sorted = item_analysis_spark.orderBy(
"order_id",
"order_item_id"
)


# %%
from pyspark.sql.functions import col, sum, when

null_counts = item_analysis_spark.select([
sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
for c in item_analysis_spark.columns
])

null_counts.show(truncate=False)



# %%
item_analysis_spark.write.mode("overwrite").parquet(output_path)

print("Parquet write successful!")

# %%
parquet_check = spark.read.parquet(output_path)

print("Rows:", parquet_check.count())
print("Columns:", len(parquet_check.columns))
print("Columns match:", parquet_check.columns == final_columns)

# %%
# Write final analytical dataset
item_analysis_spark.write.mode("overwrite").parquet(output_path)

# Read back and verify
parquet_check = spark.read.parquet(output_path)

expected_rows = item_analysis_spark.count()
actual_rows = parquet_check.count()

if actual_rows == expected_rows and parquet_check.columns == final_columns:
    print("Parquet output successfully written and verified.")
    print("Rows:", actual_rows)
    print("Columns:", len(parquet_check.columns))
else:
    raise ValueError("Parquet output verification failed.")
  


