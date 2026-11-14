from flask import Blueprint, request, jsonify
from db import db
from models import Cliente

clientes_bp = Blueprint('clientes', __name__)


@clientes_bp.route('/clientes', methods=['GET'])
def listar():
    clientes = Cliente.query.all()
    return jsonify({
        "clientes": [c.para_dic() for c in clientes],
        "total":    len(clientes)
    }), 200


@clientes_bp.route('/clientes/<int:id>', methods=['GET'])
def buscar(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    return jsonify({"cliente": cliente.para_dic()}), 200


@clientes_bp.route('/clientes', methods=['POST'])
def criar():
    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400
    if not d.get('nome'):
        return jsonify({'erro': "O campo 'nome' é obrigatório"}), 400

    cliente = Cliente(
        nome     = d['nome'],
        telefone = d.get('telefone'),
        email    = d.get('email'),
        endereco = d.get('endereco')
    )
    db.session.add(cliente)
    db.session.commit()
    return jsonify({'mensagem': 'Cliente criado com sucesso', 'cliente': cliente.para_dic()}), 201


@clientes_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400

    if 'nome' in d:
        if not d['nome']:
            return jsonify({'erro': "O campo 'nome' deve ser informado"}), 400
        cliente.nome = d['nome']
    if 'telefone' in d:
        cliente.telefone = d['telefone']
    if 'email' in d:
        cliente.email = d['email']
    if 'endereco' in d:
        cliente.endereco = d['endereco']

    db.session.commit()
    return jsonify({'mensagem': 'Cliente atualizado com sucesso', 'cliente': cliente.para_dic()}), 200


@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'mensagem': 'Cliente deletado com sucesso'}), 200
