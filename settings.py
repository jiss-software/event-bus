from tornado.options import define
from handler import HealthCheckHandler, EventsHandler

define("port", default=33003, help="Application port")
define("db_address", default="mongodb://localhost:27017", help="Database address")
define("db_name", default="Files", help="Database name")
define("max_buffer_size", default=50 * 1024**2, help="")
define("autoreload", default=False, help="Autoreload server on change")

define("log_dir", default="log", help="Logger directory")
define("log_file", default="jiss-event-service.log", help="Logger file name")

routing = [
    (r"/", HealthCheckHandler),
    (r"/events/([A-Za-z_.]*)/([A-Za-z_.]*)", EventsHandler),
]
