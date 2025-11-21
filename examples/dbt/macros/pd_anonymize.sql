{% macro pd_anonymize_phone(column) %}
  {{ pd_mask_tail(column, keep=4) }}
{% endmacro %}

{% macro pd_anonymize_email(column) %}
  {{ pd_mask_tail(column, keep=3) }}
{% endmacro %}
