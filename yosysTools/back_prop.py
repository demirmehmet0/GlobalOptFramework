import os

equals = []
def find_equal(first):
    for equal in equals:
        if first == equal[0]:
            return equal
    return None

def get_equal(equal):
    #['t0', 'x8', 'x4']
    items = [equal[0]]
    if equal[1].startswith('t'):
        item = get_equal(find_equal(equal[1]))
        for i in item:
            items.append(i)
    else:
        items.append(equal[1])
    if equal[2].startswith('t'):
        item = get_equal(find_equal(equal[2]))
        for i in item:
            items.append(i)
    else:
        items.append(equal[2])
    return items[1:]

def start(filename):
    file = open(os.path.dirname(os.path.abspath(__file__)) + '/'+filename, 'r')

    for line in file:
        #line split by '+' and '=' and remove '\n' and ' '
        line = line.replace('\n', '')
        line = line.replace(' ', '')
        line = line.replace('\t', '')
        line = line.replace('=', ',')
        line = line.replace('+', ',')
        line = line.split(',')
        equals.append(line)
    file.close()
    '''
    t0 = x8 + x4
    t1 = x10 + t0
    t2 = x15 + x10 + x8 + x4
    t3 = x4 + x13
    t4 = x17 + x4 + x13
    '''

    calculated = []
    for equal in equals:
        item = get_equal(equal)
        arr = []
        duplicate = []
        for i in item:
            i = i.replace('x', '')
            i = int(i)
            if i in arr:
                duplicate.append(i)
                continue
            arr.append(i)
        if len(duplicate) > 0:
            #remove duplicate
            for i in duplicate:
                arr.remove(i)
        #sort arrar
        arr.sort()    
        
        calculated.append(arr)
    return calculated