from flask import Blueprint, request, jsonify
from db import db
from models import Servico

servicos_bp = Blueprint('servicos', __name__)


@servicos_bp.route('/servicos', methods=['GET'])
def listar():
    servicos = Servico.query.all()
    return jsonify({
        "servicos": [s.para_dic() for s in servicos],
        "total":    len(servicos)
    }), 200


@servicos_bp.route('/servicos/<int:id>', methods=['GET'])
def buscar(id):
    servico = Servico.query.get(id)
    if not servico:
        return jsonify({'erro': 'Serviço não encontrado'}), 404
    return jsonify({"servico": servico.para_dic()}), 200


@servicos_bp.route('/servicos', methods=['POST'])
def criar():
    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400
    if not d.get('nome'):
        return jsonify({'erro': "O campo 'nome' é obrigatório"}), 400

    servico = Servico(
        nome      = d['nome'],
        descricao = d.get('descricao'),
        valor     = d.get('valor', 0)
    )
    db.session.add(servico)
    db.session.commit()
    return jsonify({'mensagem': 'Serviço criado com sucesso', 'servico': servico.para_dic()}), 201


@servicos_bp.route('/servicos/<int:id>', methods=['PUT'])
def atualizar(id):
    servico = Servico.query.get(id)
    if not servico:
        return jsonify({'erro': 'Serviço não encontrado'}), 404

    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400

    if 'nome'      in d: servico.nome      = d['nome']
    if 'descricao' in d: servico.descricao = d['descricao']
    if 'valor'     in d: servico.valor     = d['valor']

    db.session.commit()
    return jsonify({'mensagem': 'Serviço atualizado com sucesso', 'servico': servico.para_dic()}), 200


@servicos_bp.route('/servicos/<int:id>', methods=['DELETE'])
def deletar(id):
    servico = Servico.query.get(id)
    if not servico:
        return jsonify({'erro': 'Serviço não encontrado'}), 404

    db.session.delete(servico)
    db.session.commit()
    return jsonify({'mensagem': 'Serviço deletado com sucesso'}), 200
