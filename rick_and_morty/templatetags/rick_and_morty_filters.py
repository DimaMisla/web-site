from django import template

register = template.Library()


@register.filter
def GET_in_text(text: str) -> str:
    return text[-1]
