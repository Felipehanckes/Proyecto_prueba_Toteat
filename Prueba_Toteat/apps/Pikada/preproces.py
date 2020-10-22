import datetime

########### NOT USED #################

'''Functions made before realizing that most recent date is 
    from over a month ago '''
def get_date_filter(option=None):
    ''' Option attribute is setted to None and
    could be changed, the meaning of the value
    of option is:
        0: Last 7 days
        1: Last 30 days
        None: Historic data
    '''
    back_date = {0: 7, 1: 30}
    if option != None:
        time_ago = datetime.date.today() - datetime.timedelta(days=back_date[option])
        print('time ago es: {}'.format(time_ago))
    return time_ago

def convert_to_date(date_string):
    '''Convert a string with form "YYYY-MM-DD hh:mm:ss" to it's
    datetime.date form'''
    date_string = date_string.split(' ')
    date_list = date_string[0].split('-')
    date_list = [int(x) for x in date_list]
    date = datetime.date(date_list[0], date_list[1], date_list[2])
    print('date is {}'.format(date))
    return date

def get_shift(date_string):
    date_string = date_string.split(' ')
    date = date_string[0]
    time = date_string[1].split(':')
    if int(time[0]) >= 15:
        shift = 'morning'
    else:
        shift = 'afternoon'
    return [date, shift]
#########################################


def info_by_waiter(json_data, date_filter=None):
    waiters = dict()
    for order in json_data:
        date = get_shift(order['date_closed'])
        if order['waiter'] in waiters:
            waiters[order['waiter']]['shift'][date[1]].add(date[0])
            waiters[order['waiter']]['selling_amount'] += order['total']
            waiters[order['waiter']]['orders_served'] += 1
            if order['zone'] in waiters[order['waiter']]['zone']:
                waiters[order['waiter']]['zone'][order['zone']]['qty'] += 1
                waiters[order['waiter']]['zone'][order['zone']]['total'] += order['total']
            else:
                waiters[order['waiter']]['zone'][order['zone']] = {'qty': 1, 'total': order['total']}
                
        else:
            waiters[order['waiter']] = {
                'shift': {'morning': set(), 'afternoon': set()},
                'selling_amount': order['total'],
                'orders_served': 1,
                'zone': {},
                'tables': {}
            }
            waiters[order['waiter']]['zone'][order['zone']] = {'qty': 1, 'total': order['total']}
            waiters[order['waiter']]['shift'][date[1]].add(date[0])
    return waiters


def info_by_plate(json_data, date_filter=None):
    '''return a summary by plate type '''
    information = dict()
    for order in json_data:
        products_ordered = []
        for product in order['products']:
            if product['category'] in information:
                if product['name'] in information[product['category']]:
                    if product['name'] in products_ordered:
                        information[product['category']][product['name']]['serving_number'] += 1
                    else:    
                        information[product['category']][product['name']]['serving_number'] += 1
                        information[product['category']][product['name']]['order_cuantity'] += 1
                else:
                    information[product['category']][product['name']] = {
                        'serving_number': 1,
                        'order_cuantity': 1,
                    }
            else:
                information[product['category']] = {
                    product['name']: {
                        'serving_number': 1,
                        'order_cuantity': 1,
                    }}
            products_ordered.append(product['name'])
    print(information)
    return information
                
            

def info_by_payment(json_data, date_filter=None):
    payments = dict()
    max_date = get_date_filter(date_filter)
    print('max_date es: {}'.format(max_date))
    for order in json_data:
        if date_filter == None:
            for pay in order['payments']:
                print(pay)
                if pay['type'] in payments:
                    payments[pay['type']] += pay['amount']
                else:
                    payments[pay['type']] = pay['amount']
        else:
            date = convert_to_date(order['date_opened'])
            if max_date <= date:
                for pay in order['payments']:
                    if pay['type'] in payments:
                        payments[pay['type']] += pay['amount']
                    else:
                        payments[pay['type']] = pay['amount']
    return payments        
