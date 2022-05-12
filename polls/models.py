from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, JSON
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# url = "mysql+pymysql://{username}:{password}@{server}/oaeb?charset=utf8".format(username='root', password='',
#                                                                                 server='localhost')
# url = "mysql+pymysql://bc84b4f22d6208:e7ae88a3@us-cdbr-east-05.cleardb.net/heroku_3dc95edc67d0294?charset=utf8"

url = "mysql+pymysql://kroqjy9qcxtwux34:hbp7tay1ksl0kjri@ckshdphy86qnz0bj.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/heze020iv1fe39gt?charset=utf8"

engine = create_engine(url, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Backup(Base):
    __tablename__ = 'backup'

    id = Column(Integer, primary_key=True)
    base_principal = Column(String(50))
    base_secundaria = Column(String(50))
    municipio = Column(String(50))
    orgao = Column(String(50))
    tipo_cruzamento = Column(String(50))
    periodo_de = Column(String(50))
    periodo_ate = Column(String(50))
    nome = Column(String(50))
    nis = Column(String(50))

    resultado = Column(JSON, nullable=True)

    def __str__(self):
        return self.municipio + " - " + self.base_principal


Base.metadata.create_all(engine)
