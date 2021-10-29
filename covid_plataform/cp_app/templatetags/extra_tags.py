from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
@register.filter
def get_nesteditem(dictionary, key, key2):
    return dictionary.get(key.get(key2))
@register.filter
def to_str(value):
    """converts int to string"""
    return str(value)
