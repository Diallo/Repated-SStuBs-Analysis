from analysis.package_distribution_analysis.package_distribution_analysis import analyse_packages_project_level, \
    analyse_packages_per_buckets
from analysis.time_distribution_analysis.time_analysis_main import get_projects_to_bucket_details, \
    analyse_time_project_level
from data_preparation.data_grouping import load_grouped_filtered_sstubs


class AnalysisFacade:
    def __init__(self):
        self.grouped_filtered_sstubs = load_grouped_filtered_sstubs()

    # use this for visualization & investigation
    def combine_project_data(self):
        '''
        :return: dict with all data on project aggregation level,
        plus 'buckets' key under which to find all buckets level calculated data,
        as well as all sstubs given for that bucket.
        '''
        time_analysis_data = self.get_time_analysis_project_aggregation()
        package_analysis_data = self.get_package_analysis_project_aggregation()

        combined_data = {}
        for project_name in package_analysis_data.keys():
            combined_data[project_name] = {}
            time_analysis_for_project = time_analysis_data[project_name]
            package_analysis_for_project = package_analysis_data[project_name]
            combined_bucket_data = {**time_analysis_for_project, **package_analysis_for_project}
            combined_bucket_data['buckets'] = self.combine_bucket_details(project_name)
            combined_data[project_name] = combined_bucket_data
        return combined_data

    def combine_bucket_details(self, project_name):
        project_to_sstubs = {project_name: self.grouped_filtered_sstubs[project_name]}
        package_analysis = self.get_package_analysis_per_bucket(project_to_sstubs)
        time_analysis = self.get_time_analysis_per_bucket(project_to_sstubs)
        combined_bucket_details = {}
        for bucket_id in time_analysis[project_name].keys():
            combined_bucket_details[bucket_id] = {**package_analysis[project_name][bucket_id],
                                                  **time_analysis[project_name][bucket_id]}
        return combined_bucket_details

    def get_time_analysis_project_aggregation(self):
        return analyse_time_project_level(self.grouped_filtered_sstubs)

    def get_package_analysis_project_aggregation(self):
        return analyse_packages_project_level(self.grouped_filtered_sstubs)

    def get_time_analysis_per_bucket(self, grouped_sstubs):
        return get_projects_to_bucket_details(grouped_sstubs)

    def get_package_analysis_per_bucket(self, grouped_sstubs):
        return analyse_packages_per_buckets(grouped_sstubs)
