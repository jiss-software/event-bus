import tornado
import json
from pymongo import ASCENDING
from tornado.options import options


class EventsHandler(tornado.web.RequestHandler):
    def initialize(self, logger, mongodb):
        self.logger = logger
        self.mongodb = mongodb[options.db_name]

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, context, channel):
        self.logger.info('Request to events list for `%s` at `%s`' % (channel, context))

        # Load params and check that they are consistent
        start = self.get_query_argument('start', default=None)
        peek = self.get_query_argument('peek', default=None)

        if start and peek:
            self.set_status(400)
            self.write(json.dumps({'error': 'Request params are inconsistent. Please try to use them separately.'}))
            return

        # Add request conditions
        condition = {'context': context, 'channel': channel}

        if start:
            if not start.isdigit():
                self.set_status(400)
                self.write(json.dumps({'error': 'Start param should be and integer value.'}))
                return

            self.logger.info('Start condition used: `%s`' % start)
            condition['timestamp'] = {'$gt': long(start)}

        cursor = self.mongodb[options.db_name].find(condition)

        # Use peek mode
        if peek:
            if not peek.isdigit():
                self.set_status(400)
                self.write(json.dumps({'error': 'Peek param should be and integer value.'}))
                return

            if (yield cursor.count()) < peek:
                self.set_status(204)
                return

            self.logger.info('Peek index: `%s`' % peek)
            cursor.limit(int(peek)).skip(1)
        # Check if response not to big
        elif (yield cursor.count()) > 100:
            self.set_status(400)
            self.write(json.dumps({'error': 'Requested range is to big.'}))
            return

        # Execute DB request
        data = yield cursor.sort([('timestamp', ASCENDING)]).to_list(length=100)

        # Format response
        result = json.dumps([(item['timestamp'], item['payload']) for item in data])
        self.logger.info('Response for events list: %s' % result)
        self.write(result)

    def post(self):
        pass
