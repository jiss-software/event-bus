import tornado
import json


class EventsHandler(tornado.web.RequestHandler):
    def initialize(self, logger):
        self.logger = logger

    def get(self, context, channel):
        self.logger.info('Request to events list for `%s` at `%s`' % (channel, context))

        result = json.dumps([])
        self.logger.info('Response for events list: %s' % result)
        self.write(result)
