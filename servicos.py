import flet as ft



from database import (

    listar_clientes,

    cadastrar_servico,

    listar_servicos,

    listar_movimentacoes_servico,

    adicionar_movimentacao_servico,

    editar_movimentacao_servico,

    saldo_servico,

    total_saidas_servico,

    total_pago_servico,

    restante_servico,

    editar_servico,

    adicionar_servico_painel,

    remover_servico_painel,

)



LARANJA = "#FF6A00"

FUNDO = "#171717"

CARD = "#242424"

CARD_2 = "#2D2D2D"

BRANCO = "#FFFFFF"

CINZA = "#AAAAAA"

CINZA_ESCURA = "#777777"

VERDE = "#22C55E"

VERMELHO = "#EF4444"





def formatar_moeda(valor):

    return (

        f"R$ {valor:,.2f}"

        .replace(",", "X")

        .replace(".", ",")

        .replace("X", ".")

    )





def converter_valor(texto):

    texto = texto.strip()



    if not texto:

        raise ValueError()



    return float(

        texto.replace(".", "").replace(",", ".")

    )





def obter_nome_cliente(clientes, id_cliente):

    for cliente in clientes:

        if cliente[0] == id_cliente:

            return cliente[1]



    return "Cliente não encontrado"





def mostrar_servicos(

    page: ft.Page,

    area_conteudo=None,

    id_servico_abrir=None

):

    page.title = "Rafá Mobile - Serviços"

    page.bgcolor = FUNDO

    page.padding = 0



    clientes = listar_clientes()



    # ======================================================

    # CAMPOS DO CADASTRO

    # ======================================================



    cliente = ft.Dropdown(

        label="Cliente",

        hint_text="Selecione o cliente",

        options=[

            ft.DropdownOption(
                    key=str(c[0]),
                    content=ft.Text(
                        f"{c[0]} - {c[1]}",
                        color=BRANCO
                    )
                )

            for c in clientes

        ],

        width=500,

        bgcolor=FUNDO,

        color=BRANCO,

        border_color=CINZA_ESCURA,

        focused_border_color=LARANJA,

        label_style=ft.TextStyle(color=CINZA),

        menu_style=ft.MenuStyle(

            bgcolor=ft.Colors.GREY_900

        ),

    )



    descricao = ft.TextField(

        label="Descrição do serviço",

        hint_text="Ex.: Cozinha planejada",

        width=500,

        bgcolor=FUNDO,

        color=BRANCO,

        border_color=CINZA_ESCURA,

        focused_border_color=LARANJA,

        label_style=ft.TextStyle(color=CINZA),

        multiline=True,

        min_lines=2,

        max_lines=4,

    )



    valor_total = ft.TextField(

        label="Valor total",

        hint_text="Ex.: 10000,00",

        width=240,

        bgcolor=FUNDO,

        color=BRANCO,

        border_color=CINZA_ESCURA,

        focused_border_color=LARANJA,

        label_style=ft.TextStyle(color=CINZA),

    )



    entrada = ft.TextField(

        label="Entrada",

        hint_text="Ex.: 4000,00",

        width=240,

        bgcolor=FUNDO,

        color=BRANCO,

        border_color=CINZA_ESCURA,

        focused_border_color=LARANJA,

        label_style=ft.TextStyle(color=CINZA),

    )



    mensagem = ft.Text(

        "",

        size=13,

        color=LARANJA,

    )



    lista_servicos = ft.Column(

        controls=[],

        spacing=10,

        tight=True,

    )



    # ======================================================

    # MENSAGEM

    # ======================================================



    def mostrar_mensagem(texto, cor=LARANJA):

        dialogo = ft.AlertDialog(

            modal=True,

            bgcolor=ft.Colors.GREY_900,

            title=ft.Text(

                "Rafá Mobile",

                color=BRANCO,

                weight=ft.FontWeight.BOLD,

            ),

            content=ft.Container(

                bgcolor=ft.Colors.GREY_900,

                content=ft.Text(

                    texto,

                    color=BRANCO,

                    size=15,

                ),

            ),

            actions=[

                ft.Button(

                    "Fechar",

                    bgcolor=LARANJA,

                    color=BRANCO,

                    on_click=lambda e: page.pop_dialog(),

                )

            ],

        )



        page.show_dialog(dialogo)



    # ======================================================

    # EDITAR MOVIMENTAÇÃO

    # ======================================================



    def abrir_edicao_movimentacao(

        id_servico,

        movimento,

        fechar_detalhes

    ):

        id_movimento = movimento[0]

        descricao_atual = movimento[3]

        valor_atual = movimento[4]

        data_atual = movimento[5]

        categoria_atual = movimento[6]



        campo_descricao = ft.TextField(

            label="Descrição",

            value=descricao_atual,

            width=450,

            bgcolor=FUNDO,

            color=BRANCO,

            border_color=CINZA_ESCURA,

            focused_border_color=LARANJA,

            label_style=ft.TextStyle(color=CINZA),

        )



        campo_valor = ft.TextField(

            label="Valor",

            value=f"{valor_atual:.2f}".replace(".", ","),

            width=250,

            bgcolor=FUNDO,

            color=BRANCO,

            border_color=CINZA_ESCURA,

            focused_border_color=LARANJA,

            label_style=ft.TextStyle(color=CINZA),

        )



        categoria_normalizada = categoria_atual or "OUTROS"



        categorias_validas = {

            "MDF",

            "FERRAGEM",

            "GASOLINA",

            "OUTROS",

        }



        if categoria_normalizada not in categorias_validas:

            categoria_normalizada = "OUTROS"



        campo_categoria = ft.Dropdown(

            label="Categoria",

            value=categoria_normalizada,

            width=300,

            options=[

                ft.DropdownOption(

                    key="MDF",

                    content=ft.Text(

                        "MDF",

                        color=BRANCO

                    )

                ),

                ft.DropdownOption(

                    key="FERRAGEM",

                    content=ft.Text(

                        "Ferragens",

                        color=BRANCO

                    )

                ),

                ft.DropdownOption(

                    key="GASOLINA",

                    content=ft.Text(

                        "Gasolina",

                        color=BRANCO

                    )

                ),

                ft.DropdownOption(

                    key="OUTROS",

                    content=ft.Text(

                        "Outros",

                        color=BRANCO

                    )

                ),

            ],

            bgcolor=FUNDO,

            color=BRANCO,

            border_color=CINZA_ESCURA,

            focused_border_color=LARANJA,

            label_style=ft.TextStyle(

                color=CINZA

            ),

            menu_style=ft.MenuStyle(

                bgcolor=ft.Colors.GREY_900

            ),

        )



        mensagem_edicao = ft.Text(

            "",

            color=LARANJA,

            size=13,

        )



        def salvar(e):

            mensagem_edicao.value = ""



            if not campo_descricao.value.strip():

                mensagem_edicao.value = (

                    "Digite a descrição."

                )

                page.update()

                return



            try:

                valor = converter_valor(

                    campo_valor.value

                )



            except ValueError:

                mensagem_edicao.value = (

                    "Digite um valor válido."

                )

                page.update()

                return



            if valor <= 0:

                mensagem_edicao.value = (

                    "O valor deve ser maior que zero."

                )

                page.update()

                return



            try:

                editar_movimentacao_servico(

                    id_movimento,

                    campo_descricao.value.strip(),

                    valor,

                    campo_categoria.value or "OUTROS",

                    data_atual,

                )



            except Exception as erro:

                mensagem_edicao.value = str(erro)

                page.update()

                return



            page.pop_dialog()

            fechar_detalhes()



            abrir_detalhes_servico(

                id_servico

            )



        dialogo = ft.AlertDialog(

            modal=True,

            bgcolor=ft.Colors.GREY_900,

            title=ft.Text(

                "Editar saída",

                color=BRANCO,

                weight=ft.FontWeight.BOLD,

            ),

            content=ft.Container(

                bgcolor=ft.Colors.GREY_900,

                content=ft.Column(

                    controls=[

                        campo_descricao,

                        ft.Row(

                            controls=[

                                campo_valor,

                                campo_categoria,

                            ],

                            wrap=True,

                            spacing=10,

                        ),

                        mensagem_edicao,

                    ],

                    spacing=15,

                    tight=True,

                ),

            ),

            actions=[

                ft.Button(

                    "Cancelar",

                    bgcolor=ft.Colors.GREY_700,

                    color=BRANCO,

                    on_click=lambda e:

                        page.pop_dialog(),

                ),

                ft.Button(

                    "Salvar alterações",

                    bgcolor=LARANJA,

                    color=BRANCO,

                    on_click=salvar,

                ),

            ],

        )



        page.show_dialog(dialogo)



    # ======================================================

    # DETALHES DO SERVIÇO

    # ======================================================



    def abrir_detalhes_servico(id_servico):

        servicos = listar_servicos()

        servico_encontrado = None



        for s in servicos:

            if s[0] == id_servico:

                servico_encontrado = s

                break



        if servico_encontrado is None:

            mostrar_mensagem(

                "Serviço não encontrado.",

                VERMELHO,

            )

            return



        id_cliente = servico_encontrado[1]

        descricao_servico = servico_encontrado[2]

        total = servico_encontrado[3]

        valor_entrada = servico_encontrado[4]

        data = servico_encontrado[5]



        painel_principal = (

            servico_encontrado[6]

            if len(servico_encontrado) > 6

            else 0

        )



        nome_cliente = obter_nome_cliente(

            clientes,

            id_cliente,

        )



        despesas = total_saidas_servico(

            id_servico

        )



        saldo = saldo_servico(

            id_servico

        )



        restante = restante_servico(

            id_servico

        )



        texto_saldo = ft.Text(

            formatar_moeda(saldo),

            size=30,

            weight=ft.FontWeight.BOLD,

            color=VERDE if saldo >= 0 else VERMELHO,

        )



        info_servico = ft.Container(

            expand=True,

            height=78,

            bgcolor="#000000",

            border_radius=8,

            border=ft.Border.all(

                1,

                LARANJA

            ),

            padding=12,

            content=ft.Row(

                controls=[

                    ft.Column(

                        controls=[

                            ft.Text(

                                "SERVIÇO",

                                color=LARANJA,

                                size=10,

                                weight=ft.FontWeight.BOLD,

                            ),

                            ft.Text(

                                f"#{id_servico}",

                                color=BRANCO,

                                size=19,

                                weight=ft.FontWeight.BOLD,

                            ),

                        ],

                        spacing=1,

                        tight=True,

                    ),

                    ft.Container(width=20),

                    ft.Column(

                        controls=[

                            ft.Text(

                                "CLIENTE",

                                color=LARANJA,

                                size=10,

                                weight=ft.FontWeight.BOLD,

                            ),

                            ft.Text(

                                f"{id_cliente} - {nome_cliente}",

                                color=BRANCO,

                                size=13,

                            ),

                        ],

                        spacing=2,

                        tight=True,

                    ),

                    ft.Container(width=20),

                    ft.Column(

                        controls=[

                            ft.Text(

                                "DESCRIÇÃO",

                                color=LARANJA,

                                size=10,

                                weight=ft.FontWeight.BOLD,

                            ),

                            ft.Text(

                                descricao_servico,

                                color=BRANCO,

                                size=13,

                                max_lines=1,

                                overflow=ft.TextOverflow.ELLIPSIS,

                            ),

                        ],

                        spacing=2,

                        tight=True,

                        expand=True,

                    ),

                    ft.Container(width=20),

                    ft.Column(

                        controls=[

                            ft.Text(

                                "CADASTRO",

                                color=LARANJA,

                                size=10,

                                weight=ft.FontWeight.BOLD,

                            ),

                            ft.Text(

                                str(data),

                                color=BRANCO,

                                size=13,

                            ),

                        ],

                        spacing=2,

                        tight=True,

                    ),

                ],

                spacing=0,

                vertical_alignment=ft.CrossAxisAlignment.CENTER,

            ),

        )



        def criar_card_resumo(

            titulo,

            valor,

            cor=BRANCO,

            fundo=CARD

        ):

            return ft.Container(

                width=170,

                padding=12,

                bgcolor=fundo,

                border_radius=9,

                content=ft.Column(

                    controls=[

                        ft.Text(

                            titulo,

                            color=CINZA,

                            size=12,

                        ),

                        ft.Text(

                            valor,

                            color=cor,

                            size=18,

                            weight=ft.FontWeight.BOLD,

                        ),

                    ],

                    spacing=4,

                ),

            )



        card_total = criar_card_resumo(

            "Valor total",

            formatar_moeda(total)

        )



        card_entrada = criar_card_resumo(

            "Entrada inicial",

            formatar_moeda(valor_entrada)

        )



        card_restante = criar_card_resumo(

            "A receber",

            formatar_moeda(restante),

            LARANJA if restante > 0 else VERDE,

        )



        cards_pagamento = ft.Row(

            controls=[

                card_total,

                card_entrada,

                card_restante,

            ],

            spacing=10,

            wrap=True,

        )



        cabecalho_servico = ft.Column(

            controls=[

                info_servico,

                cards_pagamento,

            ],

            spacing=10,

            tight=True,

        )



        card_despesas = ft.Container(

            width=220,

            padding=15,

            bgcolor="#351919",

            border_radius=10,

            border=ft.Border.all(

                1,

                VERMELHO

            ),

            content=ft.Column(

                controls=[

                    ft.Text(

                        "DESPESAS",

                        color=VERMELHO,

                        size=14,

                        weight=ft.FontWeight.BOLD,

                    ),

                    ft.Text(

                        formatar_moeda(despesas),

                        color=VERMELHO,

                        size=24,

                        weight=ft.FontWeight.BOLD,

                    ),

                ],

                spacing=5,

            ),

        )



        card_saldo = ft.Container(

            width=220,

            padding=15,

            bgcolor="#17351F",

            border_radius=10,

            border=ft.Border.all(

                1,

                VERDE

            ),

            content=ft.Column(

                controls=[

                    ft.Text(

                        "SALDO ATUAL",

                        color=VERDE,

                        size=14,

                        weight=ft.FontWeight.BOLD,

                    ),

                    texto_saldo,

                ],

                spacing=5,

            ),

        )



        resumo = ft.Row(

            controls=[

                card_despesas,

                card_saldo,

            ],

            spacing=12,

            wrap=True,

        )



        lista_movimentos = ft.Column(

            controls=[],

            spacing=8,

            tight=True,

        )



        movimentacoes = listar_movimentacoes_servico(

            id_servico

        )



        if not movimentacoes:

            lista_movimentos.controls.append(

                ft.Container(

                    bgcolor=CARD,

                    border_radius=8,

                    padding=12,

                    content=ft.Text(

                        "Nenhuma saída registrada para este serviço.",

                        color=CINZA,

                        size=13,

                    ),

                )

            )

        else:

            tabela = ft.DataTable(

                bgcolor="#FFFFFF",

                heading_row_color="#E8E8E8",

                heading_row_height=38,

                data_row_min_height=38,

                data_row_max_height=42,

                horizontal_margin=8,

                column_spacing=12,

                divider_thickness=1,

                columns=[

                    ft.DataColumn(

                        ft.Text(

                            "Data",

                            color="#111111",

                            size=11,

                            weight=ft.FontWeight.BOLD,

                        )

                    ),

                    ft.DataColumn(

                        ft.Text(

                            "Categoria",

                            color="#111111",

                            size=11,

                            weight=ft.FontWeight.BOLD,

                        )

                    ),

                    ft.DataColumn(

                        ft.Text(

                            "Descrição",

                            color="#111111",

                            size=11,

                            weight=ft.FontWeight.BOLD,

                        )

                    ),

                    ft.DataColumn(

                        ft.Text(

                            "Valor",

                            color="#111111",

                            size=11,

                            weight=ft.FontWeight.BOLD,

                        )

                    ),

                    ft.DataColumn(

                        ft.Text(

                            "Ação",

                            color="#111111",

                            size=11,

                            weight=ft.FontWeight.BOLD,

                        )

                    ),

                ],

                rows=[],

            )



            for movimento in movimentacoes:

                tipo = movimento[2]

                descricao_mov = movimento[3]

                valor_mov = movimento[4]

                data_mov = movimento[5]

                categoria = movimento[6]



                cor_valor = (

                    VERDE

                    if tipo != "SAIDA"

                    else VERMELHO

                )



                sinal = (

                    "+"

                    if tipo != "SAIDA"

                    else "-"

                )



                tabela.rows.append(

                    ft.DataRow(

                        cells=[

                            ft.DataCell(

                                ft.Text(

                                    str(data_mov),

                                    color="#222222",

                                    size=11,

                                )

                            ),

                            ft.DataCell(

                                ft.Text(

                                    categoria or "Outros",

                                    color="#111111",

                                    size=11,

                                )

                            ),

                            ft.DataCell(

                                ft.Container(

                                    width=190,

                                    content=ft.Text(

                                        descricao_mov or "",

                                        color="#111111",

                                        size=11,

                                        max_lines=1,

                                        overflow=ft.TextOverflow.ELLIPSIS,

                                    ),

                                )

                            ),

                            ft.DataCell(

                                ft.Text(

                                    f"{sinal} "

                                    f"{formatar_moeda(valor_mov)}",

                                    color=cor_valor,

                                    size=11,

                                    weight=ft.FontWeight.BOLD,

                                )

                            ),

                            ft.DataCell(

                                ft.Button(

                                    "Editar",

                                    icon=ft.Icons.EDIT,

                                    bgcolor=ft.Colors.GREY_700,

                                    color=BRANCO,

                                    height=34,

                                    on_click=lambda e,

                                    mov=movimento:

                                        abrir_edicao_movimentacao(

                                            id_servico,

                                            mov,

                                            fechar_detalhes,

                                        ),

                                )

                            ),

                        ]

                    )

                )
                lista_movimentos.controls.append(
                ft.Container(
                    bgcolor="#FFFFFF",
                    border_radius=8,
                    padding=4,
                    content=ft.Row(
                        controls=[tabela],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                )
            )

        # ==================================================
        # CAMPOS PARA REGISTRAR SAÍDA
        # ==================================================

        descricao_saida = ft.TextField(
            label="Descrição da saída",
            hint_text="Descreva o que foi gasto...",
            width=360,
            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,
            label_style=ft.TextStyle(
                color=BRANCO
            ),
            multiline=True,
            min_lines=1,
            max_lines=2,
        )

        valor_saida = ft.TextField(
            label="Valor da saída",
            hint_text="Ex.: 500,00",
            width=190,
            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,
            label_style=ft.TextStyle(
                color=CINZA
            ),
        )

        # ==================================================
        # CATEGORIA
        # ==================================================

        categoria_saida = ft.Dropdown(
            label="Categoria",
            hint_text="Selecione",
            width=220,
            options=[
                ft.DropdownOption(
                    key="MDF",
                    content=ft.Text(
                        "MDF",
                        color=BRANCO
                    )
                ),
                ft.DropdownOption(
                    key="FERRAGEM",
                    content=ft.Text(
                        "Ferragens",
                        color=BRANCO
                    )
                ),
                ft.DropdownOption(
                    key="GASOLINA",
                    content=ft.Text(
                        "Gasolina",
                        color=BRANCO
                    )
                ),
                ft.DropdownOption(
                    key="OUTROS",
                    content=ft.Text(
                        "Outros",
                        color=BRANCO
                    )
                ),
            ],
            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,
            label_style=ft.TextStyle(
                color=BRANCO
            ),
            menu_style=ft.MenuStyle(
                bgcolor=ft.Colors.GREY_900
            ),
        )

        mensagem_saida = ft.Text(
            "",
            color=LARANJA,
            size=13,
        )

        # ==================================================
        # REGISTRAR SAÍDA
        # ==================================================

        def registrar_saida(e):

            mensagem_saida.value = ""

            if not descricao_saida.value.strip():
                mensagem_saida.value = (
                    "Digite a descrição da saída."
                )
                page.update()
                return

            if categoria_saida.value is None:
                mensagem_saida.value = (
                    "Selecione uma categoria."
                )
                page.update()
                return

            try:
                valor = converter_valor(
                    valor_saida.value
                )

            except ValueError:
                mensagem_saida.value = (
                    "Digite um valor válido."
                )
                page.update()
                return

            if valor <= 0:
                mensagem_saida.value = (
                    "O valor deve ser maior que zero."
                )
                page.update()
                return

            try:
                adicionar_movimentacao_servico(
                    id_servico,
                    "SAIDA",
                    descricao_saida.value.strip(),
                    valor,
                    categoria_saida.value,
                )

            except Exception as erro:
                mensagem_saida.value = str(erro)
                page.update()
                return

            page.pop_dialog()
            fechar_detalhes()

            abrir_detalhes_servico(
                id_servico
            )

        # ==================================================
        # BLOCO REGISTRAR SAÍDA
        # ==================================================

        formulario_saida = ft.Container(
            width=700,
            bgcolor=CARD,
            border_radius=8,
            padding=8,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Registrar saída",
                        color=BRANCO,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Row(
                        controls=[
                            categoria_saida,
                            valor_saida,
                        ],
                        wrap=True,
                        spacing=10,
                    ),

                    descricao_saida,
                    mensagem_saida,
                ],
                spacing=8,
            ),
        )

        botao_registrar_saida = ft.Button(
            "Registrar saída",
            icon=ft.Icons.ADD,
            bgcolor=LARANJA,
            color=BRANCO,
            height=36,
            on_click=registrar_saida,
        )

        formulario_saida.content.controls.append(
            botao_registrar_saida
        )

        # ==================================================
        # EDITAR SERVIÇO
        # ==================================================

        campo_editar_cliente = ft.Dropdown(
            label="Cliente",
            value=str(id_cliente),

            options=[
                ft.DropdownOption(
                    key=str(c[0]),
                    content=ft.Text(
                        f"{c[0]} - {c[1]}",
                        color=BRANCO
                    )
                )
                for c in clientes
            ],

            width=500,
            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,

            label_style=ft.TextStyle(
                color=CINZA
            ),

            menu_style=ft.MenuStyle(
                bgcolor=ft.Colors.GREY_900
            ),
        )

        campo_editar_descricao = ft.TextField(
            label="Descrição do serviço",
            value=descricao_servico,
            width=500,
            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,
            label_style=ft.TextStyle(
                color=CINZA
            ),
            multiline=True,
            min_lines=2,
            max_lines=4,
        )

        campo_editar_total = ft.TextField(
            label="Valor total",
            value=f"{total:.2f}".replace(".", ","),
            width=240,
            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,
            label_style=ft.TextStyle(
                color=CINZA
            ),
        )

        # ==================================================
        # ENTRADA INICIAL
        # ==================================================

        campo_editar_entrada = ft.TextField(
            label="Entrada inicial",
            value=f"{valor_entrada:.2f}".replace(".", ","),
            width=240,
            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,
            label_style=ft.TextStyle(
                color=CINZA
            ),
        )

        mensagem_editar_servico = ft.Text(
            "",
            color=LARANJA,
            size=13,
        )

        # ==================================================
        # SALVAR EDIÇÃO DO SERVIÇO
        # ==================================================

        def salvar_edicao_servico(e):

            mensagem_editar_servico.value = ""

            if campo_editar_cliente.value is None:
                mensagem_editar_servico.value = (
                    "Selecione um cliente."
                )
                page.update()
                return

            if not campo_editar_descricao.value.strip():
                mensagem_editar_servico.value = (
                    "Digite a descrição."
                )
                page.update()
                return

            try:
                novo_total = converter_valor(
                    campo_editar_total.value
                )

            except ValueError:
                mensagem_editar_servico.value = (
                    "Digite um valor válido."
                )
                page.update()
                return

            if novo_total <= 0:
                mensagem_editar_servico.value = (
                    "O valor total deve ser maior que zero."
                )
                page.update()
                return

            try:
                nova_entrada = converter_valor(
                    campo_editar_entrada.value
                )

            except ValueError:
                mensagem_editar_servico.value = (
                    "Digite um valor de entrada válido."
                )
                page.update()
                return

            if nova_entrada < 0:
                mensagem_editar_servico.value = (
                    "A entrada não pode ser negativa."
                )
                page.update()
                return

            if nova_entrada > novo_total:
                mensagem_editar_servico.value = (
                    "A entrada não pode ser maior "
                    "que o valor total."
                )
                page.update()
                return

            try:
                editar_servico(
                    id_servico,
                    int(
                        campo_editar_cliente.value
                    ),
                    campo_editar_descricao.value.strip(),
                    novo_total,
                    nova_entrada,
                )

            except Exception as erro:
                mensagem_editar_servico.value = str(erro)
                page.update()
                return

            page.pop_dialog()
            fechar_detalhes()
            atualizar_lista()

        # ==================================================
        # DIÁLOGO DE EDIÇÃO
        # ==================================================

        dialogo_editar_servico = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.GREY_900,

            title=ft.Text(
                f"Editar serviço #{id_servico}",
                color=BRANCO,
                weight=ft.FontWeight.BOLD,
            ),

            content=ft.Container(
                bgcolor=ft.Colors.GREY_900,

                content=ft.Column(
                    controls=[
                        campo_editar_cliente,

                        campo_editar_descricao,

                        ft.Row(
                            controls=[
                                campo_editar_total,
                                campo_editar_entrada,
                            ],
                            wrap=True,
                            spacing=10,
                        ),

                        mensagem_editar_servico,
                    ],
                    spacing=15,
                    tight=True,
                ),
            ),

            actions=[
                ft.Button(
                    "Cancelar",
                    bgcolor=ft.Colors.GREY_700,
                    color=BRANCO,
                    on_click=lambda e:
                        page.pop_dialog(),
                ),

                ft.Button(
                    "Salvar alterações",
                    bgcolor=LARANJA,
                    color=BRANCO,
                    on_click=salvar_edicao_servico,
                ),
            ],
        )

        def abrir_edicao_servico(e):
            page.show_dialog(
                dialogo_editar_servico
            )

        botao_editar_servico = ft.Button(
            "Editar serviço",
            icon=ft.Icons.EDIT,
            bgcolor=ft.Colors.GREY_700,
            color=BRANCO,
            on_click=abrir_edicao_servico,
        )

        # ==================================================
        # PAINEL PRINCIPAL
        # ==================================================

        def adicionar_ao_painel(e):

            try:
                adicionar_servico_painel(
                    id_servico
                )

                page.pop_dialog()
                fechar_detalhes()
                atualizar_lista()

            except Exception as erro:
                mostrar_mensagem(
                    str(erro),
                    VERMELHO,
                )

        def remover_do_painel(e):

            try:
                remover_servico_painel(
                    id_servico
                )

                page.pop_dialog()
                fechar_detalhes()
                atualizar_lista()

            except Exception as erro:
                mostrar_mensagem(
                    str(erro),
                    VERMELHO,
                )

        if painel_principal:

            botao_painel = ft.Button(
                "Remover do painel principal",
                bgcolor=ft.Colors.GREY_700,
                color=BRANCO,
                on_click=remover_do_painel,
            )

        else:

            botao_painel = ft.Button(
                "Adicionar ao painel principal",
                bgcolor=LARANJA,
                color=BRANCO,
                on_click=adicionar_ao_painel,
            )

        botoes_servico = ft.Row(
            controls=[
                botao_editar_servico,
                botao_painel,
            ],
            spacing=10,
            wrap=True,
        )

        # ==================================================
        # CONTEÚDO DA FICHA
        # ==================================================

        conteudo_detalhes = ft.Column(
            controls=[
                cabecalho_servico,
                resumo,
                botoes_servico,
                formulario_saida,

                ft.Text(
                    "Saídas do serviço",
                    color=BRANCO,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),

                lista_movimentos,
            ],
            spacing=15,
            tight=True,
            scroll=ft.ScrollMode.AUTO,
        )

        def fechar_detalhes():
            page.pop_dialog()

        # ==================================================
        # JANELA DA FICHA
        # ==================================================

        janela_detalhes = ft.BottomSheet(
            bgcolor=FUNDO,
            fullscreen=True,
            scrollable=True,

            content=ft.Container(
                expand=True,
                bgcolor=FUNDO,
                padding=20,
                content=conteudo_detalhes,
            ),
        )

        page.show_dialog(
            janela_detalhes
        )
            # ======================================================
    # ATUALIZAR LISTA DE SERVIÇOS
    # ======================================================

    def atualizar_lista():

        lista_servicos.controls.clear()

        servicos = listar_servicos()

        if not servicos:

            lista_servicos.controls.append(
                ft.Container(
                    bgcolor=CARD,
                    padding=20,
                    border_radius=10,
                    content=ft.Text(
                        "Nenhum serviço cadastrado ainda.",
                        color=CINZA,
                        size=14,
                    ),
                )
            )

            page.update()
            return

        for servico in servicos:

            id_servico = servico[0]
            id_cliente = servico[1]
            descricao_servico = servico[2]
            total = servico[3]
            valor_entrada = servico[4]
            data = servico[5]

            painel_principal = (
                servico[6]
                if len(servico) > 6
                else 0
            )

            nome_cliente = obter_nome_cliente(
                clientes,
                id_cliente,
            )

            despesas = total_saidas_servico(
                id_servico
            )

            saldo = saldo_servico(
                id_servico
            )

            restante = restante_servico(
                id_servico
            )

            # ==================================================
            # STATUS DO SERVIÇO
            # ==================================================

            if restante <= 0:
                status_texto = "ENTREGUE"
                status_cor = VERDE

            elif despesas > 0:
                status_texto = "EM PRODUÇÃO"
                status_cor = VERDE

            else:
                status_texto = "ORÇAMENTO"
                status_cor = LARANJA

            # ==================================================
            # CARD DO SERVIÇO
            # ==================================================

            card = ft.Container(
                bgcolor=CARD,
                border_radius=12,
                padding=16,

                on_click=lambda e,
                sid=id_servico:
                    abrir_detalhes_servico(
                        sid
                    ),

                content=ft.Column(
                    controls=[

                        # ==========================================
                        # CABEÇALHO
                        # ==========================================

                        ft.Row(
                            controls=[

                                ft.Text(
                                    f"Serviço #{id_servico}",
                                    size=17,
                                    color=BRANCO,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Container(
                                    expand=True
                                ),

                                ft.Container(
                                    bgcolor=status_cor,
                                    border_radius=20,
                                    padding=ft.Padding(
                                        left=10,
                                        right=10,
                                        top=5,
                                        bottom=5,
                                    ),
                                    content=ft.Text(
                                        status_texto,
                                        size=10,
                                        color="#000000",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ),

                                ft.Container(
                                    width=10
                                ),

                                ft.Text(
                                    "NO PAINEL"
                                    if painel_principal
                                    else "",
                                    size=11,
                                    color=LARANJA,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            vertical_alignment=(
                                ft.CrossAxisAlignment.CENTER
                            ),
                        ),

                        # ==========================================
                        # CLIENTE
                        # ==========================================

                        ft.Text(
                            f"Cliente: "
                            f"{id_cliente} - "
                            f"{nome_cliente}",
                            color=BRANCO,
                            size=14,
                        ),

                        # ==========================================
                        # DESCRIÇÃO
                        # ==========================================

                        ft.Text(
                            f"Descrição: "
                            f"{descricao_servico}",
                            color=CINZA,
                            size=13,
                            max_lines=2,
                            overflow=(
                                ft.TextOverflow.ELLIPSIS
                            ),
                        ),

                        ft.Divider(
                            color=ft.Colors.GREY_800
                        ),

                        # ==========================================
                        # INFORMAÇÕES FINANCEIRAS
                        # ==========================================

                        ft.Row(
                            controls=[

                                ft.Column(
                                    controls=[

                                        ft.Text(
                                            "Valor total",
                                            color=CINZA,
                                            size=11,
                                        ),

                                        ft.Text(
                                            formatar_moeda(
                                                total
                                            ),
                                            color=BRANCO,
                                            size=14,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                        ),
                                    ],
                                    spacing=2,
                                ),

                                ft.Column(
                                    controls=[

                                        ft.Text(
                                            "Entrada",
                                            color=CINZA,
                                            size=11,
                                        ),

                                        ft.Text(
                                            formatar_moeda(
                                                valor_entrada
                                            ),
                                            color=VERDE,
                                            size=14,
                                        ),
                                    ],
                                    spacing=2,
                                ),

                                ft.Column(
                                    controls=[

                                        ft.Text(
                                            "Despesas",
                                            color=CINZA,
                                            size=11,
                                        ),

                                        ft.Text(
                                            formatar_moeda(
                                                despesas
                                            ),
                                            color=VERMELHO,
                                            size=14,
                                        ),
                                    ],
                                    spacing=2,
                                ),

                                ft.Column(
                                    controls=[

                                        ft.Text(
                                            "A receber",
                                            color=CINZA,
                                            size=11,
                                        ),

                                        ft.Text(
                                            formatar_moeda(
                                                restante
                                            ),
                                            color=(
                                                LARANJA
                                                if restante > 0
                                                else VERDE
                                            ),
                                            size=14,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                        ),
                                    ],
                                    spacing=2,
                                ),

                                ft.Column(
                                    controls=[

                                        ft.Text(
                                            "Saldo",
                                            color=CINZA,
                                            size=11,
                                        ),

                                        ft.Text(
                                            formatar_moeda(
                                                saldo
                                            ),
                                            color=(
                                                VERDE
                                                if saldo >= 0
                                                else VERMELHO
                                            ),
                                            size=14,
                                            weight=(
                                                ft.FontWeight.BOLD
                                            ),
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            ],
                            spacing=15,
                            wrap=True,
                        ),

                        # ==========================================
                        # DATA
                        # ==========================================

                        ft.Text(
                            f"Cadastro: {data}",
                            color=CINZA,
                            size=11,
                        ),

                        # ==========================================
                        # INDICAÇÃO
                        # ==========================================

                        ft.Text(
                            "Clique para abrir a ficha financeira",
                            color=LARANJA,
                            size=12,
                        ),
                    ],
                    spacing=8,
                ),
            )

            lista_servicos.controls.append(
                card
            )

        page.update()

    # ======================================================
    # SALVAR NOVO SERVIÇO
    # ======================================================

    def salvar(e):

        mensagem.value = ""

        if cliente.value is None:
            mensagem.value = (
                "Selecione um cliente."
            )
            page.update()
            return

        if not descricao.value.strip():
            mensagem.value = (
                "Digite a descrição do serviço."
            )
            page.update()
            return

        if not valor_total.value.strip():
            mensagem.value = (
                "Digite o valor total."
            )
            page.update()
            return

        if not entrada.value.strip():
            mensagem.value = (
                "Digite o valor da entrada."
            )
            page.update()
            return

        try:
            total = converter_valor(
                valor_total.value
            )

            valor_entrada = converter_valor(
                entrada.value
            )

        except ValueError:
            mensagem.value = (
                "Digite valores válidos."
            )
            page.update()
            return

        if total <= 0:
            mensagem.value = (
                "O valor total deve ser maior que zero."
            )
            page.update()
            return

        if valor_entrada < 0:
            mensagem.value = (
                "A entrada não pode ser negativa."
            )
            page.update()
            return

        if valor_entrada > total:
            mensagem.value = (
                "A entrada não pode ser maior "
                "que o valor total."
            )
            page.update()
            return

        try:
            cadastrar_servico(
                int(cliente.value),
                descricao.value.strip(),
                total,
                valor_entrada,
            )

        except Exception as erro:
            mensagem.value = str(erro)
            page.update()
            return

        mensagem.value = (
            "Serviço cadastrado com sucesso."
        )

        cliente.value = None
        descricao.value = ""
        valor_total.value = ""
        entrada.value = ""

        atualizar_lista()

        page.update()

    # ======================================================
    # BOTÃO SALVAR
    # ======================================================

    botao_salvar = ft.Button(
        "Cadastrar serviço",
        icon=ft.Icons.SAVE,
        bgcolor=LARANJA,
        color=BRANCO,
        on_click=salvar,
    )

    # ======================================================
    # TÍTULO
    # ======================================================

    titulo = ft.Text(
        "Serviços",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=BRANCO,
    )

    subtitulo = ft.Text(
        "Cadastre e acompanhe os serviços da empresa",
        size=14,
        color=CINZA,
    )

    # ======================================================
    # FORMULÁRIO
    # ======================================================

    formulario = ft.Container(
        bgcolor=CARD,
        border_radius=12,
        padding=20,

        content=ft.Column(
            controls=[

                ft.Text(
                    "Novo serviço",
                    size=18,
                    color=BRANCO,
                    weight=ft.FontWeight.BOLD,
                ),

                cliente,

                descricao,

                ft.Row(
                    controls=[
                        valor_total,
                        entrada,
                    ],
                    spacing=15,
                    wrap=True,
                ),

                ft.Row(
                    controls=[
                        botao_salvar,
                        mensagem,
                    ],
                    spacing=15,
                    wrap=True,
                ),
            ],
            spacing=15,
        ),
    )

    # ======================================================
    # LISTA DE SERVIÇOS
    # ======================================================

    lista_container = ft.Container(
        bgcolor=CARD,
        border_radius=12,
        padding=20,

        content=ft.Column(
            controls=[

                ft.Text(
                    "Serviços cadastrados",
                    size=18,
                    color=BRANCO,
                    weight=ft.FontWeight.BOLD,
                ),

                lista_servicos,
            ],
            spacing=15,
            tight=True,
        ),
    )
        # ======================================================
    # ÁREA PRINCIPAL
    # ======================================================

    area_principal = ft.Container(
        expand=True,
        padding=30,

        content=ft.Column(
            controls=[
                titulo,

                subtitulo,

                ft.Container(
                    height=15
                ),

                formulario,

                ft.Container(
                    height=15
                ),

                lista_container,
            ],

            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # ======================================================
    # COLOCAR NA ÁREA DO DASHBOARD
    # ======================================================

    if area_conteudo is not None:

        area_conteudo.content = area_principal

        area_conteudo.update()

    else:

        page.add(
            area_principal
        )

    # ======================================================
    # CARREGAR LISTA INICIAL
    # ======================================================

    atualizar_lista()

    # ======================================================
    # ABRIR SERVIÇO AUTOMATICAMENTE
    # ======================================================

    if id_servico_abrir is not None:

        abrir_detalhes_servico(
            id_servico_abrir
        )