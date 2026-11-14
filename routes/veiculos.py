from flask import Blueprint, request, jsonify
from db import db
from models import Veiculo

veiculos_bp = Blueprint('veiculos', __name__)


@veiculos_bp.route('/veiculos', methods=['GET'])
def listar():
    veiculos = Veiculo.query.all()
    return jsonify({
        "veiculos": [v.para_dic() for v in veiculos],
        "total":    len(veiculos)
    }), 200


@veiculos_bp.route('/veiculos/<int:id>', methods=['GET'])
def buscar(id):
    veiculo = Veiculo.query.get(id)
    if not veiculo:
        return jsonify({'erro': 'Veículo não encontrado'}), 404
    return jsonify({"veiculo": veiculo.para_dic()}), 200


@veiculos_bp.route('/veiculos', methods=['POST'])
def criar():
    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400
    for campo in ('placa', 'marca', 'modelo', 'ano', 'cliente_id'):
        if not d.get(campo):
            return jsonify({'erro': f"O campo '{campo}' é obrigatório"}), 400

    veiculo = Veiculo(
        placa         = d['placa'],
        marca         = d['marca'],
        modelo        = d['modelo'],
        ano           = d['ano'],
        cor           = d.get('cor'),
        quilometragem = d.get('quilometragem', 0),
        cliente_id    = d['cliente_id']
    )
    db.session.add(veiculo)
    db.session.commit()
    return jsonify({'mensagem': 'Veículo criado com sucesso', 'veiculo': veiculo.para_dic()}), 201


@veiculos_bp.route('/veiculos/<int:id>', methods=['PUT'])
def atualizar(id):
    veiculo = Veiculo.query.get(id)
    if not veiculo:
        return jsonify({'erro': 'Veículo não encontrado'}), 404

    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400

    if 'placa'         in d: veiculo.placa         = d['placa']
    if 'marca'         in d: veiculo.marca         = d['marca']
    if 'modelo'        in d: veiculo.modelo        = d['modelo']
    if 'ano'           in d: veiculo.ano           = d['ano']
    if 'cor'           in d: veiculo.cor           = d['cor']
    if 'quilometragem' in d: veiculo.quilometragem = d['quilometragem']
    if 'cliente_id'    in d: veiculo.cliente_id    = d['cliente_id']

    db.session.commit()
    return jsonify({'mensagem': 'Veículo atualizado com sucesso', 'veiculo': veiculo.para_dic()}), 200


@veiculos_bp.route('/veiculos/<int:id>', methods=['DELETE'])
def deletar(id):
    veiculo = Veiculo.query.get(id)
    if not veiculo:
        return jsonify({'erro': 'Veículo não encontrado'}), 404

    db.session.delete(veiculo)
    db.session.commit()
    return jsonify({'mensagem': 'Veículo deletado com sucesso'}), 200
