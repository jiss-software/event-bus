import core
import tornado


class HealthCheckHandler(core.BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.logger.info('Request to health check')

        components = {
            'mongodb': None
        }

        components['mongodb'] = yield self.settings['db'].alive()

        for key in components:
            if components[key] is None:
                components[key] = False

        self.response_json({
            'status': False not in components.values(),
            'components': components
        })
