{% macro pd_hash(column, salt) %}
    md5(concat({{ salt }}, ':', {{ column }}))
{% endmacro %}

{% macro pd_mask_tail(column, keep=4) %}
    regexp_replace({{ column }}, '.(?=.{' ~ keep ~ '})', '*')
{% endmacro %}

{% macro pd_nullify(column) %}
    NULL
{% endmacro %}
