#!/usr/bin/env python3


class EtherScanGetBlocksMined:
    name = "EtherScan.io Get Blocks Mined"
    description = "EtherScan Blocks Mined from the selected account"
    originTypes = {"Crypto Wallet"}
    resultTypes = {'Crypto Wallet'}
    parameters = {'EtherScan API Key': {'description': "Enter the api key under your profile after signing up at "
                                                       "https://etherscan.io",
                                        'type': 'String',
                                        'value': '',
                  'global': True}}

    def resolution(self, entityJsonList, parameters):
        import requests

        return_result = []

        api_key = parameters['EtherScan API Key']
        url = "https://api.etherscan.io/api"

        for entity in entityJsonList:
            uid = entity['uid']
            primary_field = entity[list(entity)[1]]
            crafted_url =\
                f"{url}?module=account&action=getminedblocks&address={primary_field}&tag=latest&apikey={api_key}"
            try:
                response = requests.get(crafted_url)
            except requests.exceptions.ConnectionError:
                return "Please check your internet connection"
            response = response.json()
            return_result.append([{'Phrase': response['result'],
                                   'Entity Type': 'Phrase'},
                                  {uid: {'Resolution': 'EtherScan.io Blocks Mined', 'Notes': ''}}])
        return return_result
