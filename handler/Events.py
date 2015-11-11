import tornado
from pymongo import ASCENDING
from tornado.options import options
import time
import re
from bson.json_util import dumps, loads
import core


class EventsHandler(core.BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, context, channel):
        self.logger.info('Request to events list for `%s` at `%s`' % (channel, context))

        # Load params and check that they are consistent
        start = self.get_query_argument('start', default=None)
        peek = self.get_query_argument('peek', default=None)

        if start and peek:
            self.response_error('Request params are inconsistent. Please try to use them separately.', 400)
            return

        # Add request conditions
        if context == 'all':
            condition = {'channel': channel}
        else:
            condition = {'context': context, 'channel': channel}

        if start:
            if re.match("^\d+?\.\d+?$", start) is None:
                self.response_error('Start param should be and integer value.', 400)
                return

            self.logger.info('Start condition used: `%s`' % start)
            condition['timestamp'] = {'$gt': float(start)}

        collection = self.settings['db'][options.db_name]['Events']
        cursor = collection.find(condition)

        # Use peek mode
        quantity = yield cursor.count()
        if peek:
            if not peek.isdigit():
                self.response_error('Peek param should be and integer value.', 400)
                return

            if quantity < int(peek):
                self.set_status(204)
                return

            self.logger.info('Peek index: `%s`' % peek)
            cursor.skip(int(peek)).limit(1)
        # Check if response not to big
        elif quantity > 100:
            self.response_error('Requested range is to big.', 400)
            return

        # Execute DB request
        data = yield cursor.sort([('timestamp', ASCENDING)]).to_list(length=100)

        # Format response
        self.response_json(data)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, context, channel):
        self.logger.info('Request to register event for `%s` at `%s`' % (channel, context))

        if not self.request.body:
            self.response_error('Empty event payload.', 400)
            return

        issuer = self.request.headers.get('X-JISS-ISSUER')

        if not issuer:
            self.response_error('Issuer of new event not set in request.', 400)
            return

        timestamp = time.time()
        event = {
            "issuer": issuer,
            "context": context,
            "channel": channel,
            "timestamp": timestamp,

            "payload": loads(self.request.body)
        }

        collection = self.settings['db'][options.db_name]['Events']
        new_id = yield collection.save(event)

        self.logger.info('New event registered events list: %s' % dumps(event))
        self.response_json({'id': new_id, 'timestamp': timestamp})
