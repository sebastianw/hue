# -*- coding: utf-8 -*-
import logging
import json
import requests
from .light import Light

log = logging.getLogger(__name__)


class BridgeError(Exception):
    def __init__(self, message, errortype=None, address=None, json=None):
        super(BridgeError, self).__init__(self, message)
        self.message = message
        self.type = errortype
        self.address = address
        self.json = json

    def __str__(self):
        return '(Type %s) %s' % (self.type, self.message)


class Bridge(object):
    def __init__(self, user=None, address=None, autodiscover=True):
        self._initialised = False
        self.user = user
        if not address and autodiscover:
            address = self._discover()
        if address:
            self.address = address

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address
        self._bridgeinit()

    def _discover(self):
        r = requests.get('https://www.meethue.com/api/nupnp')
        try:
            json = r.json()
        except ValueError:
            return None
        log.debug('Discovered bridge at %s' % json[0]['internalipaddress'])
        return json[0]['internalipaddress']

    def _query(self, rmethod, api, data=None):
        if not self._initialised:
            raise BridgeError('Bridge is not initialised')
        if api[0] == '/':
            api = api[1:]
        if self.user:
            url = 'http://%s/api/%s/%s' % (self.address, self.user, api)
        else:
            url = 'http://%s/api/%s' % (self.address, api)
        if data:
            data = json.dumps(data)
            log.debug('Calling %s %s with data: %s' % (rmethod, url, data))
            r = getattr(requests, rmethod)(url, data)
        else:
            log.debug('Calling %s %s' % (rmethod, url))
            r = getattr(requests, rmethod)(url)

        j = r.json()
        log.debug('Call returned: %s' % j)

        if isinstance(j, (list, tuple)):
            if 'error' in j[0]:
                err = j[0]['error']
                raise BridgeError(err['description'], err['type'],
                                  err['address'], j)

        return j

    def get(self, api):
        return self._query('get', api)

    def post(self, api, data):
        return self._query('post', api, data)

    def put(self, api, data):
        return self._query('put', api, data)

    def delete(self, api):
        return self._query('delete', api)

    def _bridgeinit(self):
        self._initialised = True
        data = self.get('/config')
        self.mac = data['mac']
        self.swversion = data['swversion']
        self.name = data['name']
        self.apiversion = data['apiversion']
        log.info('Initialised bridge "%s" at %s (%s) with SW/API %s/%s' %
                 (self.name, self.address, self.mac, self.swversion,
                  self.apiversion))

    @property
    def lights(self):
        j_lights = self.get('/lights')
        lights = {}
        for lid in j_lights.keys():
            lights[int(lid)] = Light(lid, self)
        return lights
