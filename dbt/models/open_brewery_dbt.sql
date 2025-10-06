select *
from {{ source('brewery', 'open_brewery_silver') }}
