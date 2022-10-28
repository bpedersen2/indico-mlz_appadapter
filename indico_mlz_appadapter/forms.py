# This file is part of Indico.
# Copyright (C) 2017 Bjoern Pedersen.
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from indico.web.forms.base import IndicoForm
from wtforms.fields import StringField, URLField

from indico_mlz_appadapter import _

APPIMAGE_DESC = """URL for MLZ app teaser image"""
NEWSURL_DESC = """URL for MLZ app news page"""
NEWSUPDATED_DESC = """Time when news was last updated format: YYYY-MM-DD hh:mm"""


class EventSettingsForm(IndicoForm):
    appimage = URLField(_('App image url'), [], description=APPIMAGE_DESC)
    newsurl = URLField(_('News page url'), [], description=NEWSURL_DESC)
    news_updated = StringField(_('News last updated'), [], description=NEWSUPDATED_DESC)
