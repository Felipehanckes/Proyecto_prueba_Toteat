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
    '''
    Just retrieve data from waiters.
    '''
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

def info_by_cashier(json_data):
    cashier = dict()
    for order in json_data:
        date = get_shift(order['date_closed'])
        if order['cashier'] in cashier:
            cashier[order['cashier']]['shift'][date[1]].add(date[0])
            cashier[order['cashier']]['selling_amount'] += order['total']
        else:    
            cashier[order['cashier']] = {
                'shift': {'morning': set(), 'afternoon': set()},
                'selling_amount': order['total'],
            }
    return cashier

def info_by_plate(json_data, date_filter=None):
    '''
    Just retrieve data from plates and products.
    '''
    information = dict()
    for order in json_data:
        products_ordered = []
        for product in order['products']:
            if product['category'] in information:
                if product['name'] in information[product['category']]:
                    if product['name'] in products_ordered:
                        information[product['category']][product['name']]['serving_number'] += 1
                        information[product['category']][product['name']]['total'] += product['price']
                    else:    
                        information[product['category']][product['name']]['serving_number'] += 1
                        information[product['category']][product['name']]['order_cuantity'] += 1
                        information[product['category']][product['name']]['total'] += product['price']

                else:
                    information[product['category']][product['name']] = {
                        'serving_number': 1,
                        'order_cuantity': 1,
                        'total': product['price'],
                        'price': product['price']
                    }
            else:
                information[product['category']] = {
                    product['name']: {
                        'serving_number': 1,
                        'order_cuantity': 1,
                        'total': product['price'],
                        'price': product['price']
                    }}
            products_ordered.append(product['name'])
    print(information)
    return information

def general_information(json_data, date_filter=None):
    '''
    Just retrieve data from plates and products.
    '''
    general = dict()
    general['table'] = {}
    general['payments'] = {}
    for order in json_data:
        if order['table'] in general['table']:
            general['table'][order['table']]['average'].append(order['diners'])
            general['table'][order['table']]['amount'].append(order['total'])
        else:
            general['table'][order['table']] = {
                'average': [],
                'amount': []
            }
        for payment in order['payments']:
            if payment['type'] in general['payments']:
                general['payments'][payment['type']]['total'] += payment['amount']
                if order['zone'] in general['payments'][payment['type']]['zone']:
                    general['payments'][payment['type']]['zone'][order['zone']] += payment['amount']
                else:
                    general['payments'][payment['type']]['zone'][order['zone']] = payment['amount']
            else:
                general['payments'][payment['type']] = {
                    'total': payment['amount'],
                    'zone': {}
                }
    print(general)
    return general        

def format_number(number):
    rework = False  
    str_number = str(number)
    if ','  '.' in str_number:
        rework = True
        num_parts = str_number.split(',').split('.')
        str_number = number[0]
    else:
        str_number = str(number)
    length = len(str_number)
    decomposition = ''
    for i in range(length):
        if i % 3 == 0 and i != 0:
            print('i es {}, y i%3 es: {}'.format(i, i%3))
            decomposition  = str_number[length - 1 - i] + '.' + decomposition
        else:
            decomposition = str_number[length - 1 - i] + decomposition
    if rework == True:
        decomposition = decomposition + ',' + str(num_parts[1])
    return decomposition

def format_float(number):
    str_number = str(number).replace('.', ',')
    return str_number