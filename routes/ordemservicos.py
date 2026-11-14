from flask import Blueprint, request, jsonify
from db import db
from models import OrdemServico

os_bp = Blueprint('ordemservicos', __name__)


@os_bp.route('/ordemservicos', methods=['GET'])
def listar():
    ordens = OrdemServico.query.all()
    return jsonify({
        "ordemservicos": [o.para_dic() for o in ordens],
        "total":         len(ordens)
    }), 200


@os_bp.route('/ordemservicos/<int:id>', methods=['GET'])
def buscar(id):
    ordem = OrdemServico.query.get(id)
    if not ordem:
        return jsonify({'erro': 'Ordem de serviço não encontrada'}), 404
    return jsonify({"ordemservico": ordem.para_dic()}), 200


@os_bp.route('/ordemservicos', methods=['POST'])
def criar():
    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400
    for campo in ('dataEntrada', 'status', 'veiculo_id', 'servico_id', 'peca_id'):
        if not d.get(campo):
            return jsonify({'erro': f"O campo '{campo}' é obrigatório"}), 400

    ordem = OrdemServico(
        dataEntrada     = d['dataEntrada'],
        dataSaida       = d.get('dataSaida'),
        status          = d['status'],
        quilometragemOS = d.get('quilometragemOS'),
        valorTotal      = d.get('valorTotal', 0),
        veiculo_id      = d['veiculo_id'],
        servico_id      = d['servico_id'],
        peca_id         = d['peca_id']
    )
    db.session.add(ordem)
    db.session.commit()
    return jsonify({'mensagem': 'OS criada com sucesso', 'ordemservico': ordem.para_dic()}), 201


@os_bp.route('/ordemservicos/<int:id>', methods=['PUT'])
def atualizar(id):
    ordem = OrdemServico.query.get(id)
    if not ordem:
        return jsonify({'erro': 'Ordem de serviço não encontrada'}), 404

    d = request.get_json()
    if not d:
        return jsonify({'erro': 'Requisição deve conter um JSON válido'}), 400

    if 'dataEntrada'     in d: ordem.dataEntrada     = d['dataEntrada']
    if 'dataSaida'       in d: ordem.dataSaida       = d['dataSaida']
    if 'status'          in d: ordem.status          = d['status']
    if 'quilometragemOS' in d: ordem.quilometragemOS = d['quilometragemOS']
    if 'valorTotal'      in d: ordem.valorTotal      = d['valorTotal']
    if 'veiculo_id'      in d: ordem.veiculo_id      = d['veiculo_id']
    if 'servico_id'      in d: ordem.servico_id      = d['servico_id']
    if 'peca_id'         in d: ordem.peca_id         = d['peca_id']

    db.session.commit()
    return jsonify({'mensagem': 'OS atualizada com sucesso', 'ordemservico': ordem.para_dic()}), 200


@os_bp.route('/ordemservicos/<int:id>', methods=['DELETE'])
def deletar(id):
    ordem = OrdemServico.query.get(id)
    if not ordem:
        return jsonify({'erro': 'Ordem de serviço não encontrada'}), 404

    db.session.delete(ordem)
    db.session.commit()
    return jsonify({'mensagem': 'OS deletada com sucesso'}), 200
