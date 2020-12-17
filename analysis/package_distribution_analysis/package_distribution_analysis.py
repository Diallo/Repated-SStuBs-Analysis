def analyse_packages_project_level(grouped_sstubs):
    projects_to_package_details = {}
    for project, buckets_to_sstubs in grouped_sstubs.items():
        buckets_package_details = get_buckets_to_package_details(buckets_to_sstubs)
        same_package_buckets_share = get_share_of_buckets_with_all_sstubs_in_same_package(buckets_package_details)

        # Metrics we decided not to use:
        # avg_share_of_most_common_package = get_avg_share_of_most_common_package(buckets_package_details)
        # avg_distance_across_buckets = get_avg_distance_across_buckets(buckets_package_details)

        project_details = {
            'buckets_amount': len(buckets_to_sstubs.keys()),
            'sstubs_amount': len([sstub for sstubs in buckets_to_sstubs.values() for sstub in sstubs]),
            'shares_of_buckets_with_all_sstubs_in_same_package': same_package_buckets_share,
            # 'avg_share_of_most_common_package': avg_share_of_most_common_package,
            # 'avg_distance_across_buckets': avg_distance_across_buckets
        }

        projects_to_package_details[project] = project_details

    return projects_to_package_details


def analyse_packages_per_buckets(grouped_sstubs):
    results = {}
    for project_name, buckets_to_sstubs in grouped_sstubs.items():
        buckets_package_details = get_buckets_to_package_details(buckets_to_sstubs)
        results[project_name] = buckets_package_details
    return results


def get_buckets_to_package_details(buckets_to_sstubs):
    buckets_package_details = {}
    for bucket, sstubs_list in buckets_to_sstubs.items():
        sstub_paths = [sstub['bugFilePath'] for sstub in sstubs_list]
        package_paths = [get_parent_folder_path(path) for path in sstub_paths]
        packages_to_sstub_counts = get_paths_to_counts(package_paths)
        max_package_sstubs_share = get_shares_of_most_common_package(sstub_paths, packages_to_sstub_counts)

        buckets_package_details[bucket] = {
            # 'sstubs': sstubs_list, #commented out to reduce output size for Jupyter
            'packages_to_sstub_counts': packages_to_sstub_counts,
            'max_package_sstubs_share': max_package_sstubs_share
        }

    return buckets_package_details


def get_shares_of_most_common_package(sstub_paths, packages_to_sstub_counts):
    sstubs_total = len(sstub_paths)
    share_of_bugs_in_most_common_package = get_share_of_bugs_in_most_common_package(packages_to_sstub_counts,
                                                                                    sstubs_total)
    return share_of_bugs_in_most_common_package


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


def get_share_of_buckets_with_all_sstubs_in_same_package(buckets_to_package_details):
    single_package_buckets = get_single_package_buckets_count(buckets_to_package_details)
    buckets_total = len(buckets_to_package_details.keys())
    return single_package_buckets / buckets_total


def get_single_package_buckets_count(buckets_to_package_details):
    # returns amount of buckets where all sstubs are in same package
    count = 0
    for bucket_id, package_details in buckets_to_package_details.items():
        is_all_sstubs_in_one_package = package_details['max_package_sstubs_share'] == 1
        if is_all_sstubs_in_one_package:
            count += 1
    return count

# ---------------- functions for unused metrics below --------------------------


# # not used
# def get_avg_share_of_most_common_package(lsh_buckets):
#     biggest_share_per_buckets = get_shares_of_most_common_package_per_bucket(lsh_buckets)
#     return get_average(biggest_share_per_buckets)
#
#
# # not used
# def get_avg_distances_of_all_buckets(lsh_buckets):
#     # distance between files can only by calculated if min 2 file paths are given
#     avg_distances_of_buckets = [get_avg_distance_of_files_in_bucket(bucket['whole_paths'])
#                                 for bucket in lsh_buckets.values() if len(bucket['whole_paths']) >= 2]
#     return avg_distances_of_buckets
#
#
# # not used
# def get_avg_distance_across_buckets(lsh_buckets):
#     avg_distances_of_buckets = get_avg_distances_of_all_buckets(lsh_buckets)
#     if not avg_distances_of_buckets:
#         # if all buckets of a project contain only 1 sstub, the list will be empty and no average can be calculated
#         return None
#     return get_average(avg_distances_of_buckets)
#
#
# # not used
# def get_avg_distance_of_files_in_bucket(file_paths):
#     '''
#     gets all possible pairs between the given paths and calculates the distance between the files of each pair.
#     Returns the average distance.
#     '''
#     if len(file_paths) < 2:
#         raise Exception('At least 2 file paths must be given to calculate the distance')
#
#     all_path_pairs = list(itertools.combinations(file_paths, 2))
#     all_pairs_distances = [get_distance_between_files(pair[0], pair[1]) for pair in all_path_pairs]
#     return get_average(all_pairs_distances)
#
#
# # not used
# def get_distance_between_files(path_a, path_b):
#     '''
#     distance between any 2 files is counted in steps that are necessary from file a to file b.
#     One step is a change from one directory to its parent or child.
#
#     Examples:
#     If 2 paths are identical, the distance is 0.
#     If 2 paths belong to folders that have the same parent folder, the distance is 2:
#     1 step from file a to the common parent, then 1 step from the common parent to file b
#
#     For any 2 files within a bucket a distance can be calculated, as they are part of the same project
#     and therefore have at least the project directory in common.
#     '''
#     if path_a == path_b:
#         return 0
#
#     folders_a = path_a.split('/')
#     folders_b = path_b.split('/')
#     for i in range(len(folders_a)):
#         if not folders_a[i] == folders_b[i]:
#             # if trees are first different at i, that means at i-1 there was the lowest common parent folder
#             index_of_first_different_folder = i
#             remaining_steps_to_a = folders_a[index_of_first_different_folder:]
#             remaining_steps_to_b = folders_b[index_of_first_different_folder:]
#             steps_from_a_to_b = len(remaining_steps_to_a + remaining_steps_to_b)
#             return steps_from_a_to_b
