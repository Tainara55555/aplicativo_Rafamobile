import flet as ft
import flet_charts as fch

from datetime import datetime
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from database import (
    resumo_mes,
    listar_caixa,
    listar_servicos,
    listar_movimentacoes_servico,
    total_entradas_servico,
    total_saidas_servico,
)


# ============================================================
# CORES
# ============================================================

LARANJA = "#F75E00"

FUNDO = "#171717"
CARD = "#242424"
CARD_2 = "#2D2D2D"

BRANCO = "#FFFFFF"
CINZA = "#AAAAAA"
CINZA_ESCURA = "#777777"

VERDE = "#22C55E"
VERMELHO = "#EF4444"
AZUL = "#3B82F6"
ROXO = "#A855F7"
AMARELO = "#EAB308"


# ============================================================
# PÁGINA DE RELATÓRIOS
# ============================================================

def mostrar_relatorios(page: ft.Page, area_conteudo=None):

    page.title = "Rafá Mobile - Relatórios"
    page.bgcolor = FUNDO
    page.padding = 0


    # ========================================================
    # FILE PICKER
    # ========================================================

    file_picker = ft.FilePicker()

    try:

        if file_picker not in page.services:

            page.services.append(file_picker)

    except Exception:

        pass


    # ========================================================
    # DADOS DO RELATÓRIO
    # ========================================================

    relatorio_atual = {

        "mes": "",
        "ano": "",

        "entradas": 0.0,
        "saidas": 0.0,
        "saldo": 0.0,

        "clientes": 0,
        "servicos": 0,

        "total_servicos": 0.0,
        "entradas_servicos": 0.0,
        "despesas_servicos": 0.0,
        "saldo_servicos": 0.0,
    }


    # ========================================================
    # MESES
    # ========================================================

    meses = [

        ("01", "Janeiro"),
        ("02", "Fevereiro"),
        ("03", "Março"),
        ("04", "Abril"),
        ("05", "Maio"),
        ("06", "Junho"),
        ("07", "Julho"),
        ("08", "Agosto"),
        ("09", "Setembro"),
        ("10", "Outubro"),
        ("11", "Novembro"),
        ("12", "Dezembro"),
    ]


    nomes_meses = [

        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez",
    ]


    # ========================================================
    # CAMPOS DO FILTRO
    # ========================================================

    campo_mes = ft.Dropdown(

        label="Mês",

        width=200,

        value=str(
            datetime.now().month
        ).zfill(2),

        options=[

            ft.DropdownOption(

                key=numero,

                text=nome,
            )

            for numero, nome in meses
        ],

        bgcolor=CARD_2,

        color=BRANCO,

        border_color=LARANJA,

        focused_border_color=LARANJA,

        label_style=ft.TextStyle(

            color=LARANJA
        ),

        menu_style=ft.MenuStyle(

            bgcolor=ft.Colors.GREY_900
        ),
    )


    campo_ano = ft.TextField(

        label="Ano",

        value=str(
            datetime.now().year
        ),

        width=130,

        bgcolor=CARD_2,

        color=BRANCO,

        border_color=LARANJA,

        focused_border_color=LARANJA,

        label_style=ft.TextStyle(

            color=LARANJA
        ),
    )


    # ========================================================
    # FUNÇÃO DINHEIRO
    # ========================================================

    def dinheiro(valor):

        return (

            f"R$ {float(valor):,.2f}"

            .replace(",", "X")

            .replace(".", ",")

            .replace("X", ".")
        )


    # ========================================================
    # FORMATAR DATA
    # ========================================================

    def formatar_data(data):

        try:

            return datetime.strptime(

                str(data),

                "%Y-%m-%d"

            ).strftime(

                "%d/%m/%Y"
            )

        except Exception:

            return str(data)


    # ========================================================
    # TEXTOS DOS CARDS
    # ========================================================

    texto_entradas = ft.Text(

        "R$ 0,00",

        size=24,

        weight=ft.FontWeight.BOLD,

        color=AZUL,
    )


    texto_saidas = ft.Text(

        "R$ 0,00",

        size=24,

        weight=ft.FontWeight.BOLD,

        color=VERMELHO,
    )


    texto_saldo = ft.Text(

        "R$ 0,00",

        size=24,

        weight=ft.FontWeight.BOLD,

        color=VERDE,
    )


    texto_clientes = ft.Text(

        "0",

        size=24,

        weight=ft.FontWeight.BOLD,

        color=BRANCO,
    )


    texto_servicos = ft.Text(

        "0",

        size=24,

        weight=ft.FontWeight.BOLD,

        color=BRANCO,
    )


    # ========================================================
    # CRIAR CARD
    # ========================================================

    def criar_card(
        titulo,
        texto_valor,
    ):

        return ft.Container(

            width=210,

            height=110,

            padding=18,

            bgcolor=CARD,

            border_radius=10,

            content=ft.Column(

                spacing=8,

                controls=[

                    ft.Text(

                        titulo,

                        size=14,

                        color=CINZA,
                    ),

                    texto_valor,
                ],
            ),
        )


    # ========================================================
    # CARDS DO RESUMO
    # ========================================================

    cards_resumo = ft.Row(

        wrap=True,

        spacing=15,

        run_spacing=15,

        controls=[

            criar_card(

                "Entradas",

                texto_entradas,
            ),

            criar_card(

                "Saídas",

                texto_saidas,
            ),

            criar_card(

                "Saldo",

                texto_saldo,
            ),

            criar_card(

                "Clientes",

                texto_clientes,
            ),

            criar_card(

                "Serviços",

                texto_servicos,
            ),
        ],
    )


    # ========================================================
    # DADOS DOS GRÁFICOS
    # ========================================================

    def criar_dados_ano(ano):

        dados = []


        for mes in range(1, 13):

            dados.append({

                "mes": mes,

                "entradas_servicos": 0.0,

                "entradas_caixa": 0.0,

                "saidas_caixa": 0.0,

                "despesas_servicos": 0.0,

                "saldo_servicos": 0.0,

                "saldo_caixa": 0.0,
            })


        # ====================================================
        # CAIXA DA EMPRESA
        # ====================================================

        movimentacoes_caixa = listar_caixa()


        for movimentacao in movimentacoes_caixa:

            data = str(

                movimentacao[
                    "data_movimentacao"
                ]
            )


            if data[:4] != str(ano):

                continue


            try:

                mes = int(

                    data[5:7]
                )

            except Exception:

                continue


            valor = float(

                movimentacao["valor"] or 0
            )


            item = dados[mes - 1]


            if movimentacao["tipo"] == "ENTRADA":

                item[
                    "entradas_caixa"
                ] += valor

            else:

                item[
                    "saidas_caixa"
                ] += valor


        # ====================================================
        # SERVIÇOS
        # ====================================================

        servicos = listar_servicos()


        for servico in servicos:

            id_servico = servico["id"]


            movimentacoes = (

                listar_movimentacoes_servico(

                    id_servico
                )
            )


            for movimentacao in movimentacoes:

                data = str(

                    movimentacao[
                        "data_movimentacao"
                    ]
                )


                if data[:4] != str(ano):

                    continue


                try:

                    mes = int(

                        data[5:7]
                    )

                except Exception:

                    continue


                valor = float(

                    movimentacao["valor"] or 0
                )


                item = dados[mes - 1]


                if movimentacao["tipo"] == "ENTRADA":

                    item[
                        "entradas_servicos"
                    ] += valor

                else:

                    item[
                        "despesas_servicos"
                    ] += valor


        # ====================================================
        # SALDOS
        # ====================================================

        for item in dados:

            item[
                "saldo_servicos"
            ] = (

                item[
                    "entradas_servicos"
                ]

                -

                item[
                    "despesas_servicos"
                ]
            )


            item[
                "saldo_caixa"
            ] = (

                item[
                    "entradas_caixa"
                ]

                -

                item[
                    "saidas_caixa"
                ]
            )


        return dados


    # ========================================================
    # LEGENDA
    # ========================================================

    def legenda_grafico():

        itens = [

            (
                "Entradas serviços",
                AZUL,
            ),

            (
                "Entradas caixa",
                VERDE,
            ),

            (
                "Saídas caixa",
                VERMELHO,
            ),

            (
                "Despesas serviços",
                LARANJA,
            ),

            (
                "Saldo serviços",
                ROXO,
            ),

            (
                "Saldo caixa",
                AMARELO,
            ),
        ]


        return ft.Row(

            wrap=True,

            spacing=18,

            run_spacing=8,

            controls=[

                ft.Row(

                    spacing=6,

                    controls=[

                        ft.Container(

                            width=10,

                            height=10,

                            bgcolor=cor,

                            border_radius=2,
                        ),

                        ft.Text(

                            nome,

                            size=11,

                            color=CINZA,
                        ),
                    ],
                )

                for nome, cor in itens
            ],
        )


    # ========================================================
    # GRÁFICO ANUAL EM COLUNAS
    # ========================================================

    def criar_grafico_anual(ano):

        dados = criar_dados_ano(ano)


        series_config = [

            (
                "entradas_servicos",
                AZUL,
            ),

            (
                "entradas_caixa",
                VERDE,
            ),

            (
                "saidas_caixa",
                VERMELHO,
            ),

            (
                "despesas_servicos",
                LARANJA,
            ),

            (
                "saldo_servicos",
                ROXO,
            ),

            (
                "saldo_caixa",
                AMARELO,
            ),
        ]


        todos_valores = []


        for item in dados:

            for chave, _ in series_config:

                todos_valores.append(

                    float(
                        item[chave]
                    )
                )


        maior = max(

            todos_valores + [100]
        )


        menor = min(

            todos_valores + [0]
        )


        margem = max(

            abs(maior) * 0.15,

            100,
        )


        max_y = maior + margem

        min_y = menor - margem


        if min_y > 0:

            min_y = 0


        # ====================================================
        # GRUPOS DE COLUNAS
        # ====================================================

        grupos = []


        for mes in range(1, 13):

            rods = []


            for chave, cor in series_config:

                valor = float(

                    dados[
                        mes - 1
                    ][chave]
                )


                rods.append(

                    fch.BarChartRod(

                        from_y=0,

                        to_y=valor,

                        width=10,

                        color=cor,

                        border_radius=3,

                        tooltip=dinheiro(

                            valor
                        ),
                    )
                )


            grupos.append(

                fch.BarChartGroup(

                    x=mes,

                    rods=rods,
                )
            )


        # ====================================================
        # GRÁFICO
        # ====================================================

        grafico = fch.BarChart(

            expand=True,

            interactive=True,

            min_y=min_y,

            max_y=max_y,

            groups=grupos,

            bgcolor=CARD_2,

            border=ft.Border.all(

                1,

                "#3A3A3A",
            ),

            left_axis=fch.ChartAxis(

                label_size=55,
            ),

            bottom_axis=fch.ChartAxis(

                label_size=35,

                labels=[

                    fch.ChartAxisLabel(

                        value=index + 1,

                        label=ft.Text(

                            nomes_meses[index],

                            size=11,

                            color=CINZA,
                        ),
                    )

                    for index in range(12)
                ],
            ),

            horizontal_grid_lines=(

                fch.ChartGridLines(

                    color="#353535",

                    width=1,
                )
            ),
        )


        return ft.Container(

            width=1100,

            padding=20,

            bgcolor=CARD,

            border_radius=10,

            content=ft.Column(

                spacing=15,

                controls=[

                    ft.Row(

                        alignment=(

                            ft.MainAxisAlignment
                            .SPACE_BETWEEN
                        ),

                        controls=[

                            ft.Text(

                                f"Visão geral de {ano}",

                                size=18,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color=BRANCO,
                            ),

                            ft.Text(

                                "Janeiro a Dezembro",

                                size=12,

                                color=CINZA,
                            ),
                        ],
                    ),

                    ft.Container(

                        height=360,

                        content=grafico,
                    ),

                    legenda_grafico(),
                ],
            ),
        )


    # ========================================================
    # GRÁFICO DO MÊS
    # ========================================================

    def criar_grafico_periodo(

        ano,

        mes,
    ):

        dados = criar_dados_ano(ano)


        item = dados[

            mes - 1
        ]


        categorias = [

            (
                "Entradas serviços",

                item[
                    "entradas_servicos"
                ],

                AZUL,
            ),

            (
                "Entradas caixa",

                item[
                    "entradas_caixa"
                ],

                VERDE,
            ),

            (
                "Saídas caixa",

                item[
                    "saidas_caixa"
                ],

                VERMELHO,
            ),

            (
                "Despesas serviços",

                item[
                    "despesas_servicos"
                ],

                LARANJA,
            ),

            (
                "Saldo serviços",

                item[
                    "saldo_servicos"
                ],

                ROXO,
            ),

            (
                "Saldo caixa",

                item[
                    "saldo_caixa"
                ],

                AMARELO,
            ),
        ]


        valores = [

            float(valor)

            for _, valor, _ in categorias
        ]


        maior = max(

            valores + [100]
        )


        menor = min(

            valores + [0]
        )


        margem = max(

            abs(maior) * 0.15,

            100,
        )


        max_y = maior + margem

        min_y = menor - margem


        if min_y > 0:

            min_y = 0


        grupos = []


        for indice, (

            nome,

            valor,

            cor,

        ) in enumerate(categorias):

            grupos.append(

                fch.BarChartGroup(

                    x=indice,

                    rods=[

                        fch.BarChartRod(

                            from_y=0,

                            to_y=float(
                                valor
                            ),

                            width=38,

                            color=cor,

                            border_radius=5,
                        ),
                    ],
                )
            )


        grafico = fch.BarChart(

            expand=True,

            interactive=True,

            min_y=min_y,

            max_y=max_y,

            groups=grupos,

            bgcolor=CARD_2,

            border=ft.Border.all(

                1,

                "#3A3A3A",
            ),

            left_axis=fch.ChartAxis(

                label_size=55,
            ),

            bottom_axis=fch.ChartAxis(

                label_size=95,

                labels=[

                    fch.ChartAxisLabel(

                        value=index,

                        label=ft.Text(

                            nome,

                            size=9,

                            color=CINZA,
                        ),
                    )

                    for index, (

                        nome,

                        _,

                        _,

                    ) in enumerate(

                        categorias
                    )
                ],
            ),

            horizontal_grid_lines=(

                fch.ChartGridLines(

                    color="#353535",

                    width=1,
                )
            ),
        )


        return ft.Container(

            width=1100,

            padding=20,

            bgcolor=CARD,

            border_radius=10,

            content=ft.Column(

                spacing=15,

                controls=[

                    ft.Row(

                        alignment=(

                            ft.MainAxisAlignment
                            .SPACE_BETWEEN
                        ),

                        controls=[

                            ft.Text(

                                (

                                    f"Período: "
                                    f"{nomes_meses[mes - 1]}"
                                    f"/{ano}"
                                ),

                                size=18,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color=BRANCO,
                            ),

                            ft.Text(

                                "Resumo financeiro",

                                size=12,

                                color=CINZA,
                            ),
                        ],
                    ),

                    ft.Container(

                        height=360,

                        content=grafico,
                    ),

                    legenda_grafico(),
                ],
            ),
        )


    # ========================================================
    # GRÁFICO ANUAL NA TELA
    # ========================================================

    grafico_anual_area = ft.Container(

        visible=True,

        content=criar_grafico_anual(

            datetime.now().year
        ),
    )


    # ========================================================
    # GRÁFICO DO PERÍODO
    # ========================================================

    grafico_periodo_area = ft.Container(

        visible=False,

        content=None,
    )


    # ========================================================
    # TEXTO DE EXPORTAÇÃO
    # ========================================================

    texto_exportacao = ft.Text(

        "",

        size=13,

        color=CINZA,
    )


    # ========================================================
    # DOCUMENTO DO RELATÓRIO
    # ========================================================

    conteudo_documento = ft.Column(

        spacing=0,
    )


    relatorio_documento = ft.Container(

        visible=False,

        width=900,

        padding=45,

        bgcolor=BRANCO,

        border_radius=4,

        shadow=ft.BoxShadow(

            spread_radius=1,

            blur_radius=12,

            color="#55000000",

            offset=ft.Offset(

                0,

                4,
            ),
        ),

        content=conteudo_documento,
    )


    # ========================================================
    # SCREENSHOT SOMENTE DO DOCUMENTO
    # ========================================================

    screenshot_relatorio = ft.Screenshot(

        content=relatorio_documento,
    )


    # ========================================================
    # LINHA DE RESUMO DO DOCUMENTO
    # ========================================================

    def linha_resumo(

        titulo,

        valor,

        cor="#222222",
    ):

        return ft.Container(

            padding=ft.Padding.symmetric(

                horizontal=12,

                vertical=8,
            ),

            content=ft.Row(

                controls=[

                    ft.Text(

                        titulo,

                        size=13,

                        color="#555555",

                        expand=True,
                    ),

                    ft.Text(

                        valor,

                        size=14,

                        weight=(
                            ft.FontWeight.BOLD
                        ),

                        color=cor,
                    ),
                ],
            ),
        )


    # ========================================================
    # LINHA DE MOVIMENTAÇÃO DO DOCUMENTO
    # ========================================================

    def linha_movimentacao_documento(

        data,

        tipo,

        descricao,

        valor,
    ):

        if tipo == "ENTRADA":

            cor = VERDE

            sinal = "+"

        else:

            cor = VERMELHO

            sinal = "-"


        return ft.Container(

            padding=ft.Padding.symmetric(

                horizontal=8,

                vertical=9,
            ),

            content=ft.Column(

                spacing=0,

                controls=[

                    ft.Row(

                        controls=[

                            ft.Container(

                                width=90,

                                content=ft.Text(

                                    data,

                                    size=12,

                                    color="#555555",
                                ),
                            ),

                            ft.Container(

                                width=90,

                                content=ft.Text(

                                    tipo,

                                    size=12,

                                    weight=(
                                        ft.FontWeight.BOLD
                                    ),

                                    color=cor,
                                ),
                            ),

                            ft.Container(

                                expand=True,

                                content=ft.Text(

                                    descricao,

                                    size=12,

                                    color="#222222",
                                ),
                            ),

                            ft.Container(

                                width=130,

                                alignment=ft.Alignment(

                                    1,

                                    0,
                                ),

                                content=ft.Text(

                                    f"{sinal} "
                                    f"{dinheiro(valor)}",

                                    size=12,

                                    weight=(
                                        ft.FontWeight.BOLD
                                    ),

                                    color=cor,
                                ),
                            ),
                        ],
                    ),

                    ft.Divider(

                        height=1,

                        color="#E5E5E5",
                    ),
                ],
            ),
        )


    # ========================================================
    # MONTAR DOCUMENTO
    # ========================================================

    def atualizar_dados_documento(

        movimentacoes
    ):

        conteudo_documento.controls.clear()


        periodo = (

            f"{relatorio_atual['mes']}/"
            f"{relatorio_atual['ano']}"
        )


        # ====================================================
        # CABEÇALHO
        # ====================================================

        conteudo_documento.controls.append(

            ft.Row(

                alignment=(

                    ft.MainAxisAlignment
                    .SPACE_BETWEEN
                ),

                vertical_alignment=(

                    ft.CrossAxisAlignment.CENTER
                ),

                controls=[

                    ft.Image(

                        src="logo.png",

                        width=140,

                        height=70,

                        fit=ft.BoxFit.CONTAIN,
                    ),

                    ft.Column(

                        horizontal_alignment=(

                            ft.CrossAxisAlignment.END
                        ),

                        spacing=4,

                        controls=[

                            ft.Text(

                                "RELATÓRIO FINANCEIRO",

                                size=21,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color="#222222",
                            ),

                            ft.Text(

                                f"Período: {periodo}",

                                size=13,

                                color="#555555",
                            ),

                            ft.Text(

                                "Rafá Mobile Móveis Planejados",

                                size=11,

                                color="#777777",
                            ),
                        ],
                    ),
                ],
            )
        )


        conteudo_documento.controls.append(

            ft.Divider(

                height=25,

                color="#DDDDDD",
            )
        )


        # ====================================================
        # RESUMO FINANCEIRO
        # ====================================================

        conteudo_documento.controls.append(

            ft.Text(

                "RESUMO FINANCEIRO",

                size=16,

                weight=ft.FontWeight.BOLD,

                color="#222222",
            )
        )


        resumo_documento = ft.Container(

            margin=ft.Margin.symmetric(

                vertical=10
            ),

            padding=15,

            bgcolor="#F7F7F7",

            border_radius=6,

            content=ft.Row(

                wrap=True,

                spacing=35,

                run_spacing=20,

                controls=[

                    ft.Column(

                        spacing=4,

                        controls=[

                            ft.Text(

                                "Entradas",

                                size=11,

                                color="#777777",
                            ),

                            ft.Text(

                                dinheiro(

                                    relatorio_atual[

                                        "entradas"
                                    ]
                                ),

                                size=17,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color=AZUL,
                            ),
                        ],
                    ),

                    ft.Column(

                        spacing=4,

                        controls=[

                            ft.Text(

                                "Saídas",

                                size=11,

                                color="#777777",
                            ),

                            ft.Text(

                                dinheiro(

                                    relatorio_atual[

                                        "saidas"
                                    ]
                                ),

                                size=17,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color=VERMELHO,
                            ),
                        ],
                    ),

                    ft.Column(

                        spacing=4,

                        controls=[

                            ft.Text(

                                "Saldo",

                                size=11,

                                color="#777777",
                            ),

                            ft.Text(

                                dinheiro(

                                    relatorio_atual[

                                        "saldo"
                                    ]
                                ),

                                size=17,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color=(

                                    VERDE

                                    if relatorio_atual[

                                        "saldo"
                                    ] >= 0

                                    else VERMELHO
                                ),
                            ),
                        ],
                    ),

                    ft.Column(

                        spacing=4,

                        controls=[

                            ft.Text(

                                "Clientes",

                                size=11,

                                color="#777777",
                            ),

                            ft.Text(

                                str(

                                    relatorio_atual[

                                        "clientes"
                                    ]
                                ),

                                size=17,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color="#222222",
                            ),
                        ],
                    ),

                    ft.Column(

                        spacing=4,

                        controls=[

                            ft.Text(

                                "Serviços",

                                size=11,

                                color="#777777",
                            ),

                            ft.Text(

                                str(

                                    relatorio_atual[

                                        "servicos"
                                    ]
                                ),

                                size=17,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color="#222222",
                            ),
                        ],
                    ),
                ],
            ),
        )


        conteudo_documento.controls.append(

            resumo_documento
        )


        conteudo_documento.controls.append(

            ft.Divider(

                height=25,

                color="#DDDDDD",
            )
        )


        # ====================================================
        # MOVIMENTAÇÕES DO CAIXA
        # ====================================================

        conteudo_documento.controls.append(

            ft.Text(

                "MOVIMENTAÇÕES DO CAIXA",

                size=16,

                weight=ft.FontWeight.BOLD,

                color="#222222",
            )
        )


        conteudo_documento.controls.append(

            ft.Container(

                margin=ft.Margin.symmetric(

                    vertical=8
                ),

                padding=10,

                bgcolor="#F1F1F1",

                border_radius=5,

                content=ft.Row(

                    controls=[

                        ft.Container(

                            width=90,

                            content=ft.Text(

                                "Data",

                                size=11,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color="#444444",
                            ),
                        ),

                        ft.Container(

                            width=90,

                            content=ft.Text(

                                "Tipo",

                                size=11,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color="#444444",
                            ),
                        ),

                        ft.Container(

                            expand=True,

                            content=ft.Text(

                                "Descrição",

                                size=11,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color="#444444",
                            ),
                        ),

                        ft.Container(

                            width=130,

                            alignment=ft.Alignment(

                                1,

                                0,
                            ),

                            content=ft.Text(

                                "Valor",

                                size=11,

                                weight=(
                                    ft.FontWeight.BOLD
                                ),

                                color="#444444",
                            ),
                        ),
                    ],
                ),
            )
        )


        # ====================================================
        # MOVIMENTAÇÕES
        # ========================================================

        if movimentacoes:

            for movimentacao in movimentacoes:

                conteudo_documento.controls.append(

                    linha_movimentacao_documento(

                        formatar_data(

                            movimentacao[

                                "data_movimentacao"
                            ]
                        ),

                        movimentacao[

                            "tipo"
                        ],

                        str(

                            movimentacao[

                                "descricao"
                            ]
                        ),

                        float(

                            movimentacao[

                                "valor"
                            ] or 0
                        ),
                    )
                )

        else:

            conteudo_documento.controls.append(

                ft.Container(

                    padding=20,

                    content=ft.Text(

                        "Nenhuma movimentação "
                        "registrada neste período.",

                        size=12,

                        color="#777777",

                        italic=True,
                    ),
                )
            )


        # ====================================================
        # RESUMO DOS SERVIÇOS
        # ====================================================

        conteudo_documento.controls.append(

            ft.Divider(

                height=25,

                color="#DDDDDD",
            )
        )


        conteudo_documento.controls.append(

            ft.Text(

                "RESUMO DOS SERVIÇOS",

                size=16,

                weight=ft.FontWeight.BOLD,

                color="#222222",
            )
        )


        servicos_documento = ft.Container(

            margin=ft.Margin(

                top=10,

                right=0,

                bottom=0,

                left=0,
            ),

            padding=12,

            bgcolor="#F7F7F7",

            border_radius=6,

            content=ft.Column(

                spacing=0,

                controls=[

                    linha_resumo(

                        "Valor total dos serviços",

                        dinheiro(

                            relatorio_atual[

                                "total_servicos"
                            ]
                        ),
                    ),

                    linha_resumo(

                        "Entradas dos serviços",

                        dinheiro(

                            relatorio_atual[

                                "entradas_servicos"
                            ]
                        ),

                        VERDE,
                    ),

                    linha_resumo(

                        "Despesas dos serviços",

                        dinheiro(

                            relatorio_atual[

                                "despesas_servicos"
                            ]
                        ),

                        VERMELHO,
                    ),

                    linha_resumo(

                        "Saldo dos serviços",

                        dinheiro(

                            relatorio_atual[

                                "saldo_servicos"
                            ]
                        ),

                        (

                            VERDE

                            if relatorio_atual[

                                "saldo_servicos"
                            ] >= 0

                            else VERMELHO
                        ),
                    ),
                ],
            ),
        )


        conteudo_documento.controls.append(

            servicos_documento
        )


        # ====================================================
        # RODAPÉ
        # ====================================================

        conteudo_documento.controls.append(

            ft.Divider(

                height=25,

                color="#DDDDDD",
            )
        )


        conteudo_documento.controls.append(

            ft.Text(

                "Rafá Mobile Móveis Planejados",

                size=11,

                weight=ft.FontWeight.BOLD,

                color="#555555",
            )
        )


        conteudo_documento.controls.append(

            ft.Text(

                "Relatório gerado pelo sistema financeiro.",

                size=10,

                color="#888888",
            )
        )
            # ========================================================
    # BAIXAR PDF
    # ========================================================

    async def baixar_pdf(e):

        try:

            if not relatorio_atual["ano"]:

                texto_exportacao.value = (
                    "Gere o relatório primeiro."
                )

                page.update()

                return


            buffer = BytesIO()

            pdf = canvas.Canvas(

                buffer,

                pagesize=A4,
            )

            largura, altura = A4

            y = altura - 45


            # ------------------------------------------------
            # CABEÇALHO
            # ------------------------------------------------

            pdf.setFont(

                "Helvetica-Bold",

                18,
            )

            pdf.drawString(

                40,

                y,

                "RAFÁ MOBILE",
            )

            y -= 22


            pdf.setFont(

                "Helvetica-Bold",

                13,
            )

            pdf.drawString(

                40,

                y,

                "RELATÓRIO FINANCEIRO",
            )

            y -= 20


            pdf.setFont(

                "Helvetica",

                10,
            )

            pdf.drawString(

                40,

                y,

                (
                    f"Período: "
                    f"{relatorio_atual['mes']}/"
                    f"{relatorio_atual['ano']}"
                ),
            )

            y -= 30


            pdf.line(

                40,

                y,

                largura - 40,

                y,
            )

            y -= 25


            # ------------------------------------------------
            # RESUMO
            # ------------------------------------------------

            pdf.setFont(

                "Helvetica-Bold",

                13,
            )

            pdf.drawString(

                40,

                y,

                "RESUMO FINANCEIRO",
            )

            y -= 22


            pdf.setFont(

                "Helvetica",

                10,
            )


            resumo_pdf = [

                (
                    "Entradas",

                    relatorio_atual[
                        "entradas"
                    ],
                ),

                (
                    "Saídas",

                    relatorio_atual[
                        "saidas"
                    ],
                ),

                (
                    "Saldo",

                    relatorio_atual[
                        "saldo"
                    ],
                ),

                (
                    "Clientes",

                    relatorio_atual[
                        "clientes"
                    ],
                ),

                (
                    "Serviços",

                    relatorio_atual[
                        "servicos"
                    ],
                ),
            ]


            for titulo, valor in resumo_pdf:

                if titulo in [

                    "Clientes",

                    "Serviços",
                ]:

                    valor_formatado = str(

                        valor
                    )

                else:

                    valor_formatado = dinheiro(

                        valor
                    )


                pdf.drawString(

                    50,

                    y,

                    (
                        f"{titulo}: "
                        f"{valor_formatado}"
                    ),
                )

                y -= 18


            y -= 10


            # ------------------------------------------------
            # MOVIMENTAÇÕES
            # ------------------------------------------------

            pdf.setFont(

                "Helvetica-Bold",

                13,
            )

            pdf.drawString(

                40,

                y,

                "MOVIMENTAÇÕES DO CAIXA",
            )

            y -= 22


            pdf.setFont(

                "Helvetica-Bold",

                9,
            )

            pdf.drawString(

                40,

                y,

                "Data",
            )

            pdf.drawString(

                95,

                y,

                "Tipo",
            )

            pdf.drawString(

                150,

                y,

                "Descrição",
            )

            pdf.drawRightString(

                largura - 40,

                y,

                "Valor",
            )

            y -= 15


            pdf.setFont(

                "Helvetica",

                8,
            )


            movimentacoes_pdf = listar_caixa()


            periodo_pdf = (

                f"{relatorio_atual['ano']}-"
                f"{relatorio_atual['mes']}"
            )


            movimentacoes_periodo_pdf = [

                mov

                for mov in movimentacoes_pdf

                if str(

                    mov[
                        "data_movimentacao"
                    ]

                )[:7] == periodo_pdf
            ]


            if movimentacoes_periodo_pdf:

                for movimentacao in (

                    movimentacoes_periodo_pdf
                ):

                    if y < 60:

                        pdf.showPage()

                        y = altura - 45

                        pdf.setFont(

                            "Helvetica",

                            8,
                        )


                    data = formatar_data(

                        movimentacao[
                            "data_movimentacao"
                        ]
                    )


                    tipo = str(

                        movimentacao[
                            "tipo"
                        ]
                    )


                    descricao = str(

                        movimentacao[
                            "descricao"
                        ]
                    )


                    valor = float(

                        movimentacao[
                            "valor"
                        ] or 0
                    )


                    pdf.drawString(

                        40,

                        y,

                        data,
                    )


                    pdf.drawString(

                        95,

                        y,

                        tipo,
                    )


                    pdf.drawString(

                        150,

                        y,

                        descricao[:60],
                    )


                    pdf.drawRightString(

                        largura - 40,

                        y,

                        dinheiro(valor),
                    )


                    y -= 15


            else:

                pdf.drawString(

                    40,

                    y,

                    "Nenhuma movimentação registrada.",
                )

                y -= 20


            y -= 15


            # ------------------------------------------------
            # SERVIÇOS
            # ------------------------------------------------

            if y < 150:

                pdf.showPage()

                y = altura - 45


            pdf.setFont(

                "Helvetica-Bold",

                13,
            )


            pdf.drawString(

                40,

                y,

                "RESUMO DOS SERVIÇOS",
            )


            y -= 22


            pdf.setFont(

                "Helvetica",

                10,
            )


            servicos_pdf = [

                (
                    "Valor total dos serviços",

                    relatorio_atual[
                        "total_servicos"
                    ],
                ),

                (
                    "Entradas dos serviços",

                    relatorio_atual[
                        "entradas_servicos"
                    ],
                ),

                (
                    "Despesas dos serviços",

                    relatorio_atual[
                        "despesas_servicos"
                    ],
                ),

                (
                    "Saldo dos serviços",

                    relatorio_atual[
                        "saldo_servicos"
                    ],
                ),
            ]


            for titulo, valor in servicos_pdf:

                pdf.drawString(

                    50,

                    y,

                    (
                        f"{titulo}: "
                        f"{dinheiro(valor)}"
                    ),
                )

                y -= 18


            y -= 20


            pdf.setFont(

                "Helvetica",

                8,
            )


            pdf.drawString(

                40,

                y,

                "Relatório gerado pelo sistema Rafá Mobile.",
            )


            pdf.save()


            dados_pdf = buffer.getvalue()


            nome_arquivo = (

                f"relatorio_"
                f"{relatorio_atual['ano']}_"
                f"{relatorio_atual['mes']}.pdf"
            )


            caminho = await file_picker.save_file(

                dialog_title=(

                    "Salvar relatório em PDF"
                ),

                file_name=nome_arquivo,

                allowed_extensions=[

                    "pdf"
                ],

                src_bytes=dados_pdf,
            )


            if caminho:

                texto_exportacao.value = (

                    "PDF salvo com sucesso."
                )

            else:

                texto_exportacao.value = (

                    "Salvamento cancelado."
                )


            page.update()


        except Exception as erro:

            texto_exportacao.value = (

                f"Erro ao gerar PDF: {erro}"
            )

            page.update()


    # ========================================================
    # BAIXAR IMAGEM
    # ========================================================

    async def baixar_imagem(e):

        try:

            if not relatorio_atual["ano"]:

                texto_exportacao.value = (

                    "Gere o relatório primeiro."
                )

                page.update()

                return


            relatorio_documento.visible = True

            page.update()


            imagem = await screenshot_relatorio.capture(

                pixel_ratio=2.0
            )


            if not imagem:

                texto_exportacao.value = (

                    "Não foi possível gerar a imagem."
                )

                page.update()

                return


            nome_arquivo = (

                f"relatorio_"
                f"{relatorio_atual['ano']}_"
                f"{relatorio_atual['mes']}.png"
            )


            caminho = await file_picker.save_file(

                dialog_title=(

                    "Salvar relatório como imagem"
                ),

                file_name=nome_arquivo,

                allowed_extensions=[

                    "png"
                ],

                src_bytes=imagem,
            )


            if caminho:

                texto_exportacao.value = (

                    "Imagem salva com sucesso."
                )

            else:

                texto_exportacao.value = (

                    "Salvamento cancelado."
                )


            page.update()


        except Exception as erro:

            texto_exportacao.value = (

                f"Erro ao salvar imagem: {erro}"
            )

            page.update()


    # ========================================================
    # VISUALIZAÇÃO DOS GRÁFICOS
    # ========================================================

    def mostrar_visao_anual(e=None):

        try:

            ano = int(

                campo_ano.value
            )

        except Exception:

            ano = datetime.now().year


        grafico_anual_area.content = (

            criar_grafico_anual(

                ano
            )
        )


        grafico_anual_area.visible = True

        grafico_periodo_area.visible = False


        botao_visao_anual.bgcolor = LARANJA

        botao_visao_mes.bgcolor = CARD_2


        page.update()


    def mostrar_visao_mes(e=None):

        try:

            ano = int(

                campo_ano.value
            )

            mes = int(

                campo_mes.value
            )

        except Exception:

            return


        grafico_periodo_area.content = (

            criar_grafico_periodo(

                ano,

                mes
            )
        )


        grafico_anual_area.visible = False

        grafico_periodo_area.visible = True


        botao_visao_anual.bgcolor = CARD_2

        botao_visao_mes.bgcolor = LARANJA


        page.update()


    # ========================================================
    # BOTÃO VISÃO ANUAL
    # ========================================================

    botao_visao_anual = ft.Button(

        "Ano inteiro",

        icon=ft.Icons.BAR_CHART,

        bgcolor=LARANJA,

        color=BRANCO,

        height=42,

        on_click=mostrar_visao_anual,
    )


    # ========================================================
    # BOTÃO MÊS SELECIONADO
    # ========================================================

    botao_visao_mes = ft.Button(

        "Mês selecionado",

        icon=ft.Icons.CALENDAR_MONTH,

        bgcolor=CARD_2,

        color=BRANCO,

        height=42,

        on_click=mostrar_visao_mes,
    )


    # ========================================================
    # BOTÕES DE VISUALIZAÇÃO
    # ========================================================

    botoes_visualizacao = ft.Row(

        spacing=10,

        controls=[

            botao_visao_anual,

            botao_visao_mes,
        ],
    )


    # ========================================================
    # ATUALIZAR RELATÓRIO
    # ========================================================

    def atualizar_relatorio(e=None):

        try:

            mes = int(

                campo_mes.value
            )


            ano = int(

                campo_ano.value
            )


            periodo = (

                f"{ano:04d}-"
                f"{mes:02d}"
            )


            relatorio_atual["mes"] = (

                str(mes).zfill(2)
            )


            relatorio_atual["ano"] = (

                str(ano)
            )


            # ------------------------------------------------
            # MOSTRA AUTOMATICAMENTE O GRÁFICO DO MÊS
            # ------------------------------------------------

            grafico_anual_area.visible = False

            grafico_periodo_area.content = (

                criar_grafico_periodo(

                    ano,

                    mes
                )
            )

            grafico_periodo_area.visible = True


            # Destaca o botão mensal

            botao_visao_anual.bgcolor = CARD_2

            botao_visao_mes.bgcolor = LARANJA


            # ------------------------------------------------
            # RESUMO GERAL
            # ------------------------------------------------

            resultado = resumo_mes(

                ano,

                mes
            )


            relatorio_atual[

                "entradas"

            ] = float(

                resultado["entradas"]
            )


            relatorio_atual[

                "saidas"

            ] = float(

                resultado["saidas"]
            )


            relatorio_atual[

                "saldo"

            ] = float(

                resultado["saldo"]
            )


            relatorio_atual[

                "clientes"

            ] = int(

                resultado["clientes"]
            )


            relatorio_atual[

                "servicos"

            ] = int(

                resultado["servicos"]
            )


            # ------------------------------------------------
            # ATUALIZA CARDS
            # ------------------------------------------------

            texto_entradas.value = dinheiro(

                resultado["entradas"]
            )


            texto_saidas.value = dinheiro(

                resultado["saidas"]
            )


            texto_saldo.value = dinheiro(

                resultado["saldo"]
            )


            texto_clientes.value = str(

                resultado["clientes"]
            )


            texto_servicos.value = str(

                resultado["servicos"]
            )


            if resultado["saldo"] < 0:

                texto_saldo.color = VERMELHO

            else:

                texto_saldo.color = VERDE


            # ------------------------------------------------
            # MOVIMENTAÇÕES DO CAIXA
            # ------------------------------------------------

            movimentacoes = listar_caixa()


            movimentacoes_periodo = []


            for movimentacao in movimentacoes:

                data = str(

                    movimentacao[
                        "data_movimentacao"
                    ]
                )


                if data[:7] == periodo:

                    movimentacoes_periodo.append(

                        movimentacao
                    )


            # ------------------------------------------------
            # SERVIÇOS
            # ------------------------------------------------

            servicos = listar_servicos()


            total_servicos = 0.0

            entradas_servicos = 0.0

            despesas_servicos = 0.0


            for servico in servicos:

                data_cadastro = str(

                    servico[
                        "data_cadastro"
                    ]
                )


                if data_cadastro[:7] != periodo:

                    continue


                id_servico = servico["id"]


                total_servicos += float(

                    servico[
                        "valor_total"
                    ] or 0
                )


                entradas_servicos += (

                    total_entradas_servico(

                        id_servico
                    )
                )


                despesas_servicos += (

                    total_saidas_servico(

                        id_servico
                    )
                )


            saldo_servicos = (

                entradas_servicos

                -

                despesas_servicos
            )


            relatorio_atual[

                "total_servicos"

            ] = total_servicos


            relatorio_atual[

                "entradas_servicos"

            ] = entradas_servicos


            relatorio_atual[

                "despesas_servicos"

            ] = despesas_servicos


            relatorio_atual[

                "saldo_servicos"

            ] = saldo_servicos


            # ------------------------------------------------
            # MONTAR DOCUMENTO
            # ------------------------------------------------

            atualizar_dados_documento(

                movimentacoes_periodo
            )


            # ------------------------------------------------
            # MOSTRAR DOCUMENTO
            # ------------------------------------------------

            relatorio_documento.visible = True


            # ------------------------------------------------
            # MOSTRAR ÁREA DE DOWNLOAD
            # ------------------------------------------------

            area_exportacao.visible = True


            texto_exportacao.value = (

                "Relatório gerado. "
                "Escolha como deseja salvá-lo."
            )


            page.update()


        except Exception as erro:

            print(

                f"Erro ao gerar relatório: {erro}"
            )


            texto_exportacao.value = (

                f"Erro ao gerar relatório: {erro}"
            )


            page.update()


    # ========================================================
    # BOTÃO GERAR RELATÓRIO
    # ========================================================

    botao_gerar = ft.Button(

        "Gerar relatório",

        icon=ft.Icons.ASSESSMENT,

        bgcolor=LARANJA,

        color=BRANCO,

        height=45,

        on_click=atualizar_relatorio,
    )


    # ========================================================
    # BOTÃO PDF
    # ========================================================

    botao_pdf = ft.Button(

        "Baixar PDF",

        icon=ft.Icons.PICTURE_AS_PDF,

        bgcolor=VERMELHO,

        color=BRANCO,

        height=45,

        on_click=baixar_pdf,
    )


    # ========================================================
    # BOTÃO IMAGEM
    # ========================================================

    botao_imagem = ft.Button(

        "Baixar imagem",

        icon=ft.Icons.IMAGE,

        bgcolor=AZUL,

        color=BRANCO,

        height=45,

        on_click=baixar_imagem,
    )


    # ========================================================
    # ÁREA DE EXPORTAÇÃO
    # ========================================================

    area_exportacao = ft.Container(

        visible=False,

        width=900,

        padding=20,

        bgcolor=CARD,

        border_radius=10,

        content=ft.Column(

            spacing=12,

            controls=[

                ft.Text(

                    "Salvar relatório",

                    size=17,

                    weight=ft.FontWeight.BOLD,

                    color=BRANCO,
                ),

                ft.Text(

                    "Escolha como deseja salvar "
                    "o relatório gerado.",

                    size=13,

                    color=CINZA,
                ),

                ft.Row(

                    wrap=True,

                    spacing=12,

                    controls=[

                        botao_pdf,

                        botao_imagem,
                    ],
                ),

                texto_exportacao,
            ],
        ),
    )


    # ========================================================
    # CABEÇALHO DA PÁGINA
    # ========================================================

    cabecalho = ft.Column(

        spacing=4,

        controls=[

            ft.Text(

                "Relatórios",

                size=25,

                weight=ft.FontWeight.BOLD,

                color=BRANCO,
            ),

            ft.Text(

                "Acompanhe as movimentações "
                "e os resultados da empresa",

                size=14,

                color=CINZA,
            ),
        ],
    )


    # ========================================================
    # FILTRO
    # ========================================================

    filtro = ft.Container(

        width=1100,

        padding=20,

        bgcolor=CARD,

        border_radius=10,

        content=ft.Column(

            spacing=15,

            controls=[

                ft.Text(

                    "Período do relatório",

                    size=17,

                    weight=ft.FontWeight.BOLD,

                    color=BRANCO,
                ),

                ft.Row(

                    wrap=True,

                    spacing=15,

                    run_spacing=15,

                    controls=[

                        campo_mes,

                        campo_ano,

                        botao_gerar,
                    ],
                ),
            ],
        ),
    )


    # ========================================================
    # TÍTULO DO RELATÓRIO GERADO
    # ========================================================

    titulo_relatorio_gerado = ft.Text(

        "Relatório gerado",

        size=18,

        weight=ft.FontWeight.BOLD,

        color=BRANCO,
    )


    # ========================================================
    # CONTEÚDO PRINCIPAL
    # ========================================================

    conteudo = ft.Column(

        expand=True,

        scroll=ft.ScrollMode.AUTO,

        spacing=22,

        controls=[

            cabecalho,

            # BOTÕES DE VISUALIZAÇÃO
            botoes_visualizacao,

            # GRÁFICO ANUAL
            grafico_anual_area,

            # GRÁFICO DO PERÍODO
            grafico_periodo_area,

            filtro,

            ft.Text(

                "Resumo do período",

                size=18,

                weight=ft.FontWeight.BOLD,

                color=BRANCO,
            ),

            cards_resumo,

            titulo_relatorio_gerado,

            screenshot_relatorio,

            area_exportacao,
        ],
    )


    # ========================================================
    # CONTAINER INTERNO
    # ========================================================

    container_interno = ft.Container(

        width=1100,

        content=conteudo,
    )


    # ========================================================
    # MOSTRAR NA ÁREA PRINCIPAL
    # ========================================================

    if area_conteudo is not None:

        area_conteudo.content = ft.Container(

            expand=True,

            bgcolor=FUNDO,

            padding=30,

            content=ft.Container(

                expand=True,

                content=container_interno,
            ),
        )


        area_conteudo.bgcolor = FUNDO

        area_conteudo.update()


    else:

        page.controls.clear()

        page.add(

            ft.Container(

                expand=True,

                bgcolor=FUNDO,

                padding=30,

                content=ft.Container(

                    expand=True,

                    content=container_interno,
                ),
            )
        )


        page.bgcolor = FUNDO

        page.update()