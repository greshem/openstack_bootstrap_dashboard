# -*- coding:utf-8 -*-
'''
Created on 2016年9月22日

@author: greshem
'''
from dashboard.api import billing
def getPriceDiscount(region_id,account,billingItems):
    result = {}
    for billingItem in billingItems:
        url = '/billingItem/getBillingItem?billing_item=' + billingItem + '&region_id=' + region_id
        billingIt = billing.request(url)
        result[billingItem] = {'price':billingIt['billing_item']['price']}
        url = '/discount/detail/' + account['account_id'] + '?billing_item_id=' + str(billingIt['billing_item']['billing_item_id'])
        discount = billing.request(url)
        result[billingItem]['discount_ratio'] = discount['discount']['discount_ratio'] if discount['discount'] and discount['discount'].has_key('discount_ratio') else 1
    return result