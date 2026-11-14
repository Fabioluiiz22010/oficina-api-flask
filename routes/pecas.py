from flask import Blueprint, request, jsonify
from db import db
from models import Peca

pecas_bp = Blueprint('pecas', __name__)


@pecas_bp.route('/pecas', methods=['GET'])
def listar():
    pecas = Peca.query.all()
    return jsonify({
        "pecas": [p.para_dic() for p in pecas],
        "total": len(pecas)
    }), 200


@pecas_bp.route('/pecas/<int:id>', methods=['GET'])
def buscar(id):
    peca = Peca.query.get(id)
    if not peca:
        return jsonify({'erro': 'Peça não encontrada'}), 404
    return jsonify({"peca": peca.para_dic()}), 200


@pecas_bp.route('/pecas', methods=['POST'])
def criar():
    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400
    if not d.get('nome'):
        return jsonify({'erro': "O campo 'nome' é obrigatório"}), 400

    peca = Peca(
        nome               = d['nome'],
        descricao          = d.get('descricao'),
        valor_unitario     = d.get('valor_unitario', 0),
        quantidade_estoque = d.get('quantidade_estoque', 0)
    )
    db.session.add(peca)
    db.session.commit()
    return jsonify({'mensagem': 'Peça criada com sucesso', 'peca': peca.para_dic()}), 201


@pecas_bp.route('/pecas/<int:id>', methods=['PUT'])
def atualizar(id):
    peca = Peca.query.get(id)
    if not peca:
        return jsonify({'erro': 'Peça não encontrada'}), 404

    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400

    if 'nome'               in d: peca.nome               = d['nome']
    if 'descricao'          in d: peca.descricao          = d['descricao']
    if 'valor_unitario'     in d: peca.valor_unitario     = d['valor_unitario']
    if 'quantidade_estoque' in d: peca.quantidade_estoque = d['quantidade_estoque']

    db.session.commit()
    return jsonify({'mensagem': 'Peça atualizada com sucesso', 'peca': peca.para_dic()}), 200


@pecas_bp.route('/pecas/<int:id>', methods=['DELETE'])
def deletar(id):
    peca = Peca.query.get(id)
    if not peca:
        return jsonify({'erro': 'Peça não encontrada'}), 404

    db.session.delete(peca)
    db.session.commit()
    return jsonify({'mensagem': 'Peça deletada com sucesso'}), 200
