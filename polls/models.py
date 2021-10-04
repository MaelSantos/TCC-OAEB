from django.db import models


class Endereco(models.Model):
    municipio = models.CharField(max_length=200, unique=True, null=True)
    codigo_municipio = models.IntegerField(unique=True, null=True)
    codigo_siafi = models.IntegerField(unique=True, null=True)
    uf = models.CharField(max_length=2)  # UF

    def __str__(self):
        return self.municipio


class BeneficiarioAuxilio(models.Model):
    nome_beneficiario = models.CharField(max_length=100)
    cpf_beneficiario = models.CharField(max_length=14)
    nis = models.CharField(max_length=20, null=True)
    responsavel = models.CharField(max_length=100, null=True)
    cpf_responsavel = models.CharField(max_length=14, null=True)
    nis_responsavel = models.CharField(max_length=100, null=True)
    enquadramento = models.CharField(max_length=100)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_beneficiario


class Beneficio(models.Model):
    parcela = models.CharField(max_length=4)
    mes = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    observacao = models.CharField(max_length=200, null=True)
    beneficiario = models.ForeignKey(BeneficiarioAuxilio, on_delete=models.CASCADE)

    def __str__(self):
        return self.mes


class BeneficiarioBolsaFamilia(models.Model):
    mes_referencia = models.CharField(max_length=6)  # MÊS REFERÊNCIA
    mes_competencia = models.CharField(max_length=6)  # MÊS COMPETÊNCIA
    cpf = models.CharField(max_length=14, null=True)  # CPF FAVORECIDO
    nis = models.CharField(max_length=20)  # NIS FAVORECIDO
    nome_favorecido = models.CharField(max_length=100)  # NOME FAVORECIDO
    valor = models.DecimalField(max_digits=8, decimal_places=2)  # VALOR PARCELA
    # codigo_municipio = models.IntegerField() #CÓDIGO MUNICÍPIO SIAFI
    # nome_municipio = models.CharField(max_length=100) #NOME MUNICÍPIO
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_favorecido
