import json
import requests

ENDPOINT = "https://api.github.com/search/commits?q=hash:{}"


with open('data/original_data.json') as json_file:
    data = json.load(json_file)
    for i,entry in enumerate(data):
        print("{}/{}".format(i,len(data)))
        fixSHA = entry['fixCommitSHA1']
        parentSHA = entry["fixCommitParentSHA1"]
        repositoryName = entry["projectName"].replace(".","/")
        header = {'Accept': 'application/vnd.github.cloak-preview'}
        
        
        resp = (requests.get(ENDPOINT.format(parentSHA),headers=header).json())
        resp2 = (requests.get(ENDPOINT.format(fixSHA),headers=header).json())


        # TODO COMMIT AUTHOR OR COMMITER
        print(resp)
        for result in resp['items']:
            if result['repository']['full_name'] == repositoryName:
                data[i]['parentTime'] = result['commit']['author']['date']
                break
        
        for result in resp2['items']:
            if result['repository']['full_name'] == repositoryName:
                data[i]['fixTime'] = result['commit']['author']['date']

                break
