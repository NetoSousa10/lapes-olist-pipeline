-- Tabelas de staging na camada Silver (mesma estrutura das Bronze, mas sem constraints herdadas)

DROP TABLE IF EXISTS silver.orders_raw;
CREATE TABLE silver.orders_raw (
  LIKE bronze.orders,
  PRIMARY KEY (order_id)
);

DROP TABLE IF EXISTS silver.order_items_raw;
CREATE TABLE silver.order_items_raw (
  LIKE bronze.order_items,
  PRIMARY KEY (order_id, order_item_id)
);

DROP TABLE IF EXISTS silver.order_payments_raw;
CREATE TABLE silver.order_payments_raw (
  LIKE bronze.order_payments,
  PRIMARY KEY (order_id, payment_sequential)
);

DROP TABLE IF EXISTS silver.order_reviews_raw;
CREATE TABLE silver.order_reviews_raw (
  LIKE bronze.order_reviews,
  PRIMARY KEY (review_id)
);

DROP TABLE IF EXISTS silver.customers_raw;
CREATE TABLE silver.customers_raw (
  LIKE bronze.customers,
  PRIMARY KEY (customer_id)
);

DROP TABLE IF EXISTS silver.sellers_raw;
CREATE TABLE silver.sellers_raw (
  LIKE bronze.sellers,
  PRIMARY KEY (seller_id)
);

DROP TABLE IF EXISTS silver.products_raw;
CREATE TABLE silver.products_raw (
  LIKE bronze.products,
  PRIMARY KEY (product_id)
);

DROP TABLE IF EXISTS silver.geolocation_raw;
CREATE TABLE silver.geolocation_raw (
  LIKE bronze.geolocation,
  PRIMARY KEY (geolocation_zip_code_prefix, geolocation_lat, geolocation_lng)
);
