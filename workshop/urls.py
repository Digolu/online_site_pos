# workshop/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('selecionar_loja/', views.selecionar_loja, name='selecionar_loja'),
    path('nova_venda/', views.nova_venda, name='nova_venda'),
    path('lista_vendas/', views.lista_vendas, name='lista_vendas'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('produtosHTML/', views.produtosHTMLFUNC, name='produtosHTML'),
    path('produtosTESTE/', views.produtosTESTEFUNC, name='produtosTESTE'),
    path('vendasTESTE/', views.vendasTESTEFUNC, name='vendasTESTE'),
    path('exportar_vendas/', views.exportar_vendas, name='exportar_vendas'),
    path('limpar_vendas/', views.limpar_vendas, name='limpar_vendas'),
    path('lojas/', views.lista_lojas, name='lista_lojas'),
    path('owners/', views.lista_owners, name='lista_owners'),
    path('trocar_loja/', views.trocar_loja, name='trocar_loja'),
    path('adicionar_produto/', views.adicionar_produto, name='adicionar_produto'),
    path('adicionar_seccao/', views.adicionar_seccao, name='adicionar_seccao'),
    path('loja/adicionar/', views.adicionar_loja, name='adicionar_loja'),
    path('loja/remover/<str:nomeloja>/', views.remover_loja, name='remover_loja'),
    path('owner/adicionar/', views.adicionar_owner, name='adicionar_owner'),
    path('adicionar_fornecedor/', views.adicionar_fornecedor, name='adicionar_fornecedor'),
    path('editar_produto/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('ocultar_produto/<int:produto_id>/', views.ocultar_produto, name='ocultar_produto'),
    path('get_produto/<int:produto_id>/', views.get_produto, name='get_produto'),
]