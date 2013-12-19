from django.template import Library
import re

register = Library()


# From http://gun.io/blog/a-placeholder-template-tag-for-django/
def placeholder(value, token):
    value.field.widget.attrs["placeholder"] = token
    return value

register.filter(placeholder)
