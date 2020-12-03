import json
import requests

ENDPOINT = "https://api.github.com/repos/{}/commits/{}"


with open('data/original_data.json') as json_file:
    data = json.load(json_file)
    for i,entry in enumerate(data):
        print("{}/{}".format(i,len(data)))
        fixSHA = entry['fixCommitSHA1']
        parentSHA = entry["fixCommitParentSHA1"]
        repositoryName = entry["projectName"].replace(".","/")
        header = {'Accept': 'application/vnd.github.cloak-preview'}
        
        
        resp = requests.get(ENDPOINT.format(repositoryName,parentSHA)).json()
        resp2 = requests.get(ENDPOINT.format(repositoryName,fixSHA)).json()


        # TODO COMMIT AUTHOR OR COMMITER
       
        print(resp)
        data[i]['parentTime'] = resp['commit']['author']['date']
        data[i]['fixTime'] = resp['commit']['author']['date']

    with open('data/new_data.json', 'w+') as new_file:
        json.dump(data, new_file)
     