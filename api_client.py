# -*- coding: utf-8 -*-
import json
import threading

import numpy as np
from urllib3 import PoolManager
from urllib3.util.timeout import Timeout


class Autobahn(PoolManager):
    """Api ports scheduler"""
    def __init__(self, ports, host='localhost', **kw):
        pools = len(ports)
        PoolManager.__init__(self, max(10, pools), **kw)
        self._lock = threading.RLock()
        self.host = host
        if pools > 1:
            self.ports = np.array(ports, dtype=np.uint16)
            self._port = self._roll
        else:
            self.ports = ports[0]
            self._port = lambda: self.ports

    def _roll(self):
        with self._lock:
            self.ports = np.roll(self.ports, 1)
        return self.ports[0]

    def json(self, path='/', url=None, method='GET'):
        if not url:
            url = '{}:{:d}{}'.format(self.host, self._port(), path)
        try:
            r = self.request(method, url)
            if r.status == 200:
                return json.loads(r.data.decode())
            return []
        except Exception:
            return []


timeout = Timeout(connect=2.0, read=4.0)

api_client = Autobahn([3232, ], timeout=timeout)
