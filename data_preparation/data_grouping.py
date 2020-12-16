import copy
import json

from constants import BUCKET_HASH_KEY, PROJECT_NAME_KEY


# use this for analysis
def load_grouped_filtered_sstubs():
    with open('./data/grouped_sstubs.json') as json_file:
        grouped_sstubs = json.load(json_file)
        return exclude_buckets_with_single_sstubs(grouped_sstubs)


def exclude_buckets_with_single_sstubs(grouped_sstubs):
    filtered_projects_sstubs = copy.deepcopy(grouped_sstubs)
    for project_name, buckets in grouped_sstubs.items():

        # remove buckets that contain only 1 sstub
        for bucket_id, sstubs_of_bucket in buckets.items():
            is_single_sstub_in_bucket = len(sstubs_of_bucket) == 1
            if is_single_sstub_in_bucket:
                filtered_projects_sstubs[project_name].pop(bucket_id)

        # remove projects that don't contain any buckets anymore
        if filtered_projects_sstubs[project_name] == {}:
            filtered_projects_sstubs.pop(project_name)

    return filtered_projects_sstubs


def get_grouped_sstubs():
    '''
    :return: dict like {'projectName123': {'buckethash1234567': ['stub1infodict',
                                                                 'stub2infodict',
                                                                 'stub3infodict']
                                          },
                        'projectName234': {'buckethash1234567': ['stub4infodict',
                                                                 'stub5infodict']
                                          },
                        }
            where 'sstub[i]infodict' is the complete dict of a sstub as provided by the raw data
    '''

    with open('./data/sstubs-0104-bucket-hash.json') as json_file:
        data = json.load(json_file)

    grouped_sstubs = {}
    for sstub in data:
        project_name = sstub[PROJECT_NAME_KEY]
        bucket_hash = sstub[BUCKET_HASH_KEY]

        # add project to grouped_sstubs
        is_project_already_in_dict = project_name in grouped_sstubs.keys()
        if not is_project_already_in_dict:
            grouped_sstubs[project_name] = {}

        # add bucket to project
        is_bucket_already_in_dict = bucket_hash in grouped_sstubs[project_name].keys()
        if not is_bucket_already_in_dict:
            grouped_sstubs[project_name][bucket_hash] = []

        # add sstub to bucket
        grouped_sstubs[project_name][bucket_hash].append(sstub)

    filtered_grouped_sstubs = exclude_buckets_with_single_sstubs(grouped_sstubs)
    with open('./data/grouped_sstubs.json', 'w+') as new_file:
        json.dump(filtered_grouped_sstubs, new_file)
