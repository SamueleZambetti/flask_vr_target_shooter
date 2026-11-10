import os
from flask import Flask
from blueprints.frontend import app as bp_frontend
from blueprints.api import app as bp_api

app = Flask(__name__)

app.register_blueprint(bp_frontend)
app.register_blueprint(bp_api, url_prefix='/api')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
