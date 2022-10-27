from indico.core import signals
from indico.modules.events.features.base import EventFeature
from indico.modules.events.settings import EventSettingsProxy
from indico.util.i18n import make_bound_gettext

_ = make_bound_gettext('mlzappadapter')

mlzappadapter_event_settings = EventSettingsProxy('mlzappadapter', {
    'appimage': None,
    'newsurl': None,
    'news_updated': None
})


@signals.event.get_feature_definitions.connect
def _get_feature_definitions(sender, **kwargs):
    return MLZappadapterFeature


class MLZappadapterFeature(EventFeature):
    name = 'mlzappadapter'
    friendly_name = _('MLZ appadapter')
    description = _('Additional data for the MLZ app')

    @classmethod
    def enabled(cls, event, cloning):
        pass
