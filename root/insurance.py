import requests
import logging

logging.basicConfig(level=logging.DEBUG)

class Client:
    def __init__(self, baseURL, appID, appSecret):
        self.baseURL = baseURL
        self.appID = appID
        self.appSecret = appSecret
        self.claims = Claims(self)
        self.gadgets = Gadgets(self)

    def call(self, method, path, params=None, **kwargs):
        resp = requests.request(method, f'{self.baseURL}/{path}', params=params, auth=(self.appID, self.appSecret))
        if resp.status_code == 200 or resp.status_code == 201:
            return resp.json()
        raise Exception(resp.status_code)


class Claims:
    def __init__(self, client):
        self.client = client

    def list(self, status=None, approval=None):
        params = {}
        if status:
            params["claim_status"] = status
        params = {}
        if approval:
            params["approval_status"] = approval
        
        return self.client.call("get", "claims", params=params)


class Gadgets:
    def __init__(self, client):
        self.client = client

    def list_models(self):
        return self.client.call("get", "gadgets/models")

    def list_phone_brands(self):
        models = self.list_models()
        return set([phone['make'] for phone in models])

    def list_phones_by_brand(self, brand):
        models = self.list_models()
        return set([phone['name'] for phone in models if phone['make'] == brand])

    def get_phone_value(self, phone):
        models = self.list_models()
        return list(filter(lambda p: p['name'] == phone, models))[0]['value']/100