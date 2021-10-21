from abc import ABCMeta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Dao:
    __metaclass__ = ABCMeta

    def __init__(self):
        engine = create_engine('mysql+pymysql://root:@localhost/teste?charset=utf8', echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create(self, entidade):
        try:
            self.session.add(entidade)
            self.session.commit()
            self.session.refresh(entidade)
            return entidade.id
        except Exception as e:
            self.session.rollback()
            raise Exception('Erro ao Salvar - Contatar ADM')

    def update(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception('Erro ao Atualizar - Contatar ADM')

    def remove(self, entidade):
        try:
            entidade.ativo = False
            self.update()
            # self.session.delete(entidade)
            # self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception('Erro ao Remover - Contatar ADM')

    def search_id(self, Entidade, id):
        try:
            entidade = self.session.query(Entidade).filter(Entidade.id == id).first()
            return entidade
        except Exception as e:
            raise Exception('Erro ao Buscar - Contatar ADM')

    def search_all(self, Entidade):
        try:
            list = self.session.query(Entidade).all()
            return list
        except Exception as e:
            raise Exception('Erro ao Buscar - Contatar ADM')
