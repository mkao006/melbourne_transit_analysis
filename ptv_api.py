import configparser
import requests
from urllib.parse import urljoin
from hashlib import sha1
import hmac


class PtvApiV3:
    def __init__(self, devid, api_key):
        self.devid = devid
        self.api_key = api_key
        self.base_url = 'https://timetableapi.ptv.vic.gov.au'
        self.api_version = '/v3/'

    def get(self, endpoint):
        ''' Makecall to API to obtain data.
        '''
        request_url = self._build_request_url(endpoint)
        signature = self._calculate_signature(request_url)
        complete_url = self.base_url + request_url + '&signature=' + signature
        return requests.get(url=complete_url).json()

    def _build_request_url(self, endpoint):
        '''Tbe method create the request url required as part of signature
        calculation.

        '''
        # TODO (Michael): Strip the forward slash in endpoint if exist)
        devid_url = (endpoint + ('&' if('?' in endpoint) else '?') +
                     'devid=' + self.devid)
        return urljoin(self.api_version, devid_url)

    def _calculate_signature(self, request):
        '''The method returns the signature required for the PTV API validation.

        See
        http://stevage.github.io/PTV-API-doc/3-quickstart.html#header1
        for more information.

        '''
        # Append to suffix to request
        hashed = hmac.new(self.api_key.encode('utf-8'),
                          request.encode('utf-8'), sha1)
        signature = hashed.hexdigest()
        return signature.upper()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('ptv_api_key')
    devid = config.get('default', 'devid')
    api_key = config.get('default', 'api_key')

    con = PtvApiV3(devid=devid, api_key=api_key)
    routes = con.get('routes')
    print('The first route is:\n')
    print(routes['routes'][0])
