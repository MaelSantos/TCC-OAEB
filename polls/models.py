from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# url = "mysql://{username}:{password}@{server}/teste?charset=utf8".format('root', '', 'localhost')
engine = create_engine('mysql+pymysql://root:@localhost/teste?charset=utf8', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Endereco(Base):
    __tablename__ = 'endereco'

    id = Column(Integer, primary_key=True)
    municipio = Column(String(200), unique=True, nullable=True)
    codigo_municipio = Column(Integer, unique=True, nullable=True)
    codigo_siafi = Column(Integer, unique=True, nullable=True)
    uf = Column(String(2))  # UF

    # bf_auxilio = relationship(BeneficiarioAuxilio, backref="users")
    # bf_bolsa = relationship(BeneficiarioBolsaFamilia, backref="users")

    def __str__(self):
        return self.municipio


class BeneficiarioAuxilio(Base):
    __tablename__ = 'beneficiario_auxilio'

    id = Column(Integer, primary_key=True)
    nome_beneficiario = Column(String(100))
    cpf_beneficiario = Column(String(14))
    nis = Column(String(20), nullable=True)
    responsavel = Column(String(100), nullable=True)
    cpf_responsavel = Column(String(14), nullable=True)
    nis_responsavel = Column(String(100), nullable=True)
    enquadramento = Column(String(100))
    endereco_id = Column(Integer, ForeignKey('endereco.id'))
    endereco = relationship('Endereco')

    def __str__(self):
        return self.nome_beneficiario


class Beneficio(Base):
    __tablename__ = 'beneficio'

    id = Column(Integer, primary_key=True)
    parcela = Column(String(4))
    mes = Column(String(200))
    valor = Column(Numeric(8, 2))
    observacao = Column(String(200), nullable=True)

    beneficiario_id = Column(Integer, ForeignKey('beneficiario_auxilio.id'))
    beneficiario = relationship('BeneficiarioAuxilio')

    def __str__(self):
        return self.mes


class BeneficiarioBolsaFamilia(Base):
    __tablename__ = 'beneficiario_bolsa_familia'

    id = Column(Integer, primary_key=True)
    mes_referencia = Column(String(6))  # MÊS REFERÊNCIA
    mes_competencia = Column(String(6))  # MÊS COMPETÊNCIA
    cpf = Column(String(14), nullable=True)  # CPF FAVORECIDO
    nis = Column(String(20))  # NIS FAVORECIDO
    nome_favorecido = Column(String(100))  # NOME FAVORECIDO
    valor = Column(Numeric(8, 2))  # VALOR PARCELA
    endereco_id = Column(Integer, ForeignKey('endereco.id'))
    endereco = relationship('Endereco')

    def __str__(self):
        return self.nome_favorecido


class BolsaFamilia(Base):
    __tablename__ = 'bolsa_familia'

    id = Column(Integer, primary_key=True)
    uf = Column(String(2))
    municipio = Column(String(50))
    cpf = Column(String(20))
    nis = Column(String(20))
    nome = Column(String(100))
    valor = Column(String(20))

    def __str__(self):
        return f"ID: {self.id} - NOME: {self.nome} - NIS: {self.nis} - VALOR: {self.valor}"


class AuxilioEmergencial(Base):
    __tablename__ = 'auxilio_emergencial'

    id = Column(Integer, primary_key=True)
    uf = Column(String(2))
    municipio = Column(String(50))
    cpf = Column(String(20))
    nis = Column(String(20))
    nome = Column(String(100))
    observacao = Column(String(100))
    valor = Column(String(20))

    def __str__(self):
        return f"ID: {self.id} - NOME: {self.nome} - NIS: {self.nis} - VALOR: {self.valor}"


Base.metadata.create_all(engine)
