# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
from .preproces import info_by_payment, info_by_plate, info_by_waiter


url = 'https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json'



def inicio(request):
    context = {}
    req = requests.get(url).json()
    req = info_by_plate(req)
    context['req'] = req
    return render(request, 'inicio.html', context)

def waiters(request):
    context = {'results': []}
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
        for zone in req[waiter]['zone']:
            new_waiter['zone'].append([zone, req[waiter]['zone'][zone]['qty'],int(req[waiter]['zone'][zone]['total'])])
        context['results'].append(new_waiter)
    print(context)

    return render(request, 'waiters.html', context)
# Create your views here.
