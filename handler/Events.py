import tornado
import json


class EventsHandler(tornado.web.RequestHandler):
    def initialize(self, logger):
        self.logger = logger

    def get(self):
        self.logger.info('Request to events list')

        result = json.dumps([])
        self.logger.info('Response for events list: %s' % result)
        self.write(result)
