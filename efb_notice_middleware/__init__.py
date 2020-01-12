# coding: utf-8
import io
import os
import re
import logging
import string
from tempfile import NamedTemporaryFile
from typing import Optional
from ruamel.yaml import YAML

from ehforwarderbot import Middleware, Message, \
    coordinator, Channel, utils
from ehforwarderbot.message import Substitutions

from .__version__ import __version__ as version


class NoticeMiddleware(Middleware):
    """
    EFB Middleware - NoticeMiddleware
    """

    middleware_id: str = "notice.NoticeMiddleware"
    middleware_name: str = "Notice Middleware"
    __version__: str = version

    logger: logging.Logger = logging.getLogger("plugins.%s" % middleware_id)

    def __init__(self, instance_id=None):
        super().__init__()

        if hasattr(coordinator, "master") and isinstance(coordinator.master, Channel):
            self.admin = coordinator.master.config['admins'][0]

        if hasattr(coordinator, "slaves") and coordinator.slaves['blueset.wechat']:
            self.channel_ews = coordinator.slaves['blueset.wechat']

        self.notices_pattern = None
        self.tags_pattern = None
        self.load_config()

    def load_config(self):
        """
        Load configuration from path specified by the framework.

        Configuration file is in YAML format.
        """
        config_path = utils.get_config_path(self.middleware_id)
        if not config_path.exists():
            return

        with config_path.open() as f:
            data = YAML().load(f)

            # Verify configuration
            notices = data.get("notices", [])
            if notices and not isinstance(notices, list):
                raise ValueError(
                    "notices are expected to be a list, but {} is found.".format(notices))
            if len(notices) > 0:
                self.notices_pattern = re.compile('|'.join(notices))

            tags = data.get("tags", [])
            if tags and not isinstance(tags, list):
                raise ValueError(
                    "tags are expected to be a list, but {} is found.".format(tags))
            if len(tags) > 0:
                self.tagMap = {}
                _tag = []
                for tag in tags:
                    t = tag.split(':', 1)
                    if len(t) == 2:
                        self.tagMap[t[0]] = t[1]
                    _tag.append(t[0])

                self.tags_pattern = re.compile('|'.join(_tag))

    def sent_by_master(self, message: Message) -> bool:
        author = message.author
        if author and author.module_id and author.module_id == 'blueset.telegram':
            return True
        else:
            return False

    def process_message(self, message: Message) -> Optional[Message]:
        """
        Process a message with middleware
        Args:
            message (:obj:`.Message`): Message object to process
        Returns:
            Optional[:obj:`.Message`]: Processed message or None if discarded.
        """

        # self.logger.log(99, "Received message from NoticeMiddleware: %s", message.__dict__)

        if self.sent_by_master(message):
            return message

        tags = {}

        attributes = message.attributes
        if getattr(attributes, 'title', None) or getattr(attributes, 'description', None):
            search_text = f"{getattr(attributes, 'title', '')}{getattr(attributes, 'description', '')}"
            if self.notices_pattern:
                # self.logger.log(99, "Received message from NoticeMiddleware: %s", attributes.__dict__)
                result = self.notices_pattern.findall(search_text)
                if len(result) > 0:
                    attributes.image = 'tg://user?id=%s' % self.admin
                    # self.logger.log(99, "Received message from NoticeMiddleware: %s", message.__repr__)

            if self.tags_pattern:
                result = set(self.tags_pattern.findall(search_text))
                if len(result) > 0:
                    append = '\n\n'
                    for item in result:
                        if not tags.get(item):
                            tag = self.tagMap.get(item, item)
                            tags[tag] = True
                            append += '#%s  ' % tag
                    attributes.description = getattr(
                        attributes, 'description', '').strip() + append.strip(' ')

        text = message.text
        if text:
            if self.tags_pattern:
                result = set(self.tags_pattern.findall(text))
                if len(result) > 0:
                    append = '\n\n'
                    for item in result:
                        if not tags.get(item):
                            tag = self.tagMap.get(item, item)
                            tags[tag] = True
                            append += '#%s  ' % tag
                    message.text = message.text.strip() + append.strip(' ')

            if self.notices_pattern:
                result = self.notices_pattern.findall(text)
                if len(result) > 0:
                    message.text = '🔊 ' + message.text
                    message.substitutions = Substitutions({
                        (0, 1): message.chat.self
                    })

        return message
