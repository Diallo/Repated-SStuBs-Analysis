import json

'''
With filtered list of hashes, get timestamps and print min + max.
'''
def get_hash_timestamps(filteredBucketHashList):
    print('')
    print(' *** Printing min, max timestamps *** ')
    with open('testTimestamps.json') as json_file:
        data = json.load(json_file)
        filteredHashTimestamps = []
        for y in filteredBucketHashList:
            print('')
            print('Bucket Hash: {}'.format(y))

            for i, entry in enumerate(data):  # attempt to grab all timestamps where json has this hash value

                hash = data[i]['bucketHash']
                time = data[i]['testTime']
                if hash == y:
                    filteredHashTimestamps.append(time)

            print('Earliest Timestamp: ' + min(filteredHashTimestamps))
            print('Latest Timestamp: ' + max(filteredHashTimestamps))
            filteredHashTimestamps.clear()

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

with open('test.json') as json_file:
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

    get_hash_timestamps(filteredBucketHashList)

# TODO: Check time interval for each bucket
# TODO: Check distribution












