-- models/staging/stg_crypto_prices.sql

WITH source_data AS (
    -- 1. Read from the external source table we just defined in sources.yml
    SELECT * FROM {{ source('crypto_raw', 'raw_crypto_prices') }}
),

renamed AS (
    -- 2. Rename columns for clarity and cast to appropriate data types
    SELECT 
        index AS crypto_index,
        CAST(usd AS NUMERIC) AS price_usd,
        CAST(usd_24h_change AS NUMERIC) AS price_change_24h,
        CAST(fetch_timestamp AS TIMESTAMP) AS fetched_at
    FROM source_data
),

final AS (
    -- 3. Add business logic: Is the price up or down in the last 24h?
    SELECT 
        *,
        CASE 
            WHEN price_change_24h > 0 THEN TRUE 
            ELSE FALSE 
        END AS is_price_up
    FROM renamed
)

-- dbt will automatically wrap this SELECT in a CREATE VIEW
SELECT * FROM final