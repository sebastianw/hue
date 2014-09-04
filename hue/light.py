# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)


class Light(object):
    def __init__(self, light_id, bridge):
        self.bridge = bridge
        self.id = int(light_id)
        self.json = None
        self._update()

    def __str__(self):
        return '<%s %s "%s">' % (self.__class__.__name__, self.id,
                                 self.name)

    def _update(self):
        j = self.bridge.get('/lights/%s' % self.id)
        self.json = j

    def __getattr__(self, name):
        self._update()
        if name in self.json:
            return self.json[name]
        else:
            raise AttributeError("'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def _put(self, path, data):
        return self.bridge.put('/lights/%s/%s' % (self.id, path), data)

    @property
    def name(self):
        self._update()
        return self.json['name']

    @name.setter
    def name(self, name):
        self._put('', {"name": name})
        self._update()

    def off(self):
        self.set_state({"on": False})

    def on(self, state={}):
        state.update({"on": True})
        self.set_state(state)

    def get_state(self, state):
        self._update()
        return self.json['state'][state]

    def set_state(self, state):
        self._put('state', state)
        self._update()

    @property
    def alert(self):
        self.get_state('alert')

    @alert.setter
    def alert(self, state):
            self.set_state({"alert": state})

    @property
    def bri(self):
        return self.get_state('bri')

    @bri.setter
    def bri(self, brightness):
        if 0 <= brightness <= 255:
            self.set_state({"bri": brightness})

    @property
    def ct(self):
        return self.get_state('ct')

    @ct.setter
    def ct(self, ct):
        return self.set_state({"ct": ct})

    @property
    def effect(self):
        return self.get_state('effect')

    @effect.setter
    def effect(self, effect):
        self.set_state({"effect": effect})

    @property
    def hue(self):
        return self.get_state('hue')

    @hue.setter
    def hue(self, hue):
        if 0 <= hue <= 65535:
            self.set_state({"hue": hue})

    @property
    def sat(self):
        return self.get_state('sat')

    @sat.setter
    def sat(self, saturation):
        if 0 <= saturation <= 255:
            self.set_state({"sat": saturation})

    @property
    def xy(self):
        return self.get_state('xy')

    @xy.setter
    def xy(self, xy):
        if len(xy) == 2 and 0 <= xy[0] <= 1 and 0 <= xy[1] <= 1:
            self.set_state({"xy": xy})
