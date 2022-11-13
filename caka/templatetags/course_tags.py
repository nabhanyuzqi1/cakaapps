from django import template
import math
register = template.Library()


@register.simple_tag
def discount_calculation(price,discount):
    if price is None or price is 0:
        price = 'FREE'
        return price
    elif discount is None or discount is 0:
        return price
    sellprice = price
    sellprice = price - (price * discount/100)
    return math.floor(sellprice)