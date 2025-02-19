#!/usr/bin/env python3

class Get6KForms:
    # A string that is treated as the name of this resolution.
    name = "Get Recent 6-K Forms"

    # A string that describes this resolution.
    description = "Returns Nodes 6-K Forms"

    originTypes = {'Edgar ID'}

    resultTypes = {'Form Field'}

    parameters = {'Max Results': {'description': 'Please enter the maximum number of results to return.\n'
                                                 'Returns 5 more recent by default',
                                  'type': 'String',
                                  'default': '5'}}

    def resolution(self, entityJsonList, parameters):
        import requests
        import time

        headers = {
            'User-Agent': 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        }

        linkNumbers = int(parameters['Max Results'])
        returnResults = []
        for entity in entityJsonList:
            uid = entity['uid']
            cik = entity['CIK']
            if cik.lower().startswith('cik'):
                cik = cik.split('cik')[1]
            if len(cik) != 10:
                cik = cik.zfill(10)
            print(cik)
            search_url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
            time.sleep(1)
            r = requests.get(search_url, headers=headers)
            print(r.content)
            if r.status_code != 200:
                return []

            data = r.json()
            print(data)

            forms = list(data['facts'].keys())

            for form in forms:
                keys = list(data['facts'][form].keys())
                for i in keys:
                    if 'Deprecated' not in data['facts'][form][i]['label']:
                        if list(data['facts'][form][i]['units'].keys())[0] == 'USD':
                            if linkNumbers > len(data['facts'][form][i]['units']['USD']):
                                linkNumbers = int(len(data['facts'][form][i]['units']['USD']))
                            for j in range(linkNumbers):
                                if '6-K' in data['facts'][form][i]['units']['USD'][j]['form']:
                                    value = data['facts'][form][i]['units']['USD'][::-1][j]
                                    returnResults.append([{'Field Name': '6-K: ' + i + ' ' + value['filed'],
                                                           'Account Number': value['accn'],
                                                           'Fiscal Year': value['fy'],
                                                           'Fiscal Period': value['fp'],
                                                           'Value': value['val'],
                                                           'Unit': list(data['facts'][form][i]['units'].keys())[0],
                                                           'Taxonomy': form,
                                                           'Notes': data['facts'][form][i]['label'],

                                                           'Entity Type': 'Form Field'},
                                                          {uid: {'Resolution': '6-K Field',
                                                                 'Name': 'CIK Edgar ID',
                                                                 'Notes': ''}}])

                    if list(data['facts'][form][i]['units'].keys())[0] == 'shares':
                        if linkNumbers > len(data['facts'][form][i]['units']['shares']):
                            linkNumbers = int(len(data['facts'][form][i]['units']['shares']))
                        for j in range(linkNumbers):
                            if '6-K' in data['facts'][form][i]['units']['shares'][j]['form']:
                                value = data['facts'][form][i]['units']['shares'][::-1][j]
                                returnResults.append([{'Field Name': '6-K: ' + i + ' ' + value['filed'],
                                                       'Account Number': value['accn'],
                                                       'Fiscal Year': value['fy'],
                                                       'Fiscal Period': value['fp'],
                                                       'Value': value['val'],
                                                       'Unit': list(data['facts'][form][i]['units'].keys())[0],
                                                       'Taxonomy': form,
                                                       'Notes': data['facts'][form][i]['label'],

                                                       'Entity Type': 'Form Field'},
                                                      {uid: {'Resolution': '6-K Field',
                                                             'Name': 'CIK Edgar ID',
                                                             'Notes': ''}}])

        return returnResults
