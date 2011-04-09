# -*- coding: utf-8 -*-
"""
    helpers
    ~~~~~~~~

    Shop Application Helpers

"""

import logging

def extract_ids_from_product_list(products=None):
    if products is None:
        return []
    ids = []
    for item in products:
        ids.append(item['product_id'])
    return ids

def make_list_from_string(string=None):
    
    if string is None:
        return []
    return eval(string)

def calculate_total_price(products=None):
    
    if products is None:
        return 0
    total = 0
    price = 0
    quantity = 0
    subtotal = 0
    
    for item in products:
        price = float(item['product_price'])
        quantity = float(item['product_quantity'])
        subtotal = quantity / 250 * price
        total += subtotal
    
    return total

def make_list_from_dict(products=None):
    
    items = []
    
    for product in products:
        items.append(
            str({
                'product_id': str(product['product_id']),
                'product_quantity': str(product['product_quantity']),
            })
        )
    
    return items