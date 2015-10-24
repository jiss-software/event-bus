import tornado
import json


class HealthCheckHandler(tornado.web.RequestHandler):
    def initialize(self, logger):
        self.logger = logger

    def get(self):
        self.logger.info('Request to health check: /')

        result = json.dumps({
            'status': 'OK'
        })

        self.logger.info('Response for health check: %s' % result)
        self.write(result)
