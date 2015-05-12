from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask.ext.script import Manager, Server
import consul
import socket
import os


SECRET_KEY = "KeepThisS3cr3t"
SITE_WIDTH = 800


app = Flask(__name__)

Bootstrap(app)
manager = Manager(app)
app.config.from_object(__name__)


manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

def register():
    c = consul.Consul(host=os.getenv("CONSUL_IP"), port=int(os.getenv("CONSUL_PORT")))
    s = c.agent.service
    s.register("Python_app", service_id=socket.gethostname(), port=5000, http="http://google.com", interval="10s", tags=['python'])

@app.route('/')
def cntr():
    return render_template('index.html',hostname=socket.gethostname())

@app.route("/healthcheck")
def healthcheck():
    return "200 OK From "+socket.gethostname()

if __name__ == '__main__':
    register()
    manager.run()
