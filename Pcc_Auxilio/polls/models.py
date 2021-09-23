from django.db import models


class Endereco(models.Model):
    municipio = models.CharField(max_length=200)
    codigo_municipio = models.CharField(max_length=200)

class Beneficiario(models.Model):
    nome_beneficiario = models.CharField(max_length=200)
    cpf_beneficiario = models.CharField(max_length=200)
    nis = models.CharField(max_length=200)
    resposnsavel = models.CharField(max_length=200)
    cpf_responsavel = models.CharField(max_length=200)
    nis_responsavel = models.CharField(max_length=200)
    enquadramento = models.CharField(max_length=200)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

class Beneficio(models.Model):
    parcela = models.CharField(max_length=200)
    mes = models.CharField(max_length=200)
    valor = models.CharField(max_length=200)
    observacao = models.CharField(max_length=200)
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
