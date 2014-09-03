# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)


class Light(object):
    def __init__(self, light_id, bridge):
        self.bridge = bridge
        self.id = int(light_id)
        self.name = None
        self.json = None
        self._update()

    def __str__(self):
        return '<%s %s "%s">' % (self.__class__.__name__, self.id,
                                 self.name)

    def _update(self):
        j = self.bridge.get('/lights/%s' % self.id)
        self.name = j['name']
        self.json = j

    def __getattr__(self, name):
        if name in self.json:
            return self.json[name]
        else:
            raise AttributeError("'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def _put(self, path, data):
        return self.bridge.put('/lights/%s/%s' % (self.id, path), data)

    def off(self):
        self.set_state({"on": False})

    def on(self, state={}):
        state.update({"on": True})
        self.set_state(state)

    def set_state(self, state):
        self._put('state', state)
        self._update()

    @property
    def bri(self):
        self._update()
        return self.json['state']['bri']

    @bri.setter
    def bri(self, brightness):
        if 0 <= brightness <= 255:
            self.set_state({"bri": brightness})

    @property
    def hue(self):
        self._update()
        return self.json['state']['hue']

    @hue.setter
    def hue(self, hue):
        if 0 <= hue <= 65535:
            self.set_state({"hue": hue})

    @property
    def sat(self):
        self._update()
        return self.json['state']['sat']

    @sat.setter
    def sat(self, saturation):
        if 0 <= saturation <= 255:
            self.set_state({"sat": saturation})
