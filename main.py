import logging
import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)


class EnpassExtension(Extension):

    def __init__(self):
        logger.info('init Enpass extension')
        super(EnpassExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        rawstr = event.get_argument()
        if rawstr is None:
            rawstr = ""

        php_password_default = os.popen("php -r 'echo password_hash(%s, PASSWORD_DEFAULT);'" % rawstr).read()
        php_bycrypt = os.popen("php -r 'echo password_hash(%s, PASSWORD_BCRYPT);'" % rawstr).read()

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=php_password_default,
                                         description='PHP PASSWORD_DEFAULT',
                                         highlightable=False,
                                         on_enter=CopyToClipboardAction(php_password_default)
                                         ))

        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=php_bycrypt,
                                         description='PHP BYCRYPT',
                                         highlightable=False,
                                         on_enter=CopyToClipboardAction(php_bycrypt)
                                         ))

        return RenderResultListAction(items)


if __name__ == '__main__':
    EnpassExtension().run()
