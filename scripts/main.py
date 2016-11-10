#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing

import log_initializer  # import first
import app

# logging
from logging import getLogger, DEBUG, WARNING
log_initializer.setFmt()
log_initializer.setRootLevel(WARNING)
logger = getLogger(__name__)
logger.setLevel(DEBUG)
app.logger.setLevel(DEBUG)

if __name__ == '__main__':
    # IO queue
    update_queue = multiprocessing.Queue()
    response_queue = multiprocessing.Queue()

    # Start server
    app.start(update_queue, response_queue)

    # Main process
    try:
        while True:
            # Wait for browser inputs
            data = update_queue.get()

            if 'range' in data:
                val = data['range']
                logger.info('Range input event ({})'.format(val))
                message = 'Response: Range is changed ({})'.format(val)
            elif 'button' in data:
                logger.info('Button event')
                message = 'Response: Button clicked'
            else:
                logger.error('Invalid event')
                continue

            # Response to the browser
            response_queue.put({'message': message})

    except KeyboardInterrupt:
        logger.info('Exit')
