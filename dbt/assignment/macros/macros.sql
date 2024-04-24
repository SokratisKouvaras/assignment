{% macro convert_flag(column) %}
   CASE
        WHEN {{ column }} = 'Y' THEN TRUE
        ELSE FALSE
    END 
{% endmacro %}