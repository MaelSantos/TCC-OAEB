from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..models import Backup, Grafico


def tratar_vazios(valor):
    if valor is None:
        return "%%"
    else:
        return '%' + valor + '%'


class DaoBackup:
    url = "mysql+pymysql://{username}:{password}@{server}/oaeb?charset=utf8".format(username='root', password='', server='localhost')

    # url = "mysql+pymysql://kroqjy9qcxtwux34:hbp7tay1ksl0kjri@ckshdphy86qnz0bj.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/heze020iv1fe39gt?charset=utf8"

    engine = create_engine(url, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    def salvar(self, backup):
        try:
            self.session.add(backup)
            self.session.commit()
            self.session.refresh(backup)
            return backup.id
        except Exception as e:
            self.session.rollback()
            raise Exception('Erro ao Salvar Backup - Contatar ADM')

    def buscar_backup(self, base_principal='', base_secundaria='', municipio='', orgao='',
               tipo_cruzamento='', periodo_de='', periodo_ate='', nome='', nis=''):
        try:
            return self.session.query(Backup).filter(
                Backup.base_principal.like(tratar_vazios(base_principal))) \
                .filter(Backup.base_secundaria.like(tratar_vazios(base_secundaria))) \
                .filter(Backup.municipio.like(tratar_vazios(municipio))) \
                .filter(Backup.orgao.like(tratar_vazios(orgao))) \
                .filter(Backup.tipo_cruzamento.like(tratar_vazios(tipo_cruzamento))) \
                .filter(Backup.periodo_de.like(tratar_vazios(periodo_de))) \
                .filter(Backup.periodo_ate.like(tratar_vazios(periodo_ate))) \
                .filter(Backup.nome.like(tratar_vazios(nome))) \
                .filter(Backup.nis.like(tratar_vazios(nis))).first()
        except Exception as e:
            self.session.rollback()
            raise Exception('Erro ao Buscar Backup - Contatar ADM')

    def buscar_grafico(self, tipo='', municipio='', periodo_de='', periodo_ate=''):
        try:
            return self.session.query(Grafico)\
                .filter(Grafico.municipio.like(tratar_vazios(municipio))) \
                .filter(Grafico.tipo.like(tratar_vazios(tipo))) \
                .filter(Grafico.periodo_de.like(tratar_vazios(periodo_de))) \
                .filter(Grafico.periodo_ate.like(tratar_vazios(periodo_ate))).first()
        except Exception as e:
            self.session.rollback()
            raise Exception('Erro ao Buscar Backup - Contatar ADM')
