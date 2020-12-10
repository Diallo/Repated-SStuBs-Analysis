import json
import time
from datetime import datetime, timedelta
start_time = time.clock()


def get_interval(filteredHashTimeStamps, minTime, maxTime):
    interval = (maxTime - minTime)/(len(filteredHashTimeStamps))
    return interval


'''
With filtered list of hashes, get timestamps and print min + max.
'''
def get_hash_timestamps(filteredBucketHashList, data):
    print('')
    print(' *** Printing min, max timestamps *** ')
    filteredHashTimestamps = []

    for y in filteredBucketHashList:
        print('')
        print('Bucket Hash: {}'.format(y))

        for i, entry in enumerate(data):  # attempt to grab all timestamps where json has this hash value

            hash = data[i]['bucketHash']
            time = data[i]['testTime']
            if hash == y:
                time = datetime.strptime(time, "%b %d %Y %H:%M:%S").date()
                # time = datetime.strptime(minTime, '%Y-%m-%dT%H:%M:%SZ')
                filteredHashTimestamps.append(time)

        minTime = min(filteredHashTimestamps)
        maxTime = max(filteredHashTimestamps)
        diffTime = maxTime - minTime
        print('Entry Count: {}'.format(len(filteredHashTimestamps)))
        print('Earliest Timestamp: {}'.format(minTime))
        print('Latest Timestamp: {}'.format(maxTime))
        print('Timestamp Diff (Days): {}'.format(diffTime.days))
        print('Time Interval: {}'.format(get_interval(filteredHashTimestamps, minTime, maxTime)))
        filteredHashTimestamps = []


'''
Get unique hashes from json
'''
def get_unique(bucketHashList):
    unique = []

    for hash in bucketHashList:
        if hash in unique:
            continue
        else:
            unique.append(hash)
    return unique

'''
Loop through and grab bucket hashes.
'''

with open('testTimestamps.json') as json_file:
    data = json.load(json_file)

    bucketHashList = []
    for i, entry in enumerate(data):

        bucketHash = data[i]['bucketHash']
        bucketHashList.append(bucketHash)

    print('')
    print(' *** Unfiltered list of bucket hashes *** ')
    print(bucketHashList) # Print unfiltered list
    print('')
    filteredBucketHashList = get_unique(bucketHashList)
    print(' *** Unique list of bucket hashes *** ')
    print(filteredBucketHashList) # Print filtered list

    get_hash_timestamps(filteredBucketHashList, data)


print('')
print("--- %s seconds ---" % (time.clock() - start_time))
print('')


# TODO: Check time interval for each bucket
# TODO: Check distribution
