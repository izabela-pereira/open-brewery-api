-- O teste falha se a tabela não tiver nenhuma linha para retornar

{% macro test_table_not_empty(model) %}
    select 
            case when count(*)= 0 then 1 
            else 0 
            end
    from {{ model }}
{% endmacro %}