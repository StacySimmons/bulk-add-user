import requests
import json
import csv
from license import user_key, auth_domain, user_data


def nerdgraph_createuser(key, query):

    # US endpoint; need EU option here
    endpoint = "https://api.newrelic.com/graphql"
    headers = {'API-Key': f'{key}'}
    response = requests.post(endpoint, headers=headers, json={"query": query})

    if response.status_code == 200:
        # convert a JSON into an equivalent python dictionary
        # what's missing here is logging logic in case a user cannot be created
        # need to inspect the response for error and log the email address if there is an error
        json_dictionary = json.loads(response.content)
        print(json_dictionary)

    else:
        # raise an error with a HTTP response code
        # an error here probably indicates an API key without auth
        raise Exception(f'Nerdgraph query failed with a {response.status_code}.')


if __name__ == '__main__':
    # open a tsv file and read in the data
    # assumes data is tsv, probably need an option for csv as well
    with open(user_data) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file:
            if line[1].find('@') < 0:
                # ignore the header row, we're looking for an email address format (sort of) in the second item
                # TODO make this regex pattern match
                continue
            # for each line in the file do some stuff:
            # 1. replace query variables with data from the file
            # 2. call the API
            # 3. TODO Record success or fail, log failure emails
            query = """
                mutation {
                  userManagementCreateUser(
                    createUserOptions: {
                      authenticationDomainId: "REPLACE_AUTH_DOMAIN_ID", 
                      email: "REPLACE_EMAIL_OF_YOUR_USER", 
                      name: "REPLACE_NAME_OF_YOUR_USER", 
                      userType: REPLACE_USER_TIER}) {
                    createdUser {
                      email
                      id
                    }
                  }
                }
            """

            char_to_replace = {
                'REPLACE_AUTH_DOMAIN_ID': auth_domain,
                'REPLACE_EMAIL_OF_YOUR_USER': line[1],
                'REPLACE_NAME_OF_YOUR_USER': line[0],
                'REPLACE_USER_TIER': line[2].upper()
            }
            for key, value in char_to_replace.items():
                query = query.replace(key, value)

            # print(query)
          nerdgraph_createuser(user_key, query)
