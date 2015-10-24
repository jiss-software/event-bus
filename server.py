import tornado.ioloop
import tornado.web
import logging
from handler import HealthCheckHandler
from handler import EventsHandler
import motor
from tornado.options import define, options
import os

define("port", default=33002, help="Application port")
define("db_address", default="mongodb://localhost:27017", help="Database address")
define("db_name", default="test", help="Database name")
define("max_buffer_size", default=50 * 1024**2, help="")
define("log_dir", default="log", help="Logger directory")

if not os.path.exists(options.log_dir):
    os.makedirs(options.log_dir)

logging.basicConfig(
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    filename='log/server.log',
    level=logging.DEBUG
)

# mongodb = motor.MotorClient(DB_ADDRESS)

context = dict(
    logger=logging.getLogger('HealthCheck'),
    # database=mongodb[DB_NAME]
)

app = tornado.web.Application([
    (r"/", HealthCheckHandler, context),
    (r"/events", EventsHandler, context),
], autoreload=True)

app.listen(options.port)

if __name__ == "__main__":
    ioLoop = tornado.ioloop.IOLoop.current()
    try:
        logging.info("Starting HTTP proxy on port %d" % options.port)
        ioLoop.start()
    except KeyboardInterrupt:
        logging.info("Shutting down server HTTP proxy on port %d" % options.port)
        ioLoop.stop()