import requests
import logging

logging.basicConfig(level=logging.DEBUG)

class Client:
    def __init__(self, baseURL, appID, appSecret):
        self.baseURL = baseURL
        self.appID = appID
        self.appSecret = appSecret
        self.applications = Applications(self)
        self.claims = Claims(self)
        self.policyholders = PolicyHolders(self)
        self.gadgets = Gadgets(self)

    def call(self, method, path, params=None, **kwargs):
        resp = requests.request(method, f'{self.baseURL}/{path}', params=params, auth=(self.appID, self.appSecret))
        if resp.status_code == 200 or resp.status_code == 201:
            return resp.json()
        raise Exception(resp.status_code)


class Resource:
    def __init__(self, client):
        self.client = client
    
    def call(self, method, path, params=None, **kwargs):
        return self.call(method, path, params, **kwargs)


class Applications(Resource):
    def __init__(self, client):
         super().__init__(client)
    
    def create(self, policyholder_id, quote_package_id, monthly_premium, serial_number=None):
        data = {
            policyholder_id:  policyholder_id,
            quote_package_id: quote_package_id,
            monthly_premium:  monthly_premium,
            serial_number:    serial_number
        }
        return self.call("post", "applications", json=data)


class Claims(Resource):
    def __init__(self, client):
         super().__init__(client)

    def list(self, status=None, approval=None):
        params = {}
        if status:
            params["claim_status"] = status
        params = {}
        if approval:
            params["approval_status"] = approval
        
        return self.call("get", "claims", params=params)

    def get(self, id):
        return self.call("get", f'claims/{id}')

    def open(self, policy_id=None, policy_holder_id=None):
        data = {
            policy_id: policy_id,
            policy_holder_id: policy_holder_id
        }
        return self.call("post", "claims", json=data)

    def link_policy(self, claim_id, policy_id):
        data = {
            policy_id: policy_id
        }
        return self.call("post", f'claims/{claim_id}/policy', json=data)

    def link_policy_holder(self, claim_id, policy_holder_id):
        data = {
            policy_holder_id: policy_holder_id
        }
        return self.call("post", f'claims/{claim_id}/policyholder', json=data)

    def link_events(self, claim_id):
        return self.call("post", f'claims/{claim_id}/events')



class PolicyHolders(Resource):
    def __init__(self, client):
         super().__init__(client)

    def create(self, id, first_name, last_name, email=None, date_of_birth=None, cellphone=None):
        data = {
            id:            id,
            first_name:    first_name,
            last_name:     last_name,
            date_of_birth: date_of_birth,
            email:         email,
            cellphone:     cellphone
        }
        return self.call("post", "policyholders", json=data)

    def list(self):
        return self.call("get", "policyholders")

    def get(self, id):
        return self.call("get", f'policyholders/{id}')

    def update(self, id, email=None, cellphone=None):
        data = {
            email:     email,
            cellphone: cellphone
        }
        return self.call("patch", f'policyholders/{id}', json=data)

    def list_events(self, id):
        return self.call("get", f'policyholders/{id}/events')
        

class Gadgets(Resource):
    def __init__(self, client):
         super().__init__(client)

    def list_models(self):
        return self.call("get", "gadgets/models")

    def list_phone_brands(self):
        models = self.list_models()
        return set([phone['make'] for phone in models])

    def list_phones_by_brand(self, brand):
        models = self.list_models()
        return set([phone['name'] for phone in models if phone['make'] == brand])

    def get_phone_value(self, phone):
        models = self.list_models()
        return list(filter(lambda p: p['name'] == phone, models))[0]['value']/100