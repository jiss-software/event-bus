import tornado
from pymongo import ASCENDING
from tornado.options import options
import time
import re
from bson.json_util import dumps, loads


class EventsHandler(tornado.web.RequestHandler):
    def initialize(self, logger, mongodb):
        self.logger = logger
        self.mongodb = mongodb[options.db_name]['Events']

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, context, channel):
        self.logger.info('Request to events list for `%s` at `%s`' % (channel, context))

        # Load params and check that they are consistent
        start = self.get_query_argument('start', default=None)
        peek = self.get_query_argument('peek', default=None)

        if start and peek:
            self.set_status(400)
            self.write(dumps({'error': 'Request params are inconsistent. Please try to use them separately.'}))
            return

        # Add request conditions
        condition = {'context': context, 'channel': channel}

        if start:
            if re.match("^\d+?\.\d+?$", start) is None:
                self.set_status(400)
                self.write(dumps({'error': 'Start param should be and integer value.'}))
                return

            self.logger.info('Start condition used: `%s`' % start)
            condition['timestamp'] = {'$gt': float(start)}

        cursor = self.mongodb.find(condition)

        # Use peek mode
        if peek:
            if not peek.isdigit():
                self.set_status(400)
                self.write(dumps({'error': 'Peek param should be and integer value.'}))
                return

            if (yield cursor.count()) < peek:
                self.set_status(204)
                return

            self.logger.info('Peek index: `%s`' % peek)
            cursor.limit(int(peek)).skip(1)
        # Check if response not to big
        elif (yield cursor.count()) > 100:
            self.set_status(400)
            self.write(dumps({'error': 'Requested range is to big.'}))
            return

        # Execute DB request
        data = yield cursor.sort([('timestamp', ASCENDING)]).to_list(length=100)

        # Format response
        result = dumps([(item['timestamp'], item['payload']) for item in data])
        self.logger.info('Response for events list: %s' % result)
        self.write(result)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, context, channel):
        self.logger.info('Request to register event for `%s` at `%s`' % (channel, context))

        if not self.request.body:
            self.set_status(400)
            self.write(dumps({'error': 'Empty event payload.'}))
            return

        issuer = self.request.headers.get('X-JISS-ISSUER')

        if not issuer:
            self.set_status(400)
            self.write(dumps({'error': 'Issuer of new event not set in request.'}))
            return

        timestamp = time.time()
        event = {
            "issuer": issuer,
            "context": context,
            "channel": channel,
            "timestamp": timestamp,

            "payload": loads(self.request.body)
        }

        new_id = yield self.mongodb.save(event)

        result = dumps({'id': new_id, 'timestamp': timestamp})
        self.logger.info('New event registered events list: %s' % dumps(event))
        self.logger.info('Response for registration is: %s' % result)
        self.write(result)
