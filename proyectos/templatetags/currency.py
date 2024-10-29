from django import template

register = template.Library()

@register.filter
def pesos(value):
    """Format a number as Mexican pesos with thousands separator and two decimal places."""
    try:
        value = float(value)
        return f"MX$ {value:,.2f}"  # Format with thousands separator and 2 decimals
    except (ValueError, TypeError):
        return value
