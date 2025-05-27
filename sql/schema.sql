-- SQL schema for market data table
CREATE TABLE market_data (
  id SERIAL PRIMARY KEY,
  symbol TEXT,
  price FLOAT,
  timestamp TIMESTAMP
);
