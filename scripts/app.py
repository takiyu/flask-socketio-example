# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import multiprocessing
import os


# logging
from logging import getLogger, NullHandler, CRITICAL
logger = getLogger(__name__)
logger.addHandler(NullHandler())

# disable werkzeug logger
werkzeug_logger = getLogger('werkzeug')
werkzeug_logger.setLevel(CRITICAL)
# disable werkzeug logger
engineio_logger = getLogger('engineio')
engineio_logger.setLevel(CRITICAL)
# disable socketio logger
socketio_logger = getLogger('socketio')
socketio_logger.setLevel(CRITICAL)


IO_NAMESPACE = '/test'
ASYNC_MODE = 'eventlet'


def new_server(update_queue, response_queue, stop_page, port, secret_key):
    # create server
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = secret_key
    socketio = SocketIO(app, async_mode=ASYNC_MODE,
                        logger=False, engineio_logger=False)

    # rooting
    @app.route('/')
    def __index():
        logger.info('Render page')
        return render_template('index.html', script="index.js")

    if stop_page:
        @app.route('/stop')
        def __stop():
            socketio.stop()
            logger.info('Server stop request')
            return 'This server is stopped'

    @socketio.on('connect', namespace=IO_NAMESPACE)
    def __on_connect():
        logger.info('New connection is established')

    @socketio.on('disconnect', namespace=IO_NAMESPACE)
    def __on_disconnect():
        logger.info('Connection is closed')

    @socketio.on('update', namespace=IO_NAMESPACE)
    def __on_update(data):
        update_queue.put(data)
        if response_queue is not None:
            res = response_queue.get()
            emit('response', res)

    # start server
    logger.info('Start server on port %d' % port)
    socketio.run(app, host='0.0.0.0', port=port, debug=False, log_output=False)
    logger.info('Stop server on port %d' % port)


def start(update_queue, response_queue, stop_page=True, port=5000,
          secret_key=os.urandom(24)):
    '''Start new server on `port`.
    This function create new daemon process and start it.
    '''
    process = multiprocessing.Process(target=new_server,
                                      args=(update_queue, response_queue,
                                            stop_page, port, secret_key))
    process.daemon = True
    process.start()
