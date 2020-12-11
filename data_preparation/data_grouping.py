import json

from constants import BUCKET_HASH_KEY, PROJECT_NAME_KEY


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

    with open('../../data/sstubs-0104-bucket-hash.json') as json_file:
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

    with open('../../data/grouped_sstubs.json', 'w+') as new_file:
        json.dump(grouped_sstubs, new_file)

    return grouped_sstubs


def load_grouped_sstubs():
    with open('../../data/grouped_sstubs.json') as json_file:
        grouped_sstubs = json.load(json_file)
        return filter_representative_projects_sstubs(grouped_sstubs)


def filter_representative_projects_sstubs(grouped_sstubs):
    representative_threshold = 5  # Todo determine meaningful threshold
    # amount of projects per threshold: 100->75, 60->99, 50->112, 40->127, 20->177 5->295
    filtered_projects_sstubs = {}
    for project_name, buckets in grouped_sstubs.items():
        all_sstubs = [sstub for sstubs in buckets.values() for sstub in sstubs]
        if len(all_sstubs) >= representative_threshold:
            filtered_projects_sstubs[project_name] = buckets
    return filtered_projects_sstubs
