from django.db import models
from django.db.models import AutoField


class Owner(models.Model):
    cc = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=512)
    birth = models.DateField()
    email = models.CharField(max_length=512)
    contact = models.IntegerField()
    morada = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'owner'


class Loja(models.Model):
    nomeloja = models.CharField(max_length=512, primary_key=True)
    localizacao = models.CharField(max_length=512)
    capitalsocial = models.IntegerField()
    emailloja = models.CharField(max_length=512)
    contacto = models.IntegerField()
    owner = models.ForeignKey(
        Owner,
        on_delete=models.RESTRICT,
        db_column='owner_cc',
        related_name='lojas'
    )

    def __str__(self):
        return self.nomeloja

    class Meta:
        db_table = 'loja'


class Seccao(models.Model):
    nome = models.CharField(max_length=512, primary_key=True)
    loja = models.ForeignKey(
        Loja,
        on_delete=models.RESTRICT,
        db_column='loja_nomeloja',
        related_name='seccoes',
        null=True,
    )

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'seccao'


class Fornecedor(models.Model): 
    nif = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=512)
    email = models.CharField(max_length=512)
    contacto = models.IntegerField()
    morada = models.CharField(max_length=512)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'fornecedor'


class Produto(models.Model):
    id = AutoField(primary_key=True)
    nome = models.CharField(max_length=512)
    preco = models.FloatField()  
    qtd = models.IntegerField()
    desconto = models.IntegerField()
    iva = models.IntegerField()
    oculto = models.BooleanField(default=False)
    seccao = models.ForeignKey(
        Seccao,
        on_delete=models.RESTRICT,
        db_column='seccao_nome',
        related_name='produtos'
    )
    loja = models.ForeignKey(
        Loja,
        on_delete=models.RESTRICT,
        db_column='loja_nomeloja',
        related_name='produtos',
        null=True,
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.RESTRICT,
        db_column='fornecedor_nif',
        related_name='produtos',
        null=True,
    )

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'produto'

class Venda(models.Model):
    METODO_CHOICES = [('dinheiro', 'Dinheiro'), ('mbway', 'MBWay')]
    recibo = models.BigIntegerField(primary_key=True)
    total = models.FloatField()          # ← era BigIntegerField
    data = models.DateTimeField()        # ← era DateField, perdes a hora!
    metodo_pagamento = models.CharField(max_length=20, choices=METODO_CHOICES, default='dinheiro')
    contacto = models.ForeignKey(
        'Contacto',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='vendas'
    )

    def __str__(self):
        return f"Recibo {self.recibo}"

    class Meta:
        db_table = 'venda'

class VendeSe(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.RESTRICT, db_column='venda_recibo', related_name='linhas')
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT, db_column='produto_id', related_name='linhas_venda')
    qtd = models.IntegerField()
    preco = models.FloatField()

    def __str__(self):
        return f"Venda {self.venda_id} — Produto {self.produto_id}"

    class Meta:
        db_table = 'vende_se'
        unique_together = [('venda', 'produto')]

class Contacto(models.Model):
    nome = models.CharField(max_length=512)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nome} ({self.telefone})"

    class Meta:
        db_table = 'contacto'
