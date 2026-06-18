# workshop/admin.py
from django.contrib import admin
from .models import Owner, Loja, Seccao, Fornecedor, Produto, Venda, VendeSe, Contacto, Evento


# ── Inlines ────────────────────────────────────────────────────────────────────

class LojaInline(admin.TabularInline):
    model = Loja
    extra = 0
    fields = ('nomeloja', 'localizacao', 'capitalsocial', 'emailloja', 'contacto')
    show_change_link = True


class SeccaoInline(admin.TabularInline):
    model = Seccao
    extra = 0
    fields = ('nome',)
    show_change_link = True


class ProdutoInline(admin.TabularInline):
    model = Produto
    extra = 0
    fields = ('nome', 'preco', 'qtd', 'desconto', 'iva', 'oculto', 'seccao', 'fornecedor')
    show_change_link = True


class VendeSeInline(admin.TabularInline):
    model = VendeSe
    extra = 0
    fields = ('produto', 'qtd', 'preco')
    autocomplete_fields = ('produto',)


# ── ModelAdmins ────────────────────────────────────────────────────────────────

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display  = ('cc', 'name', 'birth', 'email', 'contact', 'morada', 'loja_count')
    search_fields = ('name', 'email')
    ordering      = ('name',)
    inlines       = [LojaInline]

    @admin.display(description='Lojas')
    def loja_count(self, obj):
        return obj.lojas.count()


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display   = ('nomeloja', 'localizacao', 'capitalsocial', 'emailloja', 'contacto', 'owner', 'oculta')
    search_fields  = ('nomeloja', 'emailloja', 'owner__name')
    list_filter    = ('owner', 'oculta')
    list_editable  = ('oculta',)
    autocomplete_fields = ('owner',)
    ordering       = ('nomeloja',)
    inlines        = [SeccaoInline, ProdutoInline]


@admin.register(Seccao)
class SeccaoAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'loja', 'produto_count')
    search_fields = ('nome', 'loja__nomeloja')
    list_filter   = ('loja',)
    autocomplete_fields = ('loja',)
    ordering      = ('nome',)
    inlines       = [ProdutoInline]

    @admin.display(description='Produtos')
    def produto_count(self, obj):
        return obj.produtos.count()


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display  = ('nif', 'nome', 'email', 'contacto', 'morada', 'produto_count')
    search_fields = ('nome', 'email', 'nif')
    ordering      = ('nome',)

    @admin.display(description='Produtos')
    def produto_count(self, obj):
        return obj.produtos.count()


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display   = ('id', 'nome', 'preco', 'qtd', 'desconto', 'iva', 'oculto', 'seccao', 'loja', 'fornecedor')
    search_fields  = ('nome', 'seccao__nome', 'loja__nomeloja', 'fornecedor__nome')
    list_filter    = ('oculto', 'iva', 'seccao', 'loja', 'fornecedor')
    list_editable  = ('preco', 'qtd', 'oculto')
    autocomplete_fields = ('seccao', 'loja', 'fornecedor')
    ordering       = ('nome',)
    fieldsets = (
        ('Informação Geral', {
            'fields': ('nome', 'seccao', 'loja', 'fornecedor', 'oculto')
        }),
        ('Preço & Stock', {
            'fields': ('preco', 'qtd', 'desconto', 'iva')
        }),
    )

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display  = (
        'recibo',
        'data',
        'total',
        'metodo_pagamento_admin',
        'num_produtos',
    )
    search_fields = ('recibo',)
    list_filter   = ('data', 'metodo_pagamento')
    date_hierarchy = 'data'
    ordering      = ('-data',)
    inlines       = [VendeSeInline]
    actions       = ['apagar_vendas']

    @admin.display(description='Pagamento')
    def metodo_pagamento_admin(self, obj):
        if obj.metodo_pagamento == 'mbway':
            if obj.contacto:
                return f'📱 MBWay · {obj.contacto.nome} ({obj.contacto.telefone})'
            return '📱 MBWay'
        return '💵 Dinheiro'

    @admin.display(description='Nº Produtos')
    def num_produtos(self, obj):
        return obj.linhas.count()

    @admin.action(description='Apagar vendas selecionadas (com linhas)')
    def apagar_vendas(self, request, queryset):
        for venda in queryset:
            venda.linhas.all().delete()
            venda.delete()
        self.message_user(request, f'{queryset.count()} venda(s) apagada(s).')

    @admin.display(description='Nº Produtos')
    def num_produtos(self, obj):
        return obj.linhas.count()

@admin.register(VendeSe)
class VendeSeAdmin(admin.ModelAdmin):
    list_display   = ('venda', 'produto', 'qtd', 'preco')
    search_fields  = ('venda__recibo', 'produto__nome')
    list_filter    = ('produto__seccao', 'produto__loja')
    autocomplete_fields = ('venda', 'produto')
    ordering       = ('venda',)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'loja', 'data_inicio', 'data_fim', 'ativo')
    list_filter   = ('loja', 'ativo')
    list_editable = ('ativo',)
    ordering      = ('loja', '-data_inicio')
    fields        = ('nome', 'loja', 'data_inicio', 'data_fim', 'ativo')

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone')
    search_fields = ('nome', 'telefone')
