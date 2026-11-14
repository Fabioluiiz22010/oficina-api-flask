from db import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome      = db.Column(db.String(200), nullable=False)
    telefone  = db.Column(db.String(20),  nullable=True)
    email     = db.Column(db.String(200), nullable=True)
    endereco  = db.Column(db.String(300), nullable=True)

    veiculos  = db.relationship("Veiculo", backref="cliente", lazy=True)

    def para_dic(self):
        return {
            "id":       self.id,
            "nome":     self.nome,
            "telefone": self.telefone,
            "email":    self.email,
            "endereco": self.endereco
        }


class Veiculo(db.Model):
    __tablename__ = "veiculos"

    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    placa          = db.Column(db.String(10),  nullable=False)
    marca          = db.Column(db.String(100), nullable=False)
    modelo         = db.Column(db.String(100), nullable=False)
    ano            = db.Column(db.Integer,     nullable=False)
    cor            = db.Column(db.String(50),  nullable=True)
    quilometragem  = db.Column(db.Float,       nullable=True, default=0)
    cliente_id     = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    def para_dic(self):
        return {
            "id":            self.id,
            "placa":         self.placa,
            "marca":         self.marca,
            "modelo":        self.modelo,
            "ano":           self.ano,
            "cor":           self.cor,
            "quilometragem": self.quilometragem,
            "cliente_id":    self.cliente_id
        }


class Peca(db.Model):
    __tablename__ = "pecas"

    id                 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome               = db.Column(db.String(200), nullable=False)
    descricao          = db.Column(db.String(500), nullable=True)
    valor_unitario     = db.Column(db.Float,       nullable=True, default=0)
    quantidade_estoque = db.Column(db.Integer,     nullable=True, default=0)

    def para_dic(self):
        return {
            "id":                 self.id,
            "nome":               self.nome,
            "descricao":          self.descricao,
            "valor_unitario":     self.valor_unitario,
            "quantidade_estoque": self.quantidade_estoque
        }


class Servico(db.Model):
    __tablename__ = "servicos"

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome      = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)
    valor     = db.Column(db.Float,       nullable=True, default=0)

    def para_dic(self):
        return {
            "id":        self.id,
            "nome":      self.nome,
            "descricao": self.descricao,
            "valor":     self.valor
        }


class OrdemServico(db.Model):
    __tablename__ = "ordemservicos"

    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataEntrada      = db.Column(db.Date,    nullable=False)
    dataSaida        = db.Column(db.Date,    nullable=True)
    status           = db.Column(db.String(50), nullable=False)
    quilometragemOS  = db.Column(db.Float,   nullable=True)
    valorTotal       = db.Column(db.Float,   nullable=True, default=0)
    veiculo_id       = db.Column(db.Integer, db.ForeignKey("veiculos.id"),  nullable=False)
    servico_id       = db.Column(db.Integer, db.ForeignKey("servicos.id"),  nullable=False)
    peca_id          = db.Column(db.Integer, db.ForeignKey("pecas.id"),     nullable=False)

    def para_dic(self):
        return {
            "id":              self.id,
            "dataEntrada":     str(self.dataEntrada),
            "dataSaida":       str(self.dataSaida) if self.dataSaida else None,
            "status":          self.status,
            "quilometragemOS": self.quilometragemOS,
            "valorTotal":      self.valorTotal,
            "veiculo_id":      self.veiculo_id,
            "servico_id":      self.servico_id,
            "peca_id":         self.peca_id
        }
