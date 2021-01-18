# -*- coding: utf-8 -*-
import logging
import stanza
import e2edutch.download

logger = logging.getLogger(__name__)


def download_models():
    logger.info('Downloading stanza models...')
    stanza.download('nl')
    logger.info('Downloading e2edutch models...')
    e2edutch.download.download_data()
