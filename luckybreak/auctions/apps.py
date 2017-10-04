from __future__ import unicode_literals

from django.apps import AppConfig


class AuctionsConfig(AppConfig):
    name = 'luckybreak.auctions'

    def ready(self):
        super(AuctionsConfig, self).ready()
        from . import signals  # noqa
