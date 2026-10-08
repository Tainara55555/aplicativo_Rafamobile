import flet as ft

import os

import shutil

import webbrowser

from datetime import datetime

from database import (
    listar_clientes,
    listar_servicos,
    cadastrar_documento,
    listar_documentos,
    editar_documento,
    obter_documento,
    remover_documento,
)

LARANJA = "#F75E00"
FUNDO = "#000000"
MENU = "#202020"
CARD = "#242424"
BRANCO = "#FFFFFF"
CINZA = "#AAAAAA"
VERDE = "#22C55E"
VERMELHO = "#EF4444"

PASTA_DOCUMENTOS = "documentos"


def criar_pasta_documentos():

    os.makedirs(
        PASTA_DOCUMENTOS,
        exist_ok=True
    )


def mostrar_registros(

    page,

    area_conteudo=None

):

    criar_pasta_documentos()

    clientes = listar_clientes()

    servicos = listar_servicos()

    mapa_clientes = {}


    for cliente in clientes:

        mapa_clientes[
            int(cliente["id"])
        ] = cliente["nome"]


    servicos_por_id = {}


    for servico in servicos:

        id_servico = int(
            servico["id"]
        )

        id_cliente = int(
            servico["id_cliente"]
        )

        nome_cliente = mapa_clientes.get(

            id_cliente,

            "Cliente não encontrado"

        )

        descricao_servico = (

            servico["descricao"]

            or "Sem descrição"

        )

        servicos_por_id[id_servico] = {

            "id_cliente": id_cliente,

            "nome_cliente": nome_cliente,

            "descricao": descricao_servico,

        }


    titulo = ft.Text(

        "Contratos / Notas Fiscais",

        size=28,

        weight=ft.FontWeight.BOLD,

        color=BRANCO,

    )


    subtitulo = ft.Text(

        "Central de documentos dos clientes e serviços",

        size=14,

        color=CINZA,

    )


    def opcao_tipo(texto):

        return ft.DropdownOption(

            key=texto,

            text=texto,

            style=ft.ButtonStyle(

                color=BRANCO,

            ),

        )


    servico_dropdown = ft.Dropdown(

        label="Serviço",

        hint_text="Selecione o serviço",

        options=[],

        width=320,

        menu_width=420,

        color=BRANCO,

        label_style=ft.TextStyle(

            color=CINZA

        ),

        border_color=ft.Colors.GREY_500,

        focused_border_color=LARANJA,

        menu_style=ft.MenuStyle(

            bgcolor=ft.Colors.GREY_900

        ),

    )


    for id_servico, dados in (

        servicos_por_id.items()

    ):

        servico_dropdown.options.append(

            ft.DropdownOption(

                key=str(id_servico),

                text=(

                    f"Serviço #{id_servico} - "

                    f"{dados['descricao']} - "

                    f"{dados['nome_cliente']}"

                ),

                style=ft.ButtonStyle(

                    color=BRANCO,

                ),

            )

        )


    cliente_info = ft.Text(

        "Cliente: selecione um serviço",

        color=CINZA,

        size=14,

    )


    tipo_dropdown = ft.Dropdown(

        label="Tipo de documento",

        hint_text="Selecione",

        width=320,

        color=BRANCO,

        label_style=ft.TextStyle(

            color=CINZA

        ),

        border_color=ft.Colors.GREY_500,

        focused_border_color=LARANJA,

        menu_style=ft.MenuStyle(

            bgcolor=ft.Colors.GREY_900

        ),

        options=[

            opcao_tipo("Orçamento"),

            opcao_tipo("Contrato"),

            opcao_tipo("Recibo"),

            opcao_tipo("Nota fiscal"),

            opcao_tipo("Nota de compra"),

            opcao_tipo("Comprovante"),

            opcao_tipo("Outro"),

        ],

    )


    descricao = ft.TextField(

        label="Descrição",

        hint_text="Ex.: Contrato assinado da cozinha",

        width=320,

        color=BRANCO,

        label_style=ft.TextStyle(

            color=CINZA

        ),

        border_color=ft.Colors.GREY_500,

        focused_border_color=LARANJA,

    )


    data_documento = ft.TextField(

        label="Data do documento",

        value=datetime.now().strftime(

            "%Y-%m-%d"

        ),

        width=320,

        color=BRANCO,

        label_style=ft.TextStyle(

            color=CINZA

        ),

        border_color=ft.Colors.GREY_500,

        focused_border_color=LARANJA,

    )


    arquivo_selecionado = ft.Text(

        "Nenhum PDF selecionado",

        color=CINZA,

        size=13,

    )


    arquivos_selecionados = []


    file_picker = ft.FilePicker()


    page.services.append(

        file_picker

    )


    async def selecionar_pdf(e):

        try:

            arquivos = await file_picker.pick_files(

                allow_multiple=True,

                allowed_extensions=[

                    "pdf"

                ],

            )


            arquivos_selecionados.clear()


            if not arquivos:

                arquivo_selecionado.value = (

                    "Nenhum PDF selecionado"

                )

                arquivo_selecionado.color = CINZA

                page.update()

                return


            for arquivo in arquivos:

                if arquivo.path:

                    arquivos_selecionados.append(

                        arquivo

                    )


            if not arquivos_selecionados:

                arquivo_selecionado.value = (

                    "Nenhum PDF selecionado"

                )

                arquivo_selecionado.color = (

                    ft.Colors.RED_300

                )

            else:

                nomes = [

                    os.path.basename(

                        arquivo.path

                    )

                    for arquivo in arquivos_selecionados

                ]


                arquivo_selecionado.value = (

                    f"{len(nomes)} PDF(s) selecionado(s): "

                    + ", ".join(nomes)

                )

                arquivo_selecionado.color = VERDE


            page.update()


        except Exception as erro:

            arquivo_selecionado.value = (

                f"Erro ao selecionar PDF: {erro}"

            )

            arquivo_selecionado.color = (

                ft.Colors.RED_300

            )

            page.update()


    def atualizar_cliente():

        if not servico_dropdown.value:

            cliente_info.value = (

                "Cliente: selecione um serviço"

            )

            cliente_info.color = CINZA

            return


        try:

            id_servico = int(

                servico_dropdown.value

            )

        except ValueError:

            cliente_info.value = (

                "Cliente: não encontrado"

            )

            cliente_info.color = (

                ft.Colors.RED_300

            )

            return


        dados = servicos_por_id.get(

            id_servico

        )


        if dados:

            cliente_info.value = (

                f"Cliente: "

                f"{dados['nome_cliente']}"

            )

            cliente_info.color = BRANCO

        else:

            cliente_info.value = (

                "Cliente: não encontrado"

            )

            cliente_info.color = (

                ft.Colors.RED_300

            )


    def servico_alterado(e):

        atualizar_cliente()

        page.update()


    servico_dropdown.on_change = (

        servico_alterado

    )


    mensagem = ft.Text(

        "",

        size=14,

        color=BRANCO,

    )


    lista_documentos = ft.Column(

        controls=[],

        spacing=0,

        tight=True,

    )


    def abrir_documento(

        caminho

    ):

        if not caminho:

            return


        if not os.path.exists(

            caminho

        ):

            dialogo = ft.AlertDialog(

                title=ft.Text(

                    "Arquivo não encontrado"

                ),

                content=ft.Text(

                    "O PDF não foi encontrado "

                    "no local armazenado."

                ),

                actions=[

                    ft.Button(

                        "Fechar",

                        on_click=lambda e:

                            page.pop_dialog(),

                    )

                ],

            )


            page.show_dialog(

                dialogo

            )

            return


        webbrowser.open(

            os.path.abspath(

                caminho

            )

        )


    def abrir_edicao(

        id_documento

    ):

        documento = obter_documento(

            id_documento

        )


        if documento is None:

            return


        servico_edit = ft.Dropdown(

            label="Serviço",

            hint_text="Selecione o serviço",

            options=[],

            width=320,

            menu_width=420,

            color=BRANCO,

            border_color=ft.Colors.GREY_500,

            focused_border_color=LARANJA,

            menu_style=ft.MenuStyle(

                bgcolor=ft.Colors.GREY_900

            ),

        )


        cliente_edit_info = ft.Text(

            "Cliente: selecione um serviço",

            color=CINZA,

            size=14,

        )


        for id_servico, dados in (

            servicos_por_id.items()

        ):

            servico_edit.options.append(

                ft.DropdownOption(

                    key=str(

                        id_servico

                    ),

                    text=(

                        f"Serviço #{id_servico} - "

                        f"{dados['descricao']} - "

                        f"{dados['nome_cliente']}"

                    ),

                    style=ft.ButtonStyle(

                        color=BRANCO,

                    ),

                )

            )


        tipo_edit = ft.Dropdown(

            label="Tipo de documento",

            width=320,

            color=BRANCO,

            options=[

                opcao_tipo("Orçamento"),

                opcao_tipo("Contrato"),

                opcao_tipo("Recibo"),

                opcao_tipo("Nota fiscal"),

                opcao_tipo("Nota de compra"),

                opcao_tipo("Comprovante"),

                opcao_tipo("Outro"),

            ],

        )


        descricao_edit = ft.TextField(

            label="Descrição",

            value=(

                documento["descricao"]

                or ""

            ),

            width=320,

            color=BRANCO,

            border_color=ft.Colors.GREY_500,

            focused_border_color=LARANJA,

        )


        data_edit = ft.TextField(

            label="Data do documento",

            value=(

                documento[

                    "data_documento"

                ]

                or ""

            ),

            width=320,

            color=BRANCO,

            border_color=ft.Colors.GREY_500,

            focused_border_color=LARANJA,

        )


        if documento["id_servico"]:

            servico_edit.value = str(

                documento[

                    "id_servico"

                ]

            )


        tipo_edit.value = (

            documento["tipo"]

        )


        def atualizar_cliente_edicao():

            if not servico_edit.value:

                cliente_edit_info.value = (

                    "Cliente: selecione um serviço"

                )

                cliente_edit_info.color = CINZA

                return


            try:

                id_servico = int(

                    servico_edit.value

                )

            except ValueError:

                return


            dados = servicos_por_id.get(

                id_servico

            )


            if dados:

                cliente_edit_info.value = (

                    f"Cliente: "

                    f"{dados['nome_cliente']}"

                )

                cliente_edit_info.color = BRANCO

            else:

                cliente_edit_info.value = (

                    "Cliente: não encontrado"

                )

                cliente_edit_info.color = (

                    ft.Colors.RED_300

                )


        atualizar_cliente_edicao()


        def servico_edit_alterado(e):

            atualizar_cliente_edicao()

            page.update()


        servico_edit.on_change = (

            servico_edit_alterado

        )


        def salvar_edicao(e):

            if not servico_edit.value:

                mensagem.value = (

                    "Selecione um serviço."

                )

                mensagem.color = (

                    ft.Colors.RED_300

                )

                page.update()

                return


            if not tipo_edit.value:

                mensagem.value = (

                    "Selecione o tipo do documento."

                )

                mensagem.color = (

                    ft.Colors.RED_300

                )

                page.update()

                return


            try:

                id_servico = int(

                    servico_edit.value

                )

                dados = servicos_por_id.get(

                    id_servico

                )

                if not dados:

                    raise ValueError(

                        "Serviço não encontrado."

                    )

                id_cliente = (

                    dados["id_cliente"]

                )

                editar_documento(

                    id_documento,

                    id_cliente,

                    id_servico,

                    tipo_edit.value,

                    descricao_edit.value,

                    documento[

                        "nome_arquivo"

                    ] or "",

                    documento[

                        "caminho_arquivo"

                    ] or "",

                    data_edit.value,

                )

                page.pop_dialog()

                mensagem.value = (

                    "Documento alterado "

                    "com sucesso."

                )

                mensagem.color = VERDE

                carregar_documentos()

                page.update()

            except Exception as erro:

                mensagem.value = (

                    "Erro ao editar documento: "

                    f"{erro}"

                )

                mensagem.color = (

                    ft.Colors.RED_300

                )

                page.update()


        dialogo = ft.AlertDialog(

            title=ft.Text(

                "Editar documento",

                color=BRANCO,

            ),

            content=ft.Column(

                controls=[

                    servico_edit,

                    cliente_edit_info,

                    tipo_edit,

                    descricao_edit,

                    data_edit,

                ],

                tight=True,

                scroll=ft.ScrollMode.AUTO,

            ),

            actions=[

                ft.Button(

                    "Cancelar",

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


        page.show_dialog(

            dialogo

        )
        def adicionar_documento_servico(

        id_servico

    ):

            dados = servicos_por_id.get(

            int(id_servico)

        )


        if not dados:

            return


        servico_dropdown.value = str(

            id_servico

        )


        cliente_info.value = (

            f"Cliente: "

            f"{dados['nome_cliente']}"

        )


        cliente_info.color = BRANCO


        mensagem.value = (

            "Serviço selecionado. "

            "Escolha o PDF e cadastre."

        )


        mensagem.color = CINZA


        page.update()


    def remover_documento_confirmacao(

        id_documento

    ):

        documento = obter_documento(

            id_documento

        )


        if documento is None:

            mensagem.value = (

                "Documento não encontrado."

            )

            mensagem.color = (

                ft.Colors.RED_300

            )

            page.update()

            return


        nome_arquivo = (

            documento["nome_arquivo"]

            or "este documento"

        )


        def cancelar(e):

            page.pop_dialog()


        def confirmar(e):

            try:

                caminho = remover_documento(

                    id_documento

                )


                if caminho and os.path.exists(

                    caminho

                ):

                    os.remove(

                        caminho

                    )


                page.pop_dialog()


                mensagem.value = (

                    "Documento removido "

                    "com sucesso."

                )


                mensagem.color = VERDE


                carregar_documentos()


                page.update()


            except Exception as erro:

                page.pop_dialog()


                mensagem.value = (

                    "Erro ao remover documento: "

                    f"{erro}"

                )


                mensagem.color = (

                    ft.Colors.RED_300

                )


                page.update()


        dialogo = ft.AlertDialog(

            title=ft.Text(

                "Remover documento?",

                color=BRANCO,

            ),

            content=ft.Text(

                f"Tem certeza que deseja remover:\n\n"

                f"{nome_arquivo}\n\n"

                f"Essa ação não poderá ser desfeita.",

                color=BRANCO,

            ),

            actions=[

                ft.Button(

                    "Cancelar",

                    icon=ft.Icons.CLOSE,

                    on_click=cancelar,

                ),

                ft.Button(

                    "Remover",

                    icon=ft.Icons.DELETE,

                    bgcolor=VERMELHO,

                    color=BRANCO,

                    on_click=confirmar,

                ),

            ],

        )


        page.show_dialog(

            dialogo

        )


    def criar_linha_pdf(

        documento

    ):

        nome_arquivo = (

            documento[

                "nome_arquivo"

            ]

            or "Documento PDF"

        )


        tipo = (

            documento[

                "tipo"

            ]

            or "Documento"

        )


        descricao_pdf = (

            documento[

                "descricao"

            ]

            or "Sem descrição"

        )


        data_pdf = (

            documento[

                "data_documento"

            ]

            or ""

        )


        informacoes = ft.Column(

            controls=[

                ft.Text(

                    nome_arquivo,

                    size=14,

                    color=BRANCO,

                    weight=(

                        ft.FontWeight.BOLD

                    ),

                ),

                ft.Text(

                    tipo,

                    size=12,

                    color=LARANJA,

                ),

                ft.Text(

                    descricao_pdf,

                    size=12,

                    color=CINZA,

                ),

                ft.Text(

                    f"Data: {data_pdf}",

                    size=11,

                    color=CINZA,

                ),

            ],

            spacing=2,

            tight=True,

        )


        botao_abrir = ft.Button(

            "Abrir",

            icon=ft.Icons.PICTURE_AS_PDF,

            on_click=(

                lambda e,

                caminho=documento[

                    "caminho_arquivo"

                ]:

                    abrir_documento(

                        caminho

                    )

            ),

        )


        botao_editar = ft.Button(

            "Editar",

            icon=ft.Icons.EDIT,

            on_click=(

                lambda e,

                id_doc=int(

                    documento["id"]

                ):

                    abrir_edicao(

                        id_doc

                    )

            ),

        )


        botao_remover = ft.Button(

            "Remover",

            icon=ft.Icons.DELETE,

            bgcolor=VERMELHO,

            color=BRANCO,

            on_click=(

                lambda e,

                id_doc=int(

                    documento["id"]

                ):

                    remover_documento_confirmacao(

                        id_doc

                    )

            ),

        )


        return ft.Container(

            bgcolor=ft.Colors.GREY_900,

            border_radius=8,

            padding=10,

            content=ft.Column(

                controls=[

                    ft.Row(

                        controls=[

                            ft.Icon(

                                ft.Icons.PICTURE_AS_PDF,

                                color=LARANJA,

                                size=28,

                            ),

                            informacoes,

                        ],

                        spacing=10,

                    ),

                    ft.Row(

                        controls=[

                            botao_abrir,

                            botao_editar,

                            botao_remover,

                        ],

                        spacing=8,

                        wrap=True,

                    ),

                ],

                spacing=8,

                tight=True,

            ),

        )


    def carregar_documentos():

        lista_documentos.controls.clear()


        documentos = listar_documentos()


        documentos_por_servico = {}


        for documento in documentos:

            id_servico = (

                documento["id_servico"]

            )


            if id_servico:

                id_servico = int(

                    id_servico

                )


                if id_servico not in (

                    documentos_por_servico

                ):

                    documentos_por_servico[

                        id_servico

                    ] = []


                documentos_por_servico[

                    id_servico

                ].append(

                    documento

                )


        for id_servico, dados in (

            servicos_por_id.items()

        ):

            documentos_do_servico = (

                documentos_por_servico.get(

                    id_servico,

                    []

                )

            )


            cabecalho_servico = ft.Row(

                controls=[

                    ft.Column(

                        controls=[

                            ft.Text(

                                f"Serviço #{id_servico}",

                                size=12,

                                color=CINZA,

                                weight=(

                                    ft.FontWeight.BOLD

                                ),

                            ),

                            ft.Text(

                                dados[

                                    "nome_cliente"

                                ],

                                size=20,

                                color=BRANCO,

                                weight=(

                                    ft.FontWeight.BOLD

                                ),

                            ),

                            ft.Text(

                                dados[

                                    "descricao"

                                ],

                                size=14,

                                color=CINZA,

                            ),

                        ],

                        spacing=4,

                        tight=True,

                    ),

                ],

                spacing=10,

                wrap=True,

                vertical_alignment=(

                    ft.CrossAxisAlignment.CENTER

                ),

            )


            documentos_coluna = ft.Column(

                controls=[],

                spacing=8,

                tight=True,

            )
            if not documentos_do_servico:

                documentos_coluna.controls.append(

                    ft.Container(

                        padding=10,

                        content=ft.Row(

                            controls=[

                                ft.Icon(

                                    ft.Icons.FOLDER_OPEN,

                                    color=CINZA,

                                    size=22,

                                ),

                                ft.Text(

                                    "Nenhum documento "

                                    "cadastrado para "

                                    "este serviço.",

                                    color=CINZA,

                                    size=13,

                                ),

                            ],

                            spacing=8,

                        ),

                    )

                )


            else:

                for documento in (

                    documentos_do_servico

                ):

                    documentos_coluna.controls.append(

                        criar_linha_pdf(

                            documento

                        )

                    )


            card_servico = ft.Container(

                bgcolor=CARD,

                border_radius=12,

                padding=20,

                margin=ft.Margin.only(

                    bottom=12

                ),

                content=ft.Column(

                    controls=[

                        cabecalho_servico,

                        ft.Divider(

                            color=(

                                ft.Colors.GREY_800

                            ),

                            height=10,

                        ),

                        documentos_coluna,

                    ],

                    spacing=12,

                    tight=True,

                ),

            )


            lista_documentos.controls.append(

                card_servico

            )


        if not servicos_por_id:

            lista_documentos.controls.append(

                ft.Container(

                    bgcolor=CARD,

                    border_radius=12,

                    padding=30,

                    content=ft.Column(

                        controls=[

                            ft.Text(

                                "Nenhum serviço cadastrado",

                                size=18,

                                color=BRANCO,

                                weight=(

                                    ft.FontWeight.BOLD

                                ),

                            ),

                            ft.Text(

                                "Cadastre um serviço "

                                "para poder vincular "

                                "documentos.",

                                size=14,

                                color=CINZA,

                            ),

                        ],

                        spacing=10,

                        tight=True,

                    ),

                )

            )


        page.update()


    def salvar_documento(e):

        mensagem.value = ""

        mensagem.color = BRANCO


        if not servico_dropdown.value:

            mensagem.value = "Selecione um serviço."

            mensagem.color = ft.Colors.RED_300

            page.update()

            return


        if not tipo_dropdown.value:

            mensagem.value = (

                "Selecione o tipo do documento."

            )

            mensagem.color = ft.Colors.RED_300

            page.update()

            return


        if not arquivos_selecionados:

            mensagem.value = (

                "Selecione pelo menos um arquivo PDF."

            )

            mensagem.color = ft.Colors.RED_300

            page.update()

            return


        try:

            id_servico = int(

                servico_dropdown.value

            )


            dados = servicos_por_id.get(

                id_servico

            )


            if not dados:

                raise ValueError(

                    "Serviço não encontrado."

                )


            id_cliente = dados["id_cliente"]

            quantidade_salva = 0


            for indice, arquivo in enumerate(

                arquivos_selecionados,

                start=1

            ):

                caminho_original = arquivo.path


                if not caminho_original:

                    continue


                nome_original = os.path.basename(

                    caminho_original

                )


                nome_final = (

                    f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_"

                    f"{indice}_"

                    f"{nome_original}"

                )


                caminho_final = os.path.join(

                    PASTA_DOCUMENTOS,

                    nome_final

                )


                shutil.copy2(

                    caminho_original,

                    caminho_final

                )


                cadastrar_documento(

                    id_cliente=id_cliente,

                    id_servico=id_servico,

                    tipo=tipo_dropdown.value,

                    descricao=descricao.value or "",

                    nome_arquivo=nome_original,

                    caminho_arquivo=caminho_final,

                    data_documento=data_documento.value,

                )


                quantidade_salva += 1


            if quantidade_salva == 0:

                raise ValueError(

                    "Não foi possível acessar o PDF selecionado."

                )


            tipo_dropdown.value = None

            descricao.value = ""

            data_documento.value = (

                datetime.now().strftime(

                    "%Y-%m-%d"

                )

            )


            arquivos_selecionados.clear()


            arquivo_selecionado.value = (

                "Nenhum PDF selecionado"

            )


            arquivo_selecionado.color = CINZA


            mensagem.value = (

                f"{quantidade_salva} documento(s) "

                "cadastrado(s) com sucesso."

            )


            mensagem.color = VERDE


            carregar_documentos()

            page.update()


        except Exception as erro:

            mensagem.value = (

                "Erro ao cadastrar documento: "

                f"{erro}"

            )

            mensagem.color = ft.Colors.RED_300

            page.update()


    botao_pdf = ft.Button(

        "Selecionar PDF",

        icon=ft.Icons.UPLOAD_FILE,

        on_click=selecionar_pdf,

    )


    botao_salvar = ft.Button(

        "Cadastrar documento(s)",

        icon=ft.Icons.SAVE,

        bgcolor=LARANJA,

        color=BRANCO,

        on_click=salvar_documento,

    )


    formulario = ft.Container(

        bgcolor=CARD,

        border_radius=12,

        padding=20,

        content=ft.Column(

            controls=[

                ft.Text(

                    "Cadastrar documento",

                    size=20,

                    weight=(

                        ft.FontWeight.BOLD

                    ),

                    color=BRANCO,

                ),

                ft.Text(

                    "Vincule o documento a um serviço. "

                    "O cliente será identificado automaticamente.",

                    size=13,

                    color=CINZA,

                ),

                ft.Divider(

                    color=(

                        ft.Colors.GREY_800

                    )

                ),

                ft.ResponsiveRow(

                    controls=[

                        ft.Container(

                            content=(

                                servico_dropdown

                            ),

                            col={

                                "sm": 12,

                                "md": 6,

                            },

                        ),

                        ft.Container(

                            content=(

                                cliente_info

                            ),

                            padding=5,

                            col={

                                "sm": 12,

                                "md": 6,

                            },

                        ),

                        ft.Container(

                            content=(

                                tipo_dropdown

                            ),

                            col={

                                "sm": 12,

                                "md": 6,

                            },

                        ),

                        ft.Container(

                            content=(

                                descricao

                            ),

                            col={

                                "sm": 12,

                                "md": 6,

                            },

                        ),

                        ft.Container(

                            content=(

                                data_documento

                            ),

                            col={

                                "sm": 12,

                                "md": 6,

                            },

                        ),

                    ],

                    spacing=15,

                    run_spacing=15,

                ),

                ft.Divider(

                    color=(

                        ft.Colors.GREY_800

                    )

                ),

                ft.Row(

                    controls=[

                        botao_pdf,

                        arquivo_selecionado,

                    ],

                    wrap=True,

                    spacing=10,

                    vertical_alignment=(

                        ft.CrossAxisAlignment.CENTER

                    ),

                ),

                mensagem,

                ft.Row(

                    controls=[

                        botao_salvar

                    ]

                ),

            ],

            spacing=15,

            tight=True,

        ),

    )


    area_lista = ft.Column(

        controls=[

            ft.Text(

                "Documentos cadastrados",

                size=20,

                weight=(

                    ft.FontWeight.BOLD

                ),

                color=BRANCO,

            ),

            ft.Text(

                "Consulte e edite os documentos "

                "já registrados.",

                size=13,

                color=CINZA,

            ),

            ft.Divider(

                color=(

                    ft.Colors.GREY_800

                )

            ),

            lista_documentos,

        ],

        spacing=10,

        tight=True,

    )


    conteudo = ft.Column(

        controls=[

            titulo,

            subtitulo,

            ft.Container(

                height=20

            ),

            formulario,

            ft.Container(

                height=20

            ),

            area_lista,

        ],

        spacing=0,

        scroll=ft.ScrollMode.AUTO,

    )


    if area_conteudo is not None:

        area_conteudo.content = (

            ft.Container(

                expand=True,

                bgcolor=FUNDO,

                padding=30,

                content=conteudo,

            )

        )

        area_conteudo.update()


    else:

        page.add(

            ft.Container(

                expand=True,

                bgcolor=FUNDO,

                padding=30,

                content=conteudo,

            )

        )


    carregar_documentos()

    page.update()
