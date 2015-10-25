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

        start = self.get_query_argument('start', default=None)

        condition = {'context': context, 'channel': channel}

        if start:
            if not start.isdigit():
                self.set_status(400)
                self.write(json.dumps({'error': 'Start param should be and integer value'}))
                return

            self.logger.info('Start condition used: `%s`' % start)
            condition['timestamp'] = {'$gt': long(start)}

        cursor = self.mongodb[options.db_name].find(condition)

        if (yield cursor.count()) > 100:
            self.set_status(400)
            self.write(json.dumps({'error': 'Requested range is to big'}))
            return

        data = yield cursor.sort([('timestamp', ASCENDING)]).to_list(length=100)

        result = json.dumps([(item['timestamp'], item['payload']) for item in data])
        self.logger.info('Response for events list: %s' % result)
        self.write(result)

    def post(self):
        pass
