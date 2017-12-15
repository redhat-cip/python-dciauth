import json
from collections import OrderedDict

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class AuthRequest(object):
    def __init__(self, method='GET', endpoint='/', payload=None, headers=None, params=None):
        self.algorithm = 'DCI-HMAC-SHA256'
        self.method = method.upper()
        self.endpoint = endpoint
        self.payload = payload or {}
        self.headers = headers or {}
        self.filtered_headers = self._filter_headers(self.headers)
        self.params = params or {}

    def build_headers(self, client_type, client_id, signature):
        auth_string_format = ("{dci_algorithm} Credential={client_type}/{client_id}, "
                              "SignedHeaders={signed_headers}, Signature={signature},")
        headers = self.headers.copy()
        headers['Authorization'] = auth_string_format.format(
            dci_algorithm=self.algorithm,
            client_type=client_type,
            client_id=client_id,
            signed_headers=self.get_signed_headers_string(),
            signature=signature)
        return headers

    def add_header(self, key, value):
        self.headers[key] = value

    def get_headers_string(self):
        headers_string = ''
        for key, value in self._order_dict(self.filtered_headers).items():
            headers_string += '%s:%s\n' % (key, value)
        return headers_string

    def get_signed_headers_string(self):
        headers = self._order_dict(self.filtered_headers).keys()
        return ';'.join([header.lower() for header in headers])

    def get_query_string(self):
        return urlencode(self._order_dict(self.params))

    def get_payload_string(self):
        if self.payload:
            return json.dumps(self._order_dict(self.payload))
        return ''

    def get_client_info(self):
        authorization_header = self.headers.get('Authorization')
        info = {}
        if authorization_header:
            credentials = self.find_between(authorization_header, 'Credential=', ',').split('/')
            info['client_type'] = credentials[0]
            info['client_id'] = credentials[1]
            info['signature'] = self.find_between(authorization_header, 'Signature=', ',')
        return info

    @staticmethod
    def find_between(string, first, last):
        try:
            start = string.index(first) + len(first)
            end = string.index(last, start)
            return string[start:end]
        except ValueError:
            return ""

    @staticmethod
    def _order_dict(dictionary):
        return OrderedDict(sorted(dictionary.items(), key=lambda k: k[0]))

    def _filter_headers(self, headers):
        authorization_header = headers.get('Authorization')
        if not authorization_header:
            return headers
        signed_headers = self.find_between(authorization_header, 'SignedHeaders=', ',').split(';')
        filtered_headers = {}
        for key, value in headers.items():
            if key.lower() in signed_headers:
                filtered_headers[key.lower()] = value
        return filtered_headers
