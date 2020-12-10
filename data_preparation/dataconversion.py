import json
import requests

ENDPOINT = "https://api.github.com/repos/{}/commits/{}"
SECRETTOKEN = "some-github-token"

with open('../../data/original_data.json') as json_file:
    data = json.load(json_file)
    for i,entry in enumerate(data):
        if i < 14571 or i > 17178:
            
            continue
        

        print("{}/{}".format(i,len(data)))
        fixSHA = entry['fixCommitSHA1']
        parentSHA = entry["fixCommitParentSHA1"]
        repositoryName = entry["projectName"].replace(".","/")
        header = {'Accept': 'application/vnd.github.cloak-preview',
        'Authorization': "token {}".format(SECRETTOKEN)}
        
        

        resp = requests.get(ENDPOINT.format(repositoryName,fixSHA),headers=header).json()
       

        try:
            data[i]['fixTime'] = resp['commit']['author']['date']
        except:
            #  have to recontinue from here
            print(i)
            break


    with open('data/lastone.json', 'a+') as new_file:
        json.dump(data, new_file)
     