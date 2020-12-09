import itertools

from package_distribution_analyser.mock_sstubs_data import sstubs


def get_lsh_hashes_to_package_details(sstubs):
    hash_key = 'bucketHash'
    all_hashes = set([sstub[hash_key] for sstub in sstubs])
    hashes_to_sstubs = {}
    for lsh_hash in all_hashes:
        sstub_paths = [sstub['bugFilePath'] for sstub in sstubs if sstub[hash_key] == lsh_hash]
        package_paths = [get_parent_folder_path(path) for path in sstub_paths]
        packages_to_sstub_counts = get_paths_to_counts(package_paths)
        hashes_to_sstubs[lsh_hash] = {'whole_paths': sstub_paths,
                                      'package_paths': package_paths,
                                      'packages_to_sstub_counts': packages_to_sstub_counts,
                                      }
    return hashes_to_sstubs


def get_share_of_bugs_in_most_common_package(packages_to_sstub_counts, sstubs_with_hash_amount):
    count_of_most_affected_package = max(packages_to_sstub_counts.values())
    return count_of_most_affected_package / sstubs_with_hash_amount


def get_paths_to_counts(paths: list):
    unique_paths = set(paths)
    paths_to_counts = {}
    for unique_path in unique_paths:
        count = len([path for path in paths if path == unique_path])
        paths_to_counts[unique_path] = count

    return paths_to_counts


def get_parent_folder_path(path):
    path_parts = path.split('/')
    package_path_parts = path_parts[:-1]
    package_path = '/'.join(package_path_parts)
    return package_path


def avg_share_of_most_common_package(lsh_buckets):
    biggest_share_per_buckets = get_shares_of_most_common_package_per_bucket(lsh_buckets)
    return get_average(biggest_share_per_buckets)


def get_average(values_list):
    return sum(values_list) / len(values_list)


def get_share_of_buckets_with_all_sstubs_in_same_package(lsh_buckets):
    biggest_share_per_buckets = get_shares_of_most_common_package_per_bucket(lsh_buckets)
    buckets_total = len(lsh_buckets.values())
    buckets_with_all_sstubs_in_one_package = len([share for share in biggest_share_per_buckets if share == 1])
    return buckets_with_all_sstubs_in_one_package / buckets_total


def get_shares_of_most_common_package_per_bucket(lsh_buckets):
    shares_of_most_common_package_per_bucket = []
    for bucket in lsh_buckets.values():
        sstubs_total = len(bucket['whole_paths'])
        packages_to_sstub_counts = bucket['packages_to_sstub_counts']
        share_of_bugs_in_most_common_package = get_share_of_bugs_in_most_common_package(packages_to_sstub_counts,
                                                                                        sstubs_total)
        shares_of_most_common_package_per_bucket.append(share_of_bugs_in_most_common_package)

    print(shares_of_most_common_package_per_bucket)  # Todo make distribution chart
    return shares_of_most_common_package_per_bucket


def get_avg_distances_of_all_buckets(lsh_buckets):
    avg_distances_of_buckets = [get_avg_distance_of_files_in_bucket(bucket['whole_paths'])
                                for bucket in lsh_buckets.values() if len(bucket['whole_paths']) >= 2]
    print(avg_distances_of_buckets)  # TODO make distribution chart
    return avg_distances_of_buckets


def get_overall_avg_distance_across_buckets(lsh_buckets):
    avg_distances_of_buckets = get_avg_distances_of_all_buckets(lsh_buckets)
    return get_average(avg_distances_of_buckets)


def get_avg_distance_of_files_in_bucket(file_paths):
    '''
    gets all possible pairs between the given paths and calculates the distance between the files of each pair.
    Returns the average distance.
    '''
    if len(file_paths) < 2:
        raise Exception('At least 2 file paths must be given to calculate the distance')

    all_path_pairs = list(itertools.combinations(file_paths, 2))
    all_pairs_distances = [get_distance_between_files(pair[0], pair[1]) for pair in all_path_pairs]
    return get_average(all_pairs_distances)


def get_distance_between_files(path_a, path_b):
    '''
    distance between any 2 files is counted in steps that are necessary from file a to file b.
    One step is a change from one directory to its parent or child.

    Examples:
    If 2 paths are identical, the distance is 0.
    If 2 paths belong to folders that have the same parent folder, the distance is 2:
    1 step from file a to the common parent, then 1 step from the common parent to file b

    For any 2 files within a bucket a distance can be calculated, as they are part of the same project
    and therefore have at least the project directory in common.
    '''
    if path_a == path_b:
        return 0

    folders_a = path_a.split('/')
    folders_b = path_b.split('/')
    for i in range(len(folders_a)):
        if not folders_a[i] == folders_b[i]:
            # if trees are first different at i, that means at i-1 there was the lowest common parent folder
            index_of_first_different_folder = i
            remaining_steps_to_a = folders_a[index_of_first_different_folder:]
            remaining_steps_to_b = folders_b[index_of_first_different_folder:]
            steps_from_a_to_b = len(remaining_steps_to_a + remaining_steps_to_b)
            return steps_from_a_to_b


lsh_buckets = get_lsh_hashes_to_package_details(sstubs)
print('lsh_buckets:', lsh_buckets)
print('avg_share_of_most_common_package:', avg_share_of_most_common_package(lsh_buckets))
print('share_of_buckets_with_all_sstubs_in_same_package:',
      get_share_of_buckets_with_all_sstubs_in_same_package(lsh_buckets))

print('overall_avg_distance_across_buckets:', get_overall_avg_distance_across_buckets(lsh_buckets))
