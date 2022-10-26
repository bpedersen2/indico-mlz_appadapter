#  -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2018 Björn Pedersen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# Created on Mar 9, 2018
#
# @author: pedersen

import re
from collections import defaultdict
from csv import QUOTE_ALL, DictWriter
from io import BytesIO, StringIO

from indico.modules.events.models.events import Event
from indico.modules.events.registration.util import build_registration_api_data
from indico.web.flask.util import send_file
from indico.web.http_api import HTTPAPIHook
from indico.web.http_api.util import get_query_parameter
from sqlalchemy.orm import joinedload

from indico_mlz_appadapter import mlzappadapter_event_settings


class MLZappadapterBase(HTTPAPIHook):
    """Base class for Mlz appadapter http api"""

    METHOD_NAME = 'appadapter_data'
    TYPES = ('mlzevent', )
    DEFAULT_DETAIL = 'default'
    MAX_RECORDS = {'default': 100}
    GUEST_ALLOWED = False
    VALID_FORMATS = ('json', 'jsonp', 'xml')

    def _getParams(self):
        super()._getParams()
        self.event_id = self._pathParams['event']
        self.event = Event.get(self.event_id, is_deleted=False)

    def _has_access(self, user):
        return self.event.can_manage(user, permission='registration')


class MLZappadapterAppImageHook(MLZappadapterBase):
    """appadapter App image"""

    RE = r'(?P<event>[\w\s]+)'

    def appadapter_data(self, user):
        data = {'appimage': 'http://....' }
        return data

