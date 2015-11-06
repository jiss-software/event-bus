import tornado.ioloop
import tornado.web
import logging
from handler import HealthCheckHandler
from handler import EventsHandler
import motor
from tornado.options import define, options
import os
import sys


define("port", default=33002, help="Application port")
define("db_address", default="mongodb://mongodb:27017", help="Database address")
define("db_name", default="Events", help="Database name")
define("max_buffer_size", default=50 * 1024**2, help="")
define("log_dir", default="log", help="Logger directory")

if not os.path.exists(options.log_dir):
    os.makedirs(options.log_dir)

logging.basicConfig(
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    filename='log/server.log',
    level=logging.DEBUG
)

ioLoop = tornado.ioloop.IOLoop.current()
try:
    mongodb = ioLoop.run_sync(motor.MotorClient(options.db_address).open)
except:
    logging.getLogger('INIT').error('Cannot connect to mongodb')
    sys.exit()

context = dict(
    logger=logging.getLogger('HealthCheck'),
    mongodb=mongodb
)

app = tornado.web.Application([
    (r"/", HealthCheckHandler, context),
    (r"/events/([A-Za-z_.]*)/([A-Za-z_.]*)", EventsHandler, context),
], autoreload=True)

app.listen(options.port)

if __name__ == "__main__":
    try:
        logging.info("Starting HTTP server on port %d" % options.port)
        ioLoop.start()
    except KeyboardInterrupt:
        logging.info("Shutting down server HTTP proxy on port %d" % options.port)
        ioLoop.stop()
