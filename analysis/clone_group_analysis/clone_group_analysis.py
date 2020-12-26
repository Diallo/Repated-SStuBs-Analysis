import constants
import re

def exclude_sstubs_with_letters(grouped_sstubs):
    '''
    :param grouped_sstubs: sstubs grouped by project as defined in the data_preparation module
    :return: grouped sstubs where the sourceBeforeFix is purely composed of digits
    '''
    filtered_grouped_sstubs = {}
    for project, project_clone_groups in grouped_sstubs.items():
        filtered_project_clone_groups = {}
        for bucket_hash, sstubs_for_hash in project_clone_groups.items():
            filtered_sstubs_for_hash = list(filter(lambda sstub: re.match(r"\d+", sstub[constants.SOURCE_BEFORE_FIX_KEY]), sstubs_for_hash))
            if len(filtered_sstubs_for_hash) > 0:
                filtered_project_clone_groups[bucket_hash] = filtered_sstubs_for_hash
        if len(filtered_project_clone_groups) > 0:
            filtered_grouped_sstubs[project] = filtered_project_clone_groups
    return filtered_grouped_sstubs

def classify_clone_groups_by_size(grouped_sstubs):
    '''
    :param grouped_sstubs: sstubs grouped by project as defined in the data_preparation module
    :return: a dict of clone_group_size to clone groups. 
    e.g. {1: {"projectA-hash": [{sstub_data}]}} shows that the clone group 'projectA-hash' contains 1 sstub
    '''
    size_to_clone_group_map = {}
    for project, project_clone_groups in grouped_sstubs.items():
        for bucket_hash, sstubs_for_hash in project_clone_groups.items():
            clone_group_size = len(sstubs_for_hash)
            project_and_bucket_hash = project + "-" + bucket_hash
            if clone_group_size in size_to_clone_group_map:
                size_to_clone_group_map[clone_group_size][project_and_bucket_hash] = sstubs_for_hash
            else:
                size_to_clone_group_map[clone_group_size] = {project_and_bucket_hash: sstubs_for_hash}
    return size_to_clone_group_map

