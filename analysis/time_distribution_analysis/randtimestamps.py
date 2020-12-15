import json
import time
from random import randrange


def rand_time(s, e):
    return time.strftime('%b %d %Y %I:%M:%S', time.localtime(randrange(s, e)))

with open('test.json') as json_file:
    data = json.load(json_file)

    ''' Load each entry of json file. Input random timestamp. '''

    for i, entry in enumerate(data):
        s = time.mktime(time.strptime('Jan 1 2010  12:00:00', '%b %d %Y %I:%M:%S'))
        e = time.mktime(time.strptime('Jan 1 2020  12:00:00', '%b %d %Y %I:%M:%S'))

        data[i]['testTime'] = rand_time(s, e)

    with open('testTimestamps.json', 'w+') as new_file:
        json.dump(data, new_file)


print('')
print(' *** Random timestamps written to "testTimestamps.json" *** ')
print('')
