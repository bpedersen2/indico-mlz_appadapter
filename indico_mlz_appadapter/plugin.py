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

from flask import session
from indico.core import signals
from indico.core.plugins import IndicoPlugin, url_for_plugin
from indico.modules.events.features.util import is_feature_enabled
from indico.web.http_api import HTTPAPIHook
from indico.web.menu import SideMenuItem

from indico_mlz_appadapter import _
from indico_mlz_appadapter.blueprint import blueprint
from indico_mlz_appadapter.forms import EventSettingsForm


class MLZAppAdapterPlugin(IndicoPlugin):
    """MLZ appadapter API plugin


    REST API:
        /mlz/appadapter/<eventid>/appimage
    """

    acl_settings = {'managers'}
    configurable = True
    event_settings_form = EventSettingsForm

    def init(self):
        super().init()
        self.connect(signals.menu.items, self.extend_event_management_menu, sender='event-management-sidemenu')

    def get_blueprints(self):
        yield blueprint

    def extend_event_management_menu(self, sender, event, **kwargs):
        if event.can_manage(session.user) and is_feature_enabled(event, 'mlzappadapter'):
            yield SideMenuItem('MLZappadaptersettings',
                               _('MLZ appadapter settings'),
                               url_for_plugin('mlz_appadapter.configure', event),
                               section='services')
