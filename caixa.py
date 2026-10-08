import flet as ft

from datetime import datetime

from database import (
    listar_caixa,
    saldo_caixa,
    adicionar_caixa,
    conectar,
)

# ==========================================================
# CORES
# ==========================================================

LARANJA = "#F75E00"
FUNDO = "#171717"
CARD = "#242424"
CARD_2 = "#2D2D2D"
BRANCO = "#FFFFFF"
CINZA = "#AAAAAA"
CINZA_ESCURA = "#777777"
VERDE = "#22C55E"
VERMELHO = "#EF4444"

# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def formatar_moeda(valor):
    valor = float(valor or 0)
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X")
    texto = texto.replace(".", ",")
    texto = texto.replace("X", ".")
    return f"R$ {texto}"

def converter_valor(texto):
    texto = (texto or "").strip()

    if not texto:
        raise ValueError("Digite o valor.")

    return float(
        texto
        .replace(".", "")
        .replace(",", ".")
    )

# ==========================================================
# TELA DO CAIXA
# ==========================================================

def mostrar_caixa(page: ft.Page, area_conteudo=None):

    page.title = "Rafá Mobile - Caixa"
    page.bgcolor = FUNDO
    page.padding = 0

    # ======================================================
    # RESUMO
    # ======================================================

    saldo_texto = ft.Text(
        "R$ 0,00",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=VERDE,
    )

    entradas_texto = ft.Text(
        "R$ 0,00",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=BRANCO,
    )

    saidas_texto = ft.Text(
        "R$ 0,00",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=BRANCO,
    )

    # ======================================================
    # LISTA DE MOVIMENTAÇÕES
    # ======================================================

    lista_movimentos = ft.Column(
        spacing=8,
        tight=True,
    )

    # ======================================================
    # MENSAGEM
    # ======================================================

    mensagem = ft.Text(
        "",
        size=13,
        color=VERDE,
    )

    # ======================================================
    # ATUALIZAR CAIXA
    # ======================================================

    def atualizar_caixa():

        movimentos = listar_caixa()

        total_entradas = sum(
            float(item["valor"])
            for item in movimentos
            if item["tipo"] == "ENTRADA"
        )

        total_saidas = sum(
            float(item["valor"])
            for item in movimentos
            if item["tipo"] == "SAIDA"
        )

        saldo = saldo_caixa()

        # ----------------------------------------------
        # SALDO
        # ----------------------------------------------

        saldo_texto.value = formatar_moeda(saldo)

        saldo_texto.color = (
            VERDE
            if saldo >= 0
            else VERMELHO
        )

        # ----------------------------------------------
        # ENTRADAS
        # ----------------------------------------------

        entradas_texto.value = formatar_moeda(
            total_entradas
        )

        # ----------------------------------------------
        # SAÍDAS
        # ----------------------------------------------

        saidas_texto.value = formatar_moeda(
            total_saidas
        )

        # ----------------------------------------------
        # LISTA
        # ----------------------------------------------

        lista_movimentos.controls.clear()

        if not movimentos:

            lista_movimentos.controls.append(
                ft.Container(
                    bgcolor=CARD,
                    border_radius=10,
                    padding=20,
                    content=ft.Text(
                        "Nenhuma movimentação registrada.",
                        color=CINZA,
                        size=14,
                    ),
                )
            )

        else:

            for movimento in movimentos:

                id_movimento = movimento["id_caixa"]
                tipo = movimento["tipo"]
                descricao = movimento["descricao"]
                valor = float(movimento["valor"])
                data = movimento["data_movimentacao"]

                if tipo == "ENTRADA":

                    sinal = "+"
                    cor_valor = VERDE
                    texto_tipo = "ENTRADA"

                else:

                    sinal = "-"
                    cor_valor = VERMELHO
                    texto_tipo = "SAÍDA"

                # --------------------------------------
                # BOTÃO EDITAR
                # --------------------------------------

                botao_editar = ft.Button(
                    "Editar",
                    icon=ft.Icons.EDIT,
                    bgcolor=ft.Colors.GREY_700,
                    color=BRANCO,
                    on_click=lambda e, mov=movimento:
                        abrir_edicao(mov),
                )

                # --------------------------------------
                # MOVIMENTAÇÃO
                # --------------------------------------

                item = ft.Container(
                    bgcolor=CARD,
                    border_radius=10,
                    padding=15,
                    content=ft.Row(
                        controls=[

                            ft.Container(
                                width=100,
                                content=ft.Text(
                                    str(data),
                                    color=CINZA,
                                    size=12,
                                ),
                            ),

                            ft.Container(
                                width=100,
                                content=ft.Text(
                                    texto_tipo,
                                    color=cor_valor,
                                    weight=ft.FontWeight.BOLD,
                                    size=12,
                                ),
                            ),

                            ft.Container(
                                expand=True,
                                content=ft.Text(
                                    descricao,
                                    color=BRANCO,
                                    size=14,
                                ),
                            ),

                            ft.Container(
                                width=150,
                                content=ft.Text(
                                    f"{sinal} "
                                    f"{formatar_moeda(valor)}",
                                    color=cor_valor,
                                    weight=ft.FontWeight.BOLD,
                                    size=14,
                                ),
                            ),

                            botao_editar,

                        ],
                        spacing=10,
                    ),
                )

                lista_movimentos.controls.append(item)

        page.update()

    # ======================================================
    # EDITAR MOVIMENTAÇÃO
    # ======================================================

    def abrir_edicao(movimento):

        id_movimento = movimento["id_caixa"]
        tipo_atual = movimento["tipo"]
        descricao_atual = movimento["descricao"]
        valor_atual = movimento["valor"]

        campo_tipo = ft.Dropdown(
            label="Tipo",
            value=tipo_atual,
            width=250,

            options=[
                ft.DropdownOption(
                    key="ENTRADA",
                    text="Entrada",
                ),
                ft.DropdownOption(
                    key="SAIDA",
                    text="Saída",
                ),
            ],

            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,

            label_style=ft.TextStyle(
                color=CINZA,
            ),

            menu_style=ft.MenuStyle(
                bgcolor=ft.Colors.GREY_900,
            ),
        )

        campo_descricao = ft.TextField(
            label="Descrição",
            value=descricao_atual,
            width=500,

            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,

            label_style=ft.TextStyle(
                color=CINZA,
            ),
        )

        campo_valor = ft.TextField(
            label="Valor",
            value=(
                f"{float(valor_atual):.2f}"
                .replace(".", ",")
            ),
            width=250,

            bgcolor=FUNDO,
            color=BRANCO,
            border_color=CINZA_ESCURA,
            focused_border_color=LARANJA,

            label_style=ft.TextStyle(
                color=CINZA,
            ),
        )

        mensagem_edicao = ft.Text(
            "",
            size=13,
            color=VERMELHO,
        )

        def salvar_edicao(e):

            mensagem_edicao.value = ""

            # ------------------------------------------
            # VALIDA TIPO
            # ------------------------------------------

            if not campo_tipo.value:

                mensagem_edicao.value = (
                    "Selecione o tipo."
                )

                page.update()
                return

            # ------------------------------------------
            # VALIDA DESCRIÇÃO
            # ------------------------------------------

            if not campo_descricao.value.strip():

                mensagem_edicao.value = (
                    "Digite a descrição."
                )

                page.update()
                return

            # ------------------------------------------
            # VALIDA VALOR
            # ------------------------------------------

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

            # ------------------------------------------
            # ATUALIZA NO BANCO
            # ------------------------------------------

            try:

                with conectar() as conn:

                    conn.execute(
                        """
                        UPDATE caixa
                        SET
                            tipo = ?,
                            descricao = ?,
                            valor = ?
                        WHERE id_caixa = ?
                        """,
                        (
                            campo_tipo.value,
                            campo_descricao.value.strip(),
                            valor,
                            id_movimento,
                        ),
                    )

            except Exception as erro:

                mensagem_edicao.value = str(erro)

                page.update()
                return

            # ------------------------------------------
            # FECHAR
            # ------------------------------------------

            page.pop_dialog()
            atualizar_caixa()

        dialogo = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.GREY_900,

            title=ft.Text(
                "Editar movimentação",
                color=BRANCO,
                weight=ft.FontWeight.BOLD,
            ),

            content=ft.Container(
                bgcolor=ft.Colors.GREY_900,

                content=ft.Column(
                    controls=[
                        campo_tipo,
                        campo_descricao,
                        campo_valor,
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
                    on_click=salvar_edicao,
                ),
            ],
        )

        page.show_dialog(dialogo)

    # ======================================================
    # NOVA MOVIMENTAÇÃO
    # ======================================================

    tipo_movimento = ft.Dropdown(
        label="Tipo",
        hint_text="Selecione",
        width=250,

        options=[
            ft.DropdownOption(
                key="ENTRADA",
                text="Entrada",
                content=ft.Text(
                    "Entrada",
                    color=BRANCO,
                ),
            ),

            ft.DropdownOption(
                key="SAIDA",
                text="Saída",
                content=ft.Text(
                    "Saída",
                    color=BRANCO,
                ),
            ),
        ],

        bgcolor=FUNDO,
        color=BRANCO,
        border_color=CINZA_ESCURA,
        focused_border_color=LARANJA,

        label_style=ft.TextStyle(
            color=CINZA,
        ),

        menu_style=ft.MenuStyle(
            bgcolor=ft.Colors.GREY_900,
        ),
    )

    descricao_movimento = ft.TextField(
        label="Descrição",
        hint_text=(
            "Ex.: Pagamento recebido, "
            "compra de material, combustível..."
        ),
        width=500,

        bgcolor=FUNDO,
        color=BRANCO,
        border_color=CINZA_ESCURA,
        focused_border_color=LARANJA,

        label_style=ft.TextStyle(
            color=CINZA,
        ),
    )

    valor_movimento = ft.TextField(
        label="Valor",
        hint_text="Ex.: 500,00",
        width=250,

        bgcolor=FUNDO,
        color=BRANCO,
        border_color=CINZA_ESCURA,
        focused_border_color=LARANJA,

        label_style=ft.TextStyle(
            color=CINZA,
        ),
    )

    def registrar_movimentacao(e):

        mensagem.value = ""
        mensagem.color = VERDE

        # ----------------------------------------------
        # TIPO
        # ----------------------------------------------

        if not tipo_movimento.value:

            mensagem.value = (
                "Selecione Entrada ou Saída."
            )

            mensagem.color = VERMELHO
            page.update()
            return

        # ----------------------------------------------
        # DESCRIÇÃO
        # ----------------------------------------------

        if not descricao_movimento.value.strip():

            mensagem.value = (
                "Digite a descrição."
            )

            mensagem.color = VERMELHO
            page.update()
            return

        # ----------------------------------------------
        # VALOR
        # ----------------------------------------------

        try:

            valor = converter_valor(
                valor_movimento.value
            )

        except ValueError:

            mensagem.value = (
                "Digite um valor válido."
            )

            mensagem.color = VERMELHO
            page.update()
            return

        if valor <= 0:

            mensagem.value = (
                "O valor deve ser maior que zero."
            )

            mensagem.color = VERMELHO
            page.update()
            return

        # ----------------------------------------------
        # DATA
        # ----------------------------------------------

        data = datetime.now().strftime(
            "%Y-%m-%d"
        )

        # ----------------------------------------------
        # SALVAR
        # ----------------------------------------------

        try:

            adicionar_caixa(
                tipo=tipo_movimento.value,
                descricao=(
                    descricao_movimento.value
                    .strip()
                ),
                valor=valor,
                data_movimentacao=data,
                id_servico=None,
                origem="CAIXA_EMPRESA",
            )

        except Exception as erro:

            mensagem.value = str(erro)
            mensagem.color = VERMELHO

            page.update()
            return

        # ----------------------------------------------
        # LIMPAR
        # ----------------------------------------------

        tipo_movimento.value = None
        descricao_movimento.value = ""
        valor_movimento.value = ""

        mensagem.value = (
            "Movimentação registrada com sucesso."
        )

        mensagem.color = VERDE

        atualizar_caixa()

    # ======================================================
    # BOTÃO
    # ======================================================

    botao_registrar = ft.Button(
        "Registrar movimentação",
        icon=ft.Icons.SAVE,
        bgcolor=LARANJA,
        color=BRANCO,
        on_click=registrar_movimentacao,
    )

    # ======================================================
    # FORMULÁRIO
    # ======================================================

    formulario = ft.Container(
        width=650,
        bgcolor=CARD,
        border_radius=12,
        padding=20,

        content=ft.Column(
            controls=[

                ft.Text(
                    "Nova movimentação",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=BRANCO,
                ),

                ft.Row(
                    controls=[
                        tipo_movimento,
                        valor_movimento,
                    ],
                    spacing=15,
                    wrap=True,
                ),

                descricao_movimento,

                ft.Row(
                    controls=[
                        botao_registrar,
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
    # CARDS DO RESUMO
    # ======================================================

    card_saldo = ft.Container(
        padding=20,
        width=220,
        bgcolor=CARD,
        border_radius=10,

        border=ft.Border.all(
            1,
            VERDE,
        ),

        content=ft.Column(
            controls=[

                ft.Text(
                    "Saldo atual",
                    color=CINZA,
                    size=13,
                ),

                saldo_texto,

            ],

            spacing=5,
        ),
    )

    card_entradas = ft.Container(
        padding=20,
        width=220,
        bgcolor=CARD,
        border_radius=10,

        content=ft.Column(
            controls=[

                ft.Text(
                    "Entradas",
                    color=CINZA,
                    size=13,
                ),

                entradas_texto,

            ],

            spacing=5,
        ),
    )

    card_saidas = ft.Container(
        padding=20,
        width=220,
        bgcolor=CARD,
        border_radius=10,

        content=ft.Column(
            controls=[

                ft.Text(
                    "Saídas",
                    color=CINZA,
                    size=13,
                ),

                saidas_texto,

            ],

            spacing=5,
        ),
    )
        # ======================================================
    # CONTEÚDO PRINCIPAL
    # ======================================================

    conteudo = ft.Column(
        controls=[

            # ------------------------------------------
            # TÍTULO
            # ------------------------------------------

            ft.Text(
                "Caixa da empresa",
                size=25,
                weight=ft.FontWeight.BOLD,
                color=BRANCO,
            ),

            ft.Text(
                "Controle das entradas e saídas da empresa",
                size=14,
                color=CINZA,
            ),

            ft.Divider(),

            # ------------------------------------------
            # RESUMO
            # ------------------------------------------

            ft.Row(
                controls=[
                    card_saldo,
                    card_entradas,
                    card_saidas,
                ],
                spacing=15,
                wrap=True,
            ),

            ft.Divider(),

            # ------------------------------------------
            # NOVA MOVIMENTAÇÃO
            # ------------------------------------------

            ft.Row(
                controls=[
                    formulario,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),

            ft.Divider(),

            # ------------------------------------------
            # MOVIMENTAÇÕES
            # ------------------------------------------

            ft.Text(
                "Movimentações do caixa",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=BRANCO,
            ),

            ft.Container(
                bgcolor=CARD_2,
                border_radius=8,
                padding=12,

                content=ft.Row(
                    controls=[

                        ft.Text(
                            "Data",
                            width=100,
                            color=CINZA,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            "Tipo",
                            width=100,
                            color=CINZA,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            "Descrição",
                            expand=True,
                            color=CINZA,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            "Valor",
                            width=150,
                            color=CINZA,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            "Ação",
                            width=90,
                            color=CINZA,
                            weight=ft.FontWeight.BOLD,
                        ),

                    ],
                    spacing=10,
                ),
            ),

            lista_movimentos,

        ],

        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # ======================================================
    # MOSTRAR NA ÁREA PRINCIPAL
    # ======================================================

    if area_conteudo is not None:

        area_conteudo.content = ft.Container(
            expand=True,
            bgcolor=FUNDO,

            # Espaço entre o menu lateral e o conteúdo
            padding=30,

            content=ft.Container(
                width=1100,
                content=conteudo,
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
                    width=1100,
                    content=conteudo,
                ),
            )
        )

        page.bgcolor = FUNDO

        page.update()

    # ======================================================
    # CARREGAR DADOS
    # ======================================================

    atualizar_caixa()