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

from flask import flash, jsonify, redirect, request, session
from indico.modules.events.management.controllers import RHManageEventBase
from indico.modules.events.models.events import Event
from indico.web.flask.util import url_for
from indico.web.forms.base import FormDefaults
from indico.web.rh import RH, oauth_scope
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import Forbidden

from indico_mlz_appadapter import _, mlzappadapter_event_settings
from indico_mlz_appadapter.forms import EventSettingsForm
from indico_mlz_appadapter.views import WPMLZappadapterEventMgmt

from . import mlzappadapter_event_settings


@oauth_scope('any')
class RHMLZappadapterBase(RH):
    """RESTful registrant API base class"""

    CSRF_ENABLED = False
    FLAT = False

    def _process_args(self):
        self.event_id = request.view_args['event_id']
        self.event = Event.get(self.event_id, is_deleted=False)
        if not self.event:
            raise NoResultFound

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


class RHappadapterAppNews(RHMLZappadapterBase):
    """ appadapter: news url and status"""
    def _process_GET(self):
        data = {}
        url = mlzappadapter_event_settings.get(self.event, 'newsurl')
        data['newsurl'] = url or None
        data['lastUpdated'] = mlzappadapter_event_settings.get(self.event, 'news_updated')
        return jsonify(data)





class RHMLZappadapterManageEvent(RHManageEventBase):
    EVENT_FEATURE = 'mlzappadapter'

    def _process(self):
        form = EventSettingsForm(prefix='mlzappadapter-',
                                 event=self.event,
                                 obj=FormDefaults(**mlzappadapter_event_settings.get_all(self.event)))
        if form.validate_on_submit():

            mlzappadapter_event_settings.set_multi(self.event, form.data)
            flash(_('Settings saved'), 'success')
            return redirect(url_for('.configure', self.event))
        return WPMLZappadapterEventMgmt.render_template('mlzappadapter_manage.html', self.event, form=form)
