import tornado
import logging
from JsonEncoders import JsonEncoders
from json import dumps


class BaseHandler(tornado.web.RequestHandler):
    logger = logging.getLogger(__name__)

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def get_allowed_methods(self):
        return [
            "GET",
            "PUT",
            "POST",
            "DELETE",
            "OPTIONS"
        ]

    def get_allowed_headers(self):
        return [
            "Origin",
            "X-Requested-With",
            "Content-Type",
            "Accept",
            "Cache-Control",
            "Referer"
            "User-Agent"
            "Accept-Encoding",
            "Accept-Language",

            "X-Jiss-Session",
            "X-Jiss-Context",
            "X-Jiss-Language",
            "X-Jiss-Calculation-Type",
            "X-Jiss-Issuer",
        ]

    def get_allowed_type(self):
        return "application/json"

    def set_default_headers(self):
        common_headers = {
            "Allow": ", ".join(self.get_allowed_methods()),
            "Accept": self.get_allowed_type(),
            "Accept-Charset": "utf-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Max-Age": "1728000",
            "Access-Control-Allow-Methods": ", ".join(self.get_allowed_methods()),
            "Access-Control-Allow-Headers": ", ".join(self.get_allowed_headers())
        }

        for key, value in common_headers.iteritems():
            self.add_header(key, value)

    def response_error(self, text, code=500):
        self.set_header('Content-Type', 'application/json')
        self.set_status(code)
        self.write(self._dumps({'error': text}))

    def response_json(self, data, code=200):
        response = self._dumps(data)

        self.set_header('Content-Type', 'application/json')
        self.set_status(code)
        self.write(response)
        self.finish()
        self.logger.info('Response: %s' % response)

    def options(self, **ignore):
        self.set_status(200)
        self.finish()

    def _dumps(self, data):
        return dumps(data, cls=JsonEncoders)
