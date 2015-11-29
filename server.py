import tornado.ioloop
import tornado.web
import logging
import motor
from settings import routing
from tornado.options import options
import os
import subprocess
import datetime

tornado.options.parse_command_line()

if not os.path.exists(options.log_dir):
    os.makedirs(options.log_dir)

logging.basicConfig(
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    filename='%s/%s' % (options.log_dir, options.log_file),
    level=logging.DEBUG
)

version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
started = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

ioLoop = tornado.ioloop.IOLoop.current()

logging.getLogger('INIT').info('Connecting to mongodb at: %s' % options.db_address)
mongodb = ioLoop.run_sync(motor.MotorClient(options.db_address).open)
app = tornado.web.Application(routing, db=mongodb, version=version, started=started, autoreload=options.autoreload)

app.listen(options.port)

if __name__ == "__main__":
    try:
        logging.info("Starting HTTP server on port %d" % options.port)
        ioLoop.start()
    except KeyboardInterrupt:
        logging.info("Shutting down server HTTP on port %d" % options.port)
        ioLoop.stop()
