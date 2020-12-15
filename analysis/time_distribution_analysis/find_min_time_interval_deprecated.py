import math


def find_min_time_interval(timestamps_list):
    '''
    :param timestamps_list: list of timestamps from all sstubs in bucket
    :return: shortest time interval in which at least the given percentage of time stamps is covered
    '''

    # minimum percentage of bugs that must be part of interval
    min_sstubs_percentage = 0.8

    # calculate number of timestamps that must be within interval (ceil always rounds up)
    min_timestamps_amount = int(math.ceil(timestamps_list * min_sstubs_percentage))
    sorted_timestamps = sorted(timestamps_list)

    shortest_interval = 0
    for i in range(len(timestamps_list)):
        first_timestamp_index = i
        last_timestamp_index = first_timestamp_index + min_timestamps_amount

        if last_timestamp_index >= len(sorted_timestamps):
            break

        diffTime = sorted_timestamps[last_timestamp_index] - sorted_timestamps[first_timestamp_index]
        if i == 0 or diffTime.days < shortest_interval:
            shortest_interval = diffTime.days

    return shortest_interval

# def get_shortest_intervals_per_bucket(buckets_to_sstubs):
#     buckets_to_intervals = {}
#     for bucket_id, sstubs in buckets_to_sstubs.items():
#         timestamps = []  # Todo: implement depnding on date string format
#         interval = find_min_time_interval(timestamps)
#         buckets_to_intervals[bucket_id] = interval
#
#     return buckets_to_intervals
