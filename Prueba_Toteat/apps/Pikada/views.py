# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
from .preproces import (general_information, info_by_plate, 
info_by_waiter, format_number, format_float, info_by_cashier)


url = 'https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json'



def categories(request):
    '''
    Retrieves and format the data regards category and products 
    to be used in HTML render.
    '''
    context = {}
    req = requests.get(url).json()
    req = info_by_plate(req)
    context['results'] = []
    context['total'] = 0
    for category in req.keys():
        print(category)
        new_category = {'name': category}
        new_category['products'] = []
        new_category['total_servings'] = 0
        new_category['total_orders'] = 0
        new_category['total'] = 0
        for product in req[category]:
            new_category['total_orders'] += req[category][product]['order_cuantity']
        for product in req[category]:
            print(product)
            new_product = {}
            new_product['name'] = product
            new_product['serving_number'] = format_number(req[category][product]['serving_number'])
            new_category['total_servings'] += req[category][product]['serving_number']
            new_product['order_qty'] = format_float(float(int(round(req[category][product]['order_cuantity']/new_category['total_orders'],4)*10000)/100))
            new_product['total_sales'] = req[category][product]['total']
            new_category['total'] += req[category][product]['total']
            new_product['price'] = format_number(req[category][product]['price'])
            new_category['products'].append(new_product)
        context['total'] += new_category['total']
        new_category['total_servings'] = format_number(int(new_category['total_servings']))
        new_category['total_orders'] = format_number(int(new_category['total_orders']))
        context['results'].append(new_category)
    index = 0
    for category in context['results']:
        context['results'][index]['income_rate'] = format_float(float(int(round(category['total']/context['total'],4)*10000)/100))
        category['total'] = format_number(int(category['total']))
        index2 = 0
        for product in category['products']:
            context['results'][index]['products'][index2]['income_rate'] = format_float(float(int(round(product['total_sales']/context['total'],4)*10000)/100))
            product['total_sales'] = format_number(int(product['total_sales']))
            index2 += 1
        index += 1
    context['total'] = format_number(context['total'])
    return render(request, 'categories.html', context)

def waiters(request):
    '''
    Retrieves and format the data regards waiters
    to be used in HTML render.
    '''
    context = {'results': [], 'total': 0}
    req = requests.get(url).json()
    req = info_by_waiter(req)
    for waiter in req.keys():
        new_waiter = {'name': waiter}
        print(req[waiter]['shift']['afternoon'])
        new_waiter['double_shifts'] = len(
            [value for value in req[waiter]['shift']['morning'] if value in req[waiter]['shift']['afternoon']])
        new_waiter['morning_shifts'] = len(req[waiter]['shift']['morning']) - new_waiter['double_shifts']
        new_waiter['afternoon_shifts'] = len(req[waiter]['shift']['afternoon']) - new_waiter['double_shifts']
        new_waiter['zone'] = []
        new_waiter['total'] = 0
        for zone in req[waiter]['zone']:
            new_waiter['zone'].append([zone, format_number(
                req[waiter]['zone'][zone]['qty']),format_number(int(req[waiter]['zone'][zone]['total']))])
            new_waiter['total'] += req[waiter]['zone'][zone]['total']
            context['total'] += req[waiter]['zone'][zone]['total']
        new_waiter['total'] = format_number(int(new_waiter['total']))
        context['results'].append(new_waiter)
    context['total'] = format_number(int(context['total']))
    print(context)

    return render(request, 'waiters.html', context)
# Create your views here.

def inicio(request):
    context = {'results': []}
    req = requests.get(url).json()
    req = general_information(req)
    for table in req['table'].keys():
        print(table)
        new_table = {'name': table}
        new_table['avg_customers'] = sum(
            req['table'][table]['average'])//len(req['table'][table]['average'])
        min_repeat = req['table'][table]['average'].count(min(req['table'][table]['average']))/len(
                req['table'][table]['amount'])
        min_repeat = format_float(float(int(round(min_repeat,4)*10000)/100))
        new_table['min_customers'] = [min_repeat, min(req['table'][table]['average'])] 
        max_repeat = req['table'][table]['average'].count(max(req['table'][table]['average']))/len(
                req['table'][table]['amount'])
        max_repeat = format_float(float(int(round(max_repeat,4)*10000)/100))
        new_table['max_customers'] = [max_repeat, max(req['table'][table]['average'])]
        new_table['avg_income'] = format_number(int(sum(
            req['table'][table]['amount'])//len(req['table'][table]['amount'])))
        new_table['total_income'] = format_number(int(sum(req['table'][table]['amount'])))
        new_table['total_orders'] = len(req['table'][table]['amount'])
        context['results'].append(new_table)
    context['payments'] = []
    for pay in req['payments'].keys():
        new_pay = {
            'name': pay,
            'total': req['payments'][pay]['total'],
            'zones': []
        }
        for zone in req['payments'][pay]['zone'].keys():
            new_pay['zones'].append({'name': zone,
            'total' : format_number(int(req['payments'][pay]['zone'][zone]))})
            
        context['payments'].append(new_pay) 
    context['results'] = sorted(context['results'], key=lambda x: x['name'])
    print(context)
    return render(request, 'inicio.html', context)

def cashiers(request):
    context = {'results': []}
    req = requests.get(url).json()
    req = info_by_cashier(req)
    print(req)
    for cashier in req.keys():
        new_cashier = {'name': cashier}
        new_cashier['double_shifts'] = len(
            [value for value in req[cashier]['shift']['morning'] if value in req[cashier]['shift']['afternoon']])
        new_cashier['morning_shifts'] = len(req[cashier]['shift']['morning']) - new_cashier['double_shifts']
        new_cashier['afternoon_shifts'] = len(req[cashier]['shift']['afternoon']) - new_cashier['double_shifts']
        new_cashier['selling_amount'] = format_number(int(req[cashier]['selling_amount']))
        context['results'].append(new_cashier)
    return render(request, 'cashiers.html', context)