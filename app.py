from flask import Flask
from config import Config
from db import db, init_db

from routes.clientes      import clientes_bp
from routes.veiculos      import veiculos_bp
from routes.pecas         import pecas_bp
from routes.servicos      import servicos_bp
from routes.ordemservicos import os_bp


app = Flask(__name__)
app.config.from_object(Config)


init_db(app)


app.register_blueprint(clientes_bp)
app.register_blueprint(veiculos_bp)
app.register_blueprint(pecas_bp)
app.register_blueprint(servicos_bp)
app.register_blueprint(os_bp)



@app.route("/")
def ola():
    return "Oficina API", 200


if __name__ == "__main__":
    app.run(debug=True)
