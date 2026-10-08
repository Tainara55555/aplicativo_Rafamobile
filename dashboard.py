import flet as ft

from pages.clientes import mostrar_clientes
from pages.servicos import mostrar_servicos
from pages.caixa import mostrar_caixa
from pages.relatorios import mostrar_relatorios
from pages.registros import mostrar_registros

from database import (
    listar_servicos_painel,
    saldo_servico,
)


# ==============================
# CORES
# ==============================

LARANJA = "#F75E00"
FUNDO = "#000000"
MENU = "#202020"
CARD = "#242424"
BRANCO = "#FFFFFF"
CINZA = "#AAAAAA"
VERDE = "#22C55E"
VERMELHO = "#EF4444"


# ==============================
# FUNÇÕES AUXILIARES
# ==============================

def formatar_moeda(valor):

    valor = float(valor or 0)

    texto = f"{valor:,.2f}"

    texto = texto.replace(",", "X")
    texto = texto.replace(".", ",")
    texto = texto.replace("X", ".")

    return f"R$ {texto}"


# ==============================
# DASHBOARD
# ==============================

def mostrar_dashboard(page: ft.Page):

    page.controls.clear()

    page.title = "Rafá Mobile"

    page.bgcolor = FUNDO

    page.padding = 0

    # ==========================================
    # ÁREA DE CONTEÚDO
    # ==========================================

    area_conteudo = ft.Container(
        expand=True,
        bgcolor=FUNDO,
        padding=0,
    )

    # ==========================================
    # FUNÇÃO PARA PREPARAR A ÁREA DE CONTEÚDO
    # ==========================================

    def preparar_area(conteudo):

        return ft.Container(
            expand=True,
            bgcolor=FUNDO,
            padding=30,
            content=conteudo,
        )

    # ==========================================
    # MOSTRAR CONTEÚDO
    # ==========================================

    def mostrar_conteudo(conteudo):

        area_conteudo.content = preparar_area(
            conteudo
        )

        area_conteudo.bgcolor = FUNDO

        page.update()

    # ==========================================
    # ÁREA PARA ABRIR CLIENTES
    # ==========================================

    def abrir_clientes(e=None):

        mostrar_clientes(
            page,
            area_conteudo,
        )

    # ==========================================
    # ÁREA PARA ABRIR SERVIÇOS
    # ==========================================

    def abrir_servicos(e=None):

        mostrar_servicos(
            page,
            area_conteudo,
        )

    # ==========================================
    # ÁREA PARA ABRIR CAIXA
    # ==========================================

    def abrir_caixa(e=None):

        mostrar_caixa(
            page,
            area_conteudo,
        )

    # ==========================================
    # ÁREA PARA ABRIR CONTRATOS / NOTAS FISCAIS
    # ==========================================

    def abrir_registros(e=None):

        mostrar_registros(
            page,
            area_conteudo,
        )

    # ==========================================
    # ABRIR FICHA DO SERVIÇO
    # ==========================================

    def abrir_servico(id_servico):

        mostrar_servicos(
            page,
            area_conteudo,
            id_servico_abrir=id_servico,
        )

    # ==========================================
    # CRIAR CARD DE SERVIÇO
    # ==========================================

    def criar_card_servico(servico):

        id_servico = servico["id"]

        nome_cliente = (
            servico["nome_cliente"]
            or "Cliente não informado"
        )

        descricao = (
            servico["descricao"]
            or "Sem descrição"
        )

        saldo = saldo_servico(
            id_servico
        )

        # --------------------------------------
        # COR DO SALDO
        # --------------------------------------

        cor_saldo = (
            VERDE
            if saldo >= 0
            else VERMELHO
        )

        texto_saldo = formatar_moeda(
            saldo
        )

        # ======================================
        # BLOCO SALDO
        # ======================================

        bloco_saldo = ft.Container(

            bgcolor="#19351F",

            border_radius=8,

            padding=15,

            content=ft.Column(

                controls=[

                    ft.Text(
                        "Saldo atual",
                        size=12,
                        color=CINZA,
                    ),

                    ft.Text(
                        texto_saldo,
                        size=20,
                        color=cor_saldo,
                        weight=ft.FontWeight.BOLD,
                    ),

                ],

                spacing=5,

                tight=True,

            ),

        )

        # ======================================
        # CARD COMPLETO
        # ======================================

        return ft.Container(

            bgcolor=CARD,

            border_radius=12,

            padding=20,

            margin=ft.Margin.only(
                bottom=12
            ),

            content=ft.Column(

                controls=[

                    # ==================================
                    # CABEÇALHO
                    # ==================================

                    ft.Row(

                        controls=[

                            ft.Column(

                                controls=[

                                    ft.Text(
                                        f"Serviço #{id_servico}",
                                        size=12,
                                        color=CINZA,
                                        weight=ft.FontWeight.BOLD,
                                    ),

                                    ft.Text(
                                        nome_cliente,
                                        size=20,
                                        color=BRANCO,
                                        weight=ft.FontWeight.BOLD,
                                    ),

                                ],

                                spacing=4,

                                tight=True,

                            ),

                            ft.Container(
                                expand=True,
                            ),

                            ft.Button(

                                "Abrir serviço",

                                icon=ft.Icons.OPEN_IN_NEW,

                                bgcolor=LARANJA,

                                color=BRANCO,

                                on_click=lambda e,
                                sid=id_servico:

                                    abrir_servico(sid),

                            ),

                        ],

                        spacing=15,

                    ),

                    # ==================================
                    # DESCRIÇÃO
                    # ==================================

                    ft.Text(
                        descricao,
                        size=14,
                        color=CINZA,
                    ),

                    # ==================================
                    # SALDO
                    # ==================================

                    bloco_saldo,

                ],

                spacing=12,

                tight=True,

            ),

        )

    # ==========================================
    # INÍCIO / PAINEL PRINCIPAL
    # ==========================================

    def mostrar_inicio(e=None):

        # --------------------------------------
        # BUSCAR SERVIÇOS DO PAINEL
        # --------------------------------------

        servicos = listar_servicos_painel()

        # --------------------------------------
        # TÍTULO
        # --------------------------------------

        titulo = ft.Text(

            "Painel principal",

            size=28,

            weight=ft.FontWeight.BOLD,

            color=BRANCO,

        )

        subtitulo = ft.Text(

            "Serviços adicionados ao painel principal",

            size=14,

            color=CINZA,

        )

        # --------------------------------------
        # LISTA DOS CARDS
        # --------------------------------------

        controles_servicos = []

        for servico in servicos:

            controles_servicos.append(

                criar_card_servico(
                    servico
                )

            )

        # --------------------------------------
        # NENHUM SERVIÇO
        # --------------------------------------

        if not controles_servicos:

            controles_servicos.append(

                ft.Container(

                    bgcolor=CARD,

                    border_radius=12,

                    padding=30,

                    content=ft.Column(

                        controls=[

                            ft.Text(

                                "Nenhum serviço no painel principal",

                                size=18,

                                color=BRANCO,

                                weight=ft.FontWeight.BOLD,

                            ),

                            ft.Text(

                                "Adicione um serviço ao painel principal pela tela de Serviços.",

                                size=14,

                                color=CINZA,

                            ),

                        ],

                        horizontal_alignment=(

                            ft.CrossAxisAlignment.CENTER

                        ),

                        spacing=10,

                        tight=True,

                    ),

                )

            )

        # --------------------------------------
        # LISTA DOS CARDS
        # --------------------------------------

        lista_cards = ft.Column(

            controls=controles_servicos,

            spacing=0,

            tight=True,

        )

        # --------------------------------------
        # CONTEÚDO DO PAINEL
        # --------------------------------------

        conteudo_inicio = ft.Column(

            controls=[

                titulo,

                subtitulo,

                ft.Container(
                    height=20,
                ),

                lista_cards,

            ],

            spacing=8,

            scroll=ft.ScrollMode.AUTO,

            expand=True,

        )

        mostrar_conteudo(
            conteudo_inicio
        )

    # ==========================================
    # MENU
    # ==========================================

    def item_menu(
        icone,
        texto,
        acao
    ):

        return ft.Container(

            padding=12,

            border_radius=8,

            on_click=acao,

            content=ft.Row(

                controls=[

                    ft.Text(
                        icone,
                        size=20,
                    ),

                    ft.Text(
                        texto,
                        size=14,
                        color=BRANCO,
                    ),

                ],

                spacing=12,

            ),

        )

    # ==========================================
    # LOGO
    # ==========================================

    logo = ft.Image(

        src="logo.png",

        width=150,

        height=90,

        fit=ft.BoxFit.CONTAIN,

    )

    # ==========================================
    # TÍTULO DO MENU
    # ==========================================

    titulo_menu = ft.Text(

        "MENU",

        size=11,

        color=CINZA,

        weight=ft.FontWeight.BOLD,

    )

    # ==========================================
    # MENU LATERAL
    # ==========================================

    menu = ft.Container(

        width=230,

        bgcolor=MENU,

        padding=20,

        content=ft.Column(

            controls=[

                logo,

                ft.Container(
                    height=20,
                ),

                titulo_menu,

                # ----------------------------------
                # INÍCIO
                # ----------------------------------

                item_menu(

                    "⌂",

                    "Início",

                    mostrar_inicio,

                ),

                # ----------------------------------
                # CLIENTES
                # ----------------------------------

                item_menu(

                    "👥",

                    "Clientes",

                    abrir_clientes,

                ),

                # ----------------------------------
                # SERVIÇOS
                # ----------------------------------

                item_menu(

                    "🛠",

                    "Serviços",

                    abrir_servicos,

                ),

                # ----------------------------------
                # CAIXA
                # ----------------------------------

                item_menu(

                    "💰",

                    "Caixa",

                    abrir_caixa,

                ),

                # ----------------------------------
                # CONTRATOS / NOTAS FISCAIS
                # ----------------------------------

                item_menu(

                    "📁",

                    "Contratos / Notas Fiscais",

                    abrir_registros,

                ),

                # ----------------------------------
                # RELATÓRIOS
                # ----------------------------------

                item_menu(

                    "📊",

                    "Relatórios",

                    lambda e:

                        mostrar_relatorios(

                            page,

                            area_conteudo,

                        ),

                ),

                # ----------------------------------
                # ESPAÇO
                # ----------------------------------

                ft.Container(
                    expand=True,
                ),

                # ----------------------------------
                # CONFIGURAÇÕES
                # ----------------------------------

                item_menu(

                    "⚙",

                    "Configurações",

                    lambda e:

                        mostrar_inicio(),

                ),

            ],

            spacing=5,

            expand=True,

        ),

    )

    # ==========================================
    # LAYOUT PRINCIPAL
    # ==========================================

    layout = ft.Row(

        controls=[

            menu,

            area_conteudo,

        ],

        spacing=0,

        expand=True,

    )

    # ==========================================
    # ADICIONAR NA PÁGINA
    # ==========================================

    page.add(layout)

    # ==========================================
    # ABRIR PAINEL PRINCIPAL
    # ==========================================

    mostrar_inicio()