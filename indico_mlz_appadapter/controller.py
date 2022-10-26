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

from __future__ import unicode_literals

from flask import jsonify, request, session
from indico.modules.events.models.events import Event
from indico.web.rh import RH, oauth_scope
from werkzeug.exceptions import Forbidden
from . import mlzappadapter_event_settings


@oauth_scope('any')
class RHMLZappadapterBase(RH):
    """RESTful registrant API base class"""

    CSRF_ENABLED = False
    FLAT = False

    def _process_args(self):
        self.event_id = request.view_args['event_id']
        self.event = Event.get(self.event_id, is_deleted=False)

    def _check_access(self):
        ok = self.event.is_public or self.event.can_display(session.user)
        if not ok:
            raise Forbidden()


class RHappadapterAppImage(RHMLZappadapterBase):
    """ appadapter: image for app as url"""
    def _process_GET(self):
        data = {}
        url = mlzappadapter_event_settings.get(self.event, 'appimage')
        data['appimage'] = url or self.event.external_logo_url or self.event.category.effective_icon_url
        return jsonify(data)


class RHappadapterAppImage(RHMLZappadapterBase):
    """ appadapter: news url and status"""
    def _process_GET(self):
        data = {}
        url = mlzappadapter_event_settings.get(self.event, 'news')
        data['newsurl'] = url or None
        return jsonify(data)
