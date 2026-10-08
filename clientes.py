import flet as ft
import urllib.request
import json
import re

from database import cadastrar_cliente as salvar_cliente
from database import listar_clientes
from database import editar_cliente
from database import listar_servicos_cliente


def mostrar_clientes(page: ft.Page, area_conteudo=None):

    titulo = ft.Text(
        "Clientes",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    subtitulo = ft.Text(
        "Cadastre e gerencie os clientes da Rafá Mobile.",
        size=14,
        color=ft.Colors.GREY_400,
    )

    nome = ft.TextField(
        label="Nome completo",
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_300
        ),
        text_style=ft.TextStyle(
            color=ft.Colors.WHITE
        ),
        border_color=ft.Colors.GREY_500,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.PERSON,
        expand=True,
    )

    telefone = ft.TextField(
        label="Telefone",
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_300
        ),
        text_style=ft.TextStyle(
            color=ft.Colors.WHITE
        ),
        border_color=ft.Colors.GREY_500,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.PHONE,
        expand=True,
    )

    cpf_cnpj = ft.TextField(
        label="CPF / CNPJ",
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_300
        ),
        text_style=ft.TextStyle(
            color=ft.Colors.WHITE
        ),
        border_color=ft.Colors.GREY_500,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.BADGE,
        expand=True,
    )

    cep = ft.TextField(
        label="CEP",
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_300
        ),
        text_style=ft.TextStyle(
            color=ft.Colors.WHITE
        ),
        border_color=ft.Colors.GREY_500,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.LOCATION_ON,
        expand=True,
    )

    endereco = ft.TextField(
        label="Endereço",
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_300
        ),
        text_style=ft.TextStyle(
            color=ft.Colors.WHITE
        ),
        border_color=ft.Colors.GREY_500,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.HOME,
        expand=True,
    )

    numero = ft.TextField(
        label="Número",
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_300
        ),
        text_style=ft.TextStyle(
            color=ft.Colors.WHITE
        ),
        border_color=ft.Colors.GREY_500,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.NUMBERS,
        width=180,
    )

    bairro = ft.TextField(
        label="Bairro",
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_300
        ),
        text_style=ft.TextStyle(
            color=ft.Colors.WHITE
        ),
        border_color=ft.Colors.GREY_500,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.LOCATION_CITY,
        expand=True,
    )

    cidade = ft.TextField(
        label="Cidade",
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_300
        ),
        text_style=ft.TextStyle(
            color=ft.Colors.WHITE
        ),
        border_color=ft.Colors.GREY_500,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.LOCATION_CITY,
        expand=True,
    )

    estado = ft.TextField(
        label="Estado",
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_300
        ),
        text_style=ft.TextStyle(
            color=ft.Colors.WHITE
        ),
        border_color=ft.Colors.GREY_500,
        focused_border_color=ft.Colors.ORANGE,
        prefix_icon=ft.Icons.MAP,
        width=180,
    )

    mensagem = ft.Text(
        "",
        color=ft.Colors.GREEN_400,
    )

    # ==========================================================
    # CONSULTAR CEP
    # ==========================================================

    def consultar_cep(e):

        cep_digitado = re.sub(
            r"\D",
            "",
            e.control.value
        )

        if len(cep_digitado) != 8:
            return

        try:

            url = (
                f"https://viacep.com.br/ws/"
                f"{cep_digitado}/json/"
            )

            with urllib.request.urlopen(
                url,
                timeout=5
            ) as resposta:

                dados = json.loads(
                    resposta.read().decode("utf-8")
                )

            if dados.get("erro"):

                mensagem.value = "CEP não encontrado."
                mensagem.color = ft.Colors.RED_400

            else:

                endereco.value = dados.get(
                    "logradouro",
                    ""
                )

                bairro.value = dados.get(
                    "bairro",
                    ""
                )

                cidade.value = dados.get(
                    "localidade",
                    ""
                )

                estado.value = dados.get(
                    "uf",
                    ""
                )

                mensagem.value = (
                    "Endereço preenchido automaticamente."
                )

                mensagem.color = ft.Colors.GREEN_400

            page.update()

        except Exception:

            mensagem.value = (
                "Não foi possível consultar o CEP."
            )

            mensagem.color = ft.Colors.RED_400

            page.update()

    cep.on_blur = consultar_cep

    # ==========================================================
    # LISTA DE CLIENTES
    # ==========================================================

    lista_clientes = ft.ListView(
        spacing=8,
        height=300,
    )

    # ==========================================================
    # EDITAR CLIENTE
    # ==========================================================

    def abrir_edicao_cliente(cliente):

        id_cliente = cliente[0]

        campo_nome = ft.TextField(
            label="Nome completo",
            value=cliente[1] or "",
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_500,
            focused_border_color=ft.Colors.ORANGE,
            prefix_icon=ft.Icons.PERSON,
        )

        campo_telefone = ft.TextField(
            label="Telefone",
            value=cliente[2] or "",
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_500,
            focused_border_color=ft.Colors.ORANGE,
            prefix_icon=ft.Icons.PHONE,
        )

        campo_cpf = ft.TextField(
            label="CPF / CNPJ",
            value=cliente[3] or "",
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_500,
            focused_border_color=ft.Colors.ORANGE,
            prefix_icon=ft.Icons.BADGE,
        )

        campo_cep = ft.TextField(
            label="CEP",
            value=cliente[4] or "",
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_500,
            focused_border_color=ft.Colors.ORANGE,
            prefix_icon=ft.Icons.LOCATION_ON,
        )

        campo_endereco = ft.TextField(
            label="Endereço",
            value=cliente[5] or "",
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_500,
            focused_border_color=ft.Colors.ORANGE,
            prefix_icon=ft.Icons.HOME,
        )

        campo_numero = ft.TextField(
            label="Número",
            value=cliente[6] or "",
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_500,
            focused_border_color=ft.Colors.ORANGE,
            prefix_icon=ft.Icons.NUMBERS,
            width=180,
        )

        campo_bairro = ft.TextField(
            label="Bairro",
            value=cliente[7] or "",
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_500,
            focused_border_color=ft.Colors.ORANGE,
            prefix_icon=ft.Icons.LOCATION_CITY,
        )

        campo_cidade = ft.TextField(
            label="Cidade",
            value=cliente[8] or "",
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_500,
            focused_border_color=ft.Colors.ORANGE,
            prefix_icon=ft.Icons.LOCATION_CITY,
        )

        campo_estado = ft.TextField(
            label="Estado",
            value=cliente[9] or "",
            color=ft.Colors.WHITE,
            border_color=ft.Colors.GREY_500,
            focused_border_color=ft.Colors.ORANGE,
            prefix_icon=ft.Icons.MAP,
            width=180,
        )

        mensagem_edicao = ft.Text(
            "",
            color=ft.Colors.GREEN_400,
        )

        def consultar_cep_edicao(e):

            cep_digitado = re.sub(
                r"\D",
                "",
                campo_cep.value
            )

            if len(cep_digitado) != 8:
                return

            try:

                url = (
                    f"https://viacep.com.br/ws/"
                    f"{cep_digitado}/json/"
                )

                with urllib.request.urlopen(
                    url,
                    timeout=5
                ) as resposta:

                    dados = json.loads(
                        resposta.read().decode("utf-8")
                    )

                if dados.get("erro"):

                    mensagem_edicao.value = (
                        "CEP não encontrado."
                    )

                    mensagem_edicao.color = (
                        ft.Colors.RED_400
                    )

                else:

                    campo_endereco.value = dados.get(
                        "logradouro",
                        ""
                    )

                    campo_bairro.value = dados.get(
                        "bairro",
                        ""
                    )

                    campo_cidade.value = dados.get(
                        "localidade",
                        ""
                    )

                    campo_estado.value = dados.get(
                        "uf",
                        ""
                    )

                    mensagem_edicao.value = (
                        "Endereço preenchido automaticamente."
                    )

                    mensagem_edicao.color = (
                        ft.Colors.GREEN_400
                    )

                page.update()

            except Exception:

                mensagem_edicao.value = (
                    "Não foi possível consultar o CEP."
                )

                mensagem_edicao.color = (
                    ft.Colors.RED_400
                )

                page.update()

        campo_cep.on_blur = consultar_cep_edicao

        def salvar_edicao(e):

            if not campo_nome.value.strip():

                mensagem_edicao.value = (
                    "Informe o nome do cliente."
                )

                mensagem_edicao.color = (
                    ft.Colors.RED_400
                )

                page.update()

                return

            try:

                editar_cliente(
                    id_cliente=id_cliente,
                    nome=campo_nome.value,
                    telefone=campo_telefone.value,
                    cpf_cnpj=campo_cpf.value,
                    cep=campo_cep.value,
                    endereco=campo_endereco.value,
                    numero=campo_numero.value,
                    bairro=campo_bairro.value,
                    cidade=campo_cidade.value,
                    estado=campo_estado.value,
                )

                page.pop_dialog()

                mensagem.value = (
                    f"Cliente {campo_nome.value} "
                    "alterado com sucesso!"
                )

                mensagem.color = (
                    ft.Colors.GREEN_400
                )

                atualizar_lista()

                page.update()

            except Exception as erro:

                mensagem_edicao.value = (
                    f"Erro ao alterar cliente: {erro}"
                )

                mensagem_edicao.color = (
                    ft.Colors.RED_400
                )

                page.update()

        dialogo_edicao = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.GREY_900,

            title=ft.Text(
                f"Editar cliente #{id_cliente}",
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
            ),

            content=ft.Container(
                width=700,

                content=ft.Column(
                    [
                        ft.Row(
                            [
                                campo_nome,
                                campo_telefone,
                            ],
                            spacing=15,
                        ),

                        ft.Row(
                            [
                                campo_cpf,
                                campo_cep,
                            ],
                            spacing=15,
                        ),

                        ft.Row(
                            [
                                campo_endereco,
                                campo_numero,
                            ],
                            spacing=15,
                        ),

                        ft.Row(
                            [
                                campo_bairro,
                                campo_cidade,
                            ],
                            spacing=15,
                        ),

                        ft.Row(
                            [
                                campo_estado,
                            ],
                            spacing=15,
                        ),

                        mensagem_edicao,

                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),

            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: page.pop_dialog(),
                ),

                ft.Button(
                    "Salvar alterações",
                    icon=ft.Icons.SAVE,
                    on_click=salvar_edicao,
                ),
            ],
        )

        page.show_dialog(dialogo_edicao)

    # ==========================================================
    # DETALHES DO CLIENTE
    # ==========================================================

    def mostrar_detalhes(cliente):

        id_cliente = cliente[0]
        nome_cliente = cliente[1]
        telefone_cliente = cliente[2] or "Não informado"
        cpf_cliente = cliente[3] or "Não informado"
        cep_cliente = cliente[4] or "Não informado"
        endereco_cliente = cliente[5] or "Não informado"
        numero_cliente = cliente[6] or "Não informado"
        bairro_cliente = cliente[7] or "Não informado"
        cidade_cliente = cliente[8] or "Não informado"
        estado_cliente = cliente[9] or "Não informado"
        data_cliente = cliente[10] or "Não informado"

        if data_cliente != "Não informado":

            partes = data_cliente.split("-")

            if len(partes) == 3:

                data_cliente = (
                    f"{partes[2]}/"
                    f"{partes[1]}/"
                    f"{partes[0]}"
                )

        # ==========================================================
        # HISTÓRICO DE SERVIÇOS
        # ==========================================================

        servicos_cliente = listar_servicos_cliente(
            id_cliente
        )

        historico = ft.Column(
            controls=[],
            spacing=10,
        )

        if not servicos_cliente:

            historico.controls.append(
                ft.Container(
                    bgcolor=ft.Colors.GREY_800,
                    padding=15,
                    border_radius=8,
                    content=ft.Text(
                        "Nenhum serviço registrado "
                        "para este cliente.",
                        color=ft.Colors.GREY_400,
                    ),
                )
            )

        else:

            for servico in servicos_cliente:

                id_servico = servico[0]
                descricao_servico = servico[2]
                valor_total = servico[3]
                entrada_servico = servico[4]
                data_servico = servico[5]

                valor_total_formatado = (
                    f"R$ {valor_total:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

                entrada_formatada = (
                    f"R$ {entrada_servico:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

                historico.controls.append(
                    ft.Container(
                        bgcolor=ft.Colors.GREY_800,
                        padding=15,
                        border_radius=8,

                        content=ft.Column(
                            [
                                ft.Text(
                                    f"Serviço #{id_servico}",
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),

                                ft.Text(
                                    f"Descrição: "
                                    f"{descricao_servico}",
                                    color=ft.Colors.GREY_300,
                                ),

                                ft.Text(
                                    f"Valor total: "
                                    f"{valor_total_formatado}",
                                    color=ft.Colors.GREY_300,
                                ),

                                ft.Text(
                                    f"Entrada: "
                                    f"{entrada_formatada}",
                                    color=ft.Colors.GREY_300,
                                ),

                                ft.Text(
                                    f"Data: {data_servico}",
                                    color=ft.Colors.GREY_500,
                                    size=12,
                                ),
                            ],
                            spacing=5,
                        ),
                    )
                )

        dialogo = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.GREY_900,

            title=ft.Text(
                nome_cliente,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
            ),

            content=ft.Container(
                width=650,

                content=ft.Column(
                    [
                        ft.Text(
                            f"ID do cliente: {id_cliente}",
                            color=ft.Colors.ORANGE,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Divider(),

                        ft.Text(
                            "DADOS PESSOAIS",
                            size=16,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            f"Nome: {nome_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Text(
                            f"CPF / CNPJ: {cpf_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Text(
                            f"Telefone: {telefone_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Divider(),

                        ft.Text(
                            "ENDEREÇO",
                            size=16,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Text(
                            f"CEP: {cep_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Text(
                            f"Endereço: {endereco_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Text(
                            f"Número: {numero_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Text(
                            f"Bairro: {bairro_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Text(
                            f"Cidade: {cidade_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Text(
                            f"Estado: {estado_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Text(
                            f"Data de cadastro: {data_cliente}",
                            color=ft.Colors.GREY_300,
                        ),

                        ft.Divider(),

                        ft.Text(
                            "HISTÓRICO DO CLIENTE",
                            size=16,
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                        ),

                        historico,

                    ],
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),

            actions=[
                ft.TextButton(
                    "Fechar",
                    on_click=lambda e: page.pop_dialog(),
                ),

                ft.Button(
                    "Editar cliente",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e: (
                        page.pop_dialog(),
                        abrir_edicao_cliente(cliente)
                    ),
                ),
            ],
        )

        page.show_dialog(dialogo)

    # ==========================================================
    # ATUALIZAR LISTA
    # ==========================================================

    def atualizar_lista():

        lista_clientes.controls.clear()

        clientes = listar_clientes()

        if not clientes:

            lista_clientes.controls.append(
                ft.Text(
                    "Nenhum cliente cadastrado ainda.",
                    color=ft.Colors.GREY_500,
                )
            )

        else:

            lista_clientes.controls.append(
                ft.Container(
                    bgcolor=ft.Colors.GREY_800,
                    padding=12,
                    border_radius=8,

                    content=ft.Row(
                        [
                            ft.Text(
                                "ID",
                                width=50,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),

                            ft.Text(
                                "Nome",
                                expand=True,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),

                            ft.Text(
                                "Telefone",
                                width=150,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),

                            ft.Text(
                                "Cidade",
                                width=150,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),

                            ft.Text(
                                "Cadastro",
                                width=110,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),

                            ft.Text(
                                "Ação",
                                width=120,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                        spacing=10,
                    ),
                )
            )

            for cliente in clientes:

                id_cliente = cliente[0]
                nome_cliente = cliente[1]
                telefone_cliente = cliente[2] or ""
                cidade_cliente = cliente[8] or ""
                data_cadastro = cliente[10] or ""

                if data_cadastro:

                    partes = data_cadastro.split("-")

                    if len(partes) == 3:

                        data_cadastro = (
                            f"{partes[2]}/"
                            f"{partes[1]}/"
                            f"{partes[0]}"
                        )

                cliente_linha = ft.Container(
                    bgcolor=ft.Colors.GREY_900,
                    padding=12,
                    border_radius=8,

                    content=ft.Row(
                        [
                            ft.Text(
                                str(id_cliente),
                                width=50,
                                color=ft.Colors.WHITE,
                            ),

                            ft.Text(
                                nome_cliente,
                                expand=True,
                                color=ft.Colors.WHITE,
                            ),

                            ft.Text(
                                telefone_cliente,
                                width=150,
                                color=ft.Colors.GREY_300,
                            ),

                            ft.Text(
                                cidade_cliente,
                                width=150,
                                color=ft.Colors.GREY_300,
                            ),

                            ft.Text(
                                data_cadastro,
                                width=110,
                                color=ft.Colors.GREY_300,
                            ),

                            ft.Button(
                                "Editar",
                                icon=ft.Icons.EDIT,
                                on_click=lambda e, c=cliente:
                                    abrir_edicao_cliente(c),
                            ),
                        ],
                        spacing=10,
                    ),

                    on_click=lambda e, c=cliente:
                        mostrar_detalhes(c),
                )

                lista_clientes.controls.append(
                    cliente_linha
                )

        page.update()

    # ==========================================================
    # CADASTRAR CLIENTE
    # ==========================================================

    def cadastrar_cliente(e):

        if not nome.value.strip():

            mensagem.value = (
                "Informe o nome do cliente."
            )

            mensagem.color = (
                ft.Colors.RED_400
            )

            page.update()

            return

        try:

            salvar_cliente(
                nome=nome.value.strip(),
                telefone=telefone.value.strip(),
                cpf_cnpj=cpf_cnpj.value.strip(),
                cep=cep.value.strip(),
                endereco=endereco.value.strip(),
                numero=numero.value.strip(),
                bairro=bairro.value.strip(),
                cidade=cidade.value.strip(),
                estado=estado.value.strip(),
            )

            mensagem.value = (
                f"Cliente {nome.value} "
                "cadastrado com sucesso!"
            )

            mensagem.color = (
                ft.Colors.GREEN_400
            )

            nome.value = ""
            telefone.value = ""
            cpf_cnpj.value = ""
            cep.value = ""
            endereco.value = ""
            numero.value = ""
            bairro.value = ""
            cidade.value = ""
            estado.value = ""

            atualizar_lista()

        except Exception as erro:

            mensagem.value = (
                f"Erro ao cadastrar cliente: {erro}"
            )

            mensagem.color = (
                ft.Colors.RED_400
            )

            page.update()

    # ==========================================================
    # BOTÃO CADASTRAR
    # ==========================================================

    botao_cadastrar = ft.Button(
        "Cadastrar cliente",
        icon=ft.Icons.PERSON_ADD,
        on_click=cadastrar_cliente,
    )

    # ==========================================================
    # FORMULÁRIO
    # ==========================================================

    formulario = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Novo cliente",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),

                ft.Row(
                    [
                        nome,
                        telefone,
                    ],
                    spacing=15,
                ),

                ft.Row(
                    [
                        cpf_cnpj,
                        cep,
                    ],
                    spacing=15,
                ),

                ft.Row(
                    [
                        endereco,
                        numero,
                    ],
                    spacing=15,
                ),

                ft.Row(
                    [
                        bairro,
                        cidade,
                    ],
                    spacing=15,
                ),

                ft.Row(
                    [
                        estado,
                    ],
                    spacing=15,
                ),

                botao_cadastrar,

                mensagem,
            ],
            spacing=15,
        ),

        bgcolor=ft.Colors.GREY_900,
        padding=25,
        border_radius=12,
    )

    # ==========================================================
    # LISTA
    # ==========================================================

    lista = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Clientes cadastrados",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),

                ft.Text(
                    "Clique em um cliente para visualizar "
                    "o cadastro completo e o histórico.",
                    size=12,
                    color=ft.Colors.GREY_500,
                ),

                lista_clientes,
            ],
            spacing=15,
        ),

        bgcolor=ft.Colors.GREY_900,
        padding=25,
        border_radius=12,
    )

    # ==========================================================
    # CONTEÚDO PRINCIPAL
    # ==========================================================

    conteudo = ft.Column(
        [
            titulo,
            subtitulo,
            formulario,
            lista,
        ],
        spacing=20,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    # ==========================================================
    # COLOCA TUDO NA PÁGINA
    # ==========================================================

    if area_conteudo is not None:

        area_conteudo.content = conteudo

        atualizar_lista()

        page.update()

    else:

        page.add(conteudo)

        atualizar_lista()

        page.update()