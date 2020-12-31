import copy
import json
import re

from constants import BUCKET_HASH_KEY, BUG_TYPE_KEY, PROJECT_NAME_KEY, SOURCE_BEFORE_FIX_KEY


# use this for analysis
def load_grouped_filtered_sstubs():
    with open('./data/grouped_filtered_sstubs.json') as json_file:
        grouped_sstubs = json.load(json_file)
        return grouped_sstubs


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


def exclude_sstubs_with_regex(grouped_sstubs, regex_filter):
    '''
    :param grouped_sstubs: sstubs grouped by project as defined in the data_preparation module
    :param regex_filter:
    :return: grouped sstubs where the sourceBeforeFix matches regex_filter
    '''
    grouped_filtered_sstubs = {}
    for project, project_clone_groups in grouped_sstubs.items():
        filtered_project_clone_groups = {}
        for bucket_hash, sstubs_for_hash in project_clone_groups.items():
            filtered_sstubs_for_hash = list(filter(lambda sstub: re.match(regex_filter, sstub[SOURCE_BEFORE_FIX_KEY]), sstubs_for_hash))
            if len(filtered_sstubs_for_hash) > 0:
                filtered_project_clone_groups[bucket_hash] = filtered_sstubs_for_hash
        if len(filtered_project_clone_groups) > 0:
            grouped_filtered_sstubs[project] = filtered_project_clone_groups
    return grouped_filtered_sstubs


def exclude_sstubs_with_letters(grouped_sstubs):
    '''
    :param grouped_sstubs: sstubs grouped by project as defined in the data_preparation module
    :return: grouped sstubs where the sourceBeforeFix is purely composed of digits
    '''
    return exclude_sstubs_with_regex(grouped_sstubs, r"\d+")

def exclude_sstubs_with_digits_only(grouped_sstubs):
    '''
    :param grouped_sstubs: sstubs grouped by project as defined in the data_preparation module
    :return: grouped sstubs where the sourceBeforeFix is purely composed of digits
    '''
    return exclude_sstubs_with_regex(grouped_sstubs, r"(?!^\d+$)^.+$")

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
    grouped_sstubs = load_raw_grouped_sstubs()
    with open('./data/grouped_sstubs.json', 'w+') as new_file:
        json.dump(grouped_sstubs, new_file)

def get_grouped_filtered_sstubs():
    grouped_sstubs = load_raw_grouped_sstubs()

    grouped_filtered_sstubs = exclude_buckets_with_single_sstubs(grouped_sstubs)
    grouped_filtered_sstubs = exclude_sstubs_with_digits_only(grouped_filtered_sstubs)
    
    with open('./data/grouped_filtered_sstubs.json', 'w+') as new_file:
        json.dump(grouped_filtered_sstubs, new_file)


def load_raw_grouped_sstubs():
    with open('./data/sstubs-0104-bucket-hash.json') as json_file:
        data = json.load(json_file)
        
        grouped_sstubs = {}
        for sstub in data:
            project_name = sstub[PROJECT_NAME_KEY]
            bucket_hash = f"{sstub[BUCKET_HASH_KEY]}-{sstub[BUG_TYPE_KEY]}"
            sstub[BUCKET_HASH_KEY] = bucket_hash

            # add project to grouped_sstubs
            is_project_already_in_dict = project_name in grouped_sstubs.keys()
            if not is_project_already_in_dict:
                grouped_sstubs[project_name] = {}

            # add bucket to project
            is_bucket_already_in_dict = bucket_hash in grouped_sstubs[project_name].keys()
            if not is_bucket_already_in_dict:
                grouped_sstubs[project_name][bucket_hash] = []

            # add sstub to bucket if no duplicate exists
            add_sstub_to_bucket = True
            if is_bucket_already_in_dict:
                for existing_sstub in grouped_sstubs[project_name][bucket_hash]:
                    if sstub == existing_sstub:
                        add_sstub_to_bucket = False
                        break

            if add_sstub_to_bucket:   
                grouped_sstubs[project_name][bucket_hash].append(sstub)
        
        return grouped_sstubs
