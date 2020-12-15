import json
import time
import datetime
start_time = time.clock()



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
                filteredHashTimestamps.append(time)

        minTime = min(filteredHashTimestamps)
        maxTime = max(filteredHashTimestamps)
        print('Earliest Timestamp: {}'.format(minTime))
        print('Latest Timestamp: {}'.format(maxTime))
        # Call new datetime function here
        # datetime.datetime.strptime(u'2014-03-06T04:38:51Z', '%Y-%m-%dT%H:%M:%SZ')
        # yourdate = datetime.datetime.strptime(u'2014-03-06T04:38:51Z', '%Y-%m-%dT%H:%M:%SZ')
        # or could just convert on the fly for these printouts with the above line ^^^
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
    print(' *** Filtered list of bucket hashes *** ')
    print(filteredBucketHashList) # Print filtered list

    get_hash_timestamps(filteredBucketHashList, data)

# TODO: Check time interval for each bucket
# TODO: Check distribution
# TODO: Create function following get_hash_timestamps. unicode times -> datetime objects. Return list of datetimes.

print('')
print("--- %s seconds ---" % (time.clock() - start_time))
print('')