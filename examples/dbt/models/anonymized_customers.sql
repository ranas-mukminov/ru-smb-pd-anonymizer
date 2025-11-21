{{ config(materialized='table') }}

select
    customer_id,
    {{ pd_mask_tail('phone', keep=4) }} as phone,
    {{ pd_mask_tail('email', keep=3) }} as email,
    {{ pd_hash('fio', 'salt_placeholder') }} as fio_hash,
    city,
    age
from {{ ref('raw_customers') }}
