import sqlite3



from datetime import datetime





# =====================================

# CONEXÃO COM O BANCO

# =====================================





def conectar():



    conexao = sqlite3.connect("rafa_mobile.db")



    conexao.row_factory = sqlite3.Row



    conexao.execute("PRAGMA foreign_keys = ON")



    return conexao





# =====================================

# CRIAR BANCO E TABELAS

# =====================================





def criar_banco():



    with conectar() as conn:



        conn.execute("""

            CREATE TABLE IF NOT EXISTS clientes (



                id INTEGER PRIMARY KEY AUTOINCREMENT,



                nome TEXT NOT NULL,



                telefone TEXT,



                cpf_cnpj TEXT,



                cep TEXT,



                endereco TEXT,



                numero TEXT,



                bairro TEXT,



                cidade TEXT,



                estado TEXT,



                data_cadastro TEXT NOT NULL



            )

        """)



    criar_tabela_servicos()



    criar_tabela_movimentacoes_servico()



    criar_tabela_caixa()



    criar_tabela_pagamentos()



    criar_tabela_documentos()





# =====================================

# CLIENTES

# =====================================





def cadastrar_cliente(

    nome,

    telefone,

    cpf_cnpj,

    cep,

    endereco,

    numero,

    bairro,

    cidade,

    estado

):



    data_cadastro = datetime.now().strftime("%Y-%m-%d")



    with conectar() as conn:



        cursor = conn.execute("""

            INSERT INTO clientes (



                nome,

                telefone,

                cpf_cnpj,

                cep,

                endereco,

                numero,

                bairro,

                cidade,

                estado,

                data_cadastro



            )



            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (



            nome.strip(),

            telefone.strip(),

            cpf_cnpj.strip(),

            cep.strip(),

            endereco.strip(),

            numero.strip(),

            bairro.strip(),

            cidade.strip(),

            estado.strip(),

            data_cadastro



        ))



        return cursor.lastrowid





def listar_clientes():



    with conectar() as conn:



        return conn.execute("""

            SELECT



                id,

                nome,

                telefone,

                cpf_cnpj,

                cep,

                endereco,

                numero,

                bairro,

                cidade,

                estado,

                data_cadastro



            FROM clientes



            ORDER BY id DESC

        """).fetchall()





def editar_cliente(

    id_cliente,

    nome,

    telefone,

    cpf_cnpj,

    cep,

    endereco,

    numero,

    bairro,

    cidade,

    estado

):



    with conectar() as conn:



        cliente = conn.execute("""

            SELECT id



            FROM clientes



            WHERE id = ?

        """, (id_cliente,)).fetchone()



        if cliente is None:



            raise ValueError("Cliente não encontrado.")



        conn.execute("""

            UPDATE clientes



            SET



                nome = ?,

                telefone = ?,

                cpf_cnpj = ?,

                cep = ?,

                endereco = ?,

                numero = ?,

                bairro = ?,

                cidade = ?,

                estado = ?



            WHERE id = ?

        """, (



            nome.strip(),

            telefone.strip(),

            cpf_cnpj.strip(),

            cep.strip(),

            endereco.strip(),

            numero.strip(),

            bairro.strip(),

            cidade.strip(),

            estado.strip(),

            id_cliente



        ))





# =====================================

# SERVIÇOS

# =====================================





def criar_tabela_servicos():



    with conectar() as conn:



        conn.execute("""

            CREATE TABLE IF NOT EXISTS servicos (



                id INTEGER PRIMARY KEY AUTOINCREMENT,



                id_cliente INTEGER NOT NULL,



                descricao TEXT NOT NULL,



                valor_total REAL NOT NULL,



                entrada REAL NOT NULL,



                data_cadastro TEXT NOT NULL,



                painel_principal INTEGER NOT NULL DEFAULT 0,



                FOREIGN KEY (id_cliente)



                REFERENCES clientes(id)



            )

        """)



        # Compatibilidade com bancos antigos



        colunas = conn.execute(

            "PRAGMA table_info(servicos)"

        ).fetchall()



        nomes_colunas = [

            coluna["name"]

            for coluna in colunas

        ]



        if "painel_principal" not in nomes_colunas:



            conn.execute("""

                ALTER TABLE servicos



                ADD COLUMN painel_principal

                INTEGER NOT NULL DEFAULT 0

            """)





def cadastrar_servico(

    id_cliente,

    descricao,

    valor_total,

    entrada

):



    valor_total = float(valor_total)



    entrada = float(entrada)



    if valor_total <= 0:



        raise ValueError(

            "O valor total deve ser maior que zero."

        )



    if entrada < 0:



        raise ValueError(

            "A entrada não pode ser negativa."

        )



    if entrada > valor_total:



        raise ValueError(

            "A entrada não pode ser maior que o valor total."

        )



    data_cadastro = datetime.now().strftime(

        "%Y-%m-%d"

    )



    with conectar() as conn:



        cliente = conn.execute("""

            SELECT id



            FROM clientes



            WHERE id = ?

        """, (id_cliente,)).fetchone()



        if cliente is None:



            raise ValueError(

                "Cliente não encontrado."

            )



        cursor = conn.execute("""

            INSERT INTO servicos (



                id_cliente,

                descricao,

                valor_total,

                entrada,

                data_cadastro,

                painel_principal



            )



            VALUES (?, ?, ?, ?, ?, 0)

        """, (



            id_cliente,

            descricao.strip(),

            valor_total,

            entrada,

            data_cadastro



        ))



        id_servico = cursor.lastrowid



        # A entrada inicial pertence ao caixa do serviço.

        # Ela NÃO entra automaticamente no caixa geral.



        if entrada > 0:



            conn.execute("""

                INSERT INTO movimentacoes_servico (



                    id_servico,

                    tipo,

                    descricao,

                    valor,

                    data_movimentacao,

                    categoria



                )



                VALUES (

                    ?,

                    'ENTRADA',

                    ?,

                    ?,

                    ?,

                    ?

                )

            """, (



                id_servico,

                "Entrada inicial do serviço",

                entrada,

                data_cadastro,

                "ENTRADA_INICIAL"



            ))



        return id_servico





def listar_servicos():



    with conectar() as conn:



        return conn.execute("""

            SELECT



                id,

                id_cliente,

                descricao,

                valor_total,

                entrada,

                data_cadastro,

                painel_principal



            FROM servicos



            ORDER BY id DESC

        """).fetchall()





def listar_servicos_cliente(id_cliente):



    with conectar() as conn:



        return conn.execute("""

            SELECT



                id,

                id_cliente,

                descricao,

                valor_total,

                entrada,

                data_cadastro,

                painel_principal



            FROM servicos



            WHERE id_cliente = ?



            ORDER BY id DESC

        """, (id_cliente,)).fetchall()





def editar_servico(
    id_servico,
    id_cliente,
    descricao,
    valor_total,
    entrada
):

    valor_total = float(valor_total)
    entrada = float(entrada)

    if valor_total <= 0:
        raise ValueError(
            "O valor total deve ser maior que zero."
        )

    if entrada < 0:
        raise ValueError(
            "A entrada não pode ser negativa."
        )

    if entrada > valor_total:
        raise ValueError(
            "A entrada não pode ser maior que o valor total."
        )

    with conectar() as conn:
        servico = conn.execute("""
            SELECT id
            FROM servicos
            WHERE id = ?
        """, (id_servico,)).fetchone()

        if servico is None:
            raise ValueError(
                "Serviço não encontrado."
            )

        cliente = conn.execute("""
            SELECT id
            FROM clientes
            WHERE id = ?
        """, (id_cliente,)).fetchone()

        if cliente is None:
            raise ValueError(
                "Cliente não encontrado."
            )

        conn.execute("""
            UPDATE servicos
            SET
                id_cliente = ?,
                descricao = ?,
                valor_total = ?,
                entrada = ?
            WHERE id = ?
        """, (
            id_cliente,
            descricao.strip(),
            valor_total,
            entrada,
            id_servico
        ))

        movimento = conn.execute("""
            SELECT id_movimentacao
            FROM movimentacoes_servico
            WHERE id_servico = ?
              AND categoria = 'ENTRADA_INICIAL'
            ORDER BY id_movimentacao ASC
            LIMIT 1
        """, (id_servico,)).fetchone()

        if movimento is not None:
            if entrada > 0:
                conn.execute("""
                    UPDATE movimentacoes_servico
                    SET
                        valor = ?,
                        descricao = 'Entrada inicial do serviço'
                    WHERE id_movimentacao = ?
                """, (
                    entrada,
                    movimento["id_movimentacao"]
                ))
            else:
                conn.execute("""
                    DELETE FROM movimentacoes_servico
                    WHERE id_movimentacao = ?
                """, (
                    movimento["id_movimentacao"],
                ))
        elif entrada > 0:
            data_cadastro = datetime.now().strftime(
                "%Y-%m-%d"
            )

            conn.execute("""
                INSERT INTO movimentacoes_servico (
                    id_servico,
                    tipo,
                    descricao,
                    valor,
                    data_movimentacao,
                    categoria
                )
                VALUES (?, 'ENTRADA', ?, ?, ?, ?)
            """, (
                id_servico,
                "Entrada inicial do serviço",
                entrada,
                data_cadastro,
                "ENTRADA_INICIAL"
            ))


# =====================================

# PAINEL PRINCIPAL

# =====================================





def adicionar_servico_painel(id_servico):



    with conectar() as conn:



        servico = conn.execute("""

            SELECT id



            FROM servicos



            WHERE id = ?

        """, (id_servico,)).fetchone()



        if servico is None:



            raise ValueError(

                "Serviço não encontrado."

            )



        conn.execute("""

            UPDATE servicos



            SET painel_principal = 1



            WHERE id = ?

        """, (id_servico,))





def remover_servico_painel(id_servico):



    with conectar() as conn:



        conn.execute("""

            UPDATE servicos



            SET painel_principal = 0



            WHERE id = ?

        """, (id_servico,))





def listar_servicos_painel():



    with conectar() as conn:



        return conn.execute("""

            SELECT



                s.id,

                s.id_cliente,

                s.descricao,

                s.valor_total,

                s.entrada,

                s.data_cadastro,

                s.painel_principal,



                c.nome AS nome_cliente



            FROM servicos s



            INNER JOIN clientes c



                ON c.id = s.id_cliente



            WHERE s.painel_principal = 1



            ORDER BY s.id DESC

        """).fetchall()





# ==========================================

# MOVIMENTAÇÕES DO CAIXA DO SERVIÇO

# ==========================================





def criar_tabela_movimentacoes_servico():



    with conectar() as conn:



        conn.execute("""

            CREATE TABLE IF NOT EXISTS movimentacoes_servico (



                id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,



                id_servico INTEGER NOT NULL,



                tipo TEXT NOT NULL CHECK(



                    tipo IN ('ENTRADA', 'SAIDA')



                ),



                descricao TEXT NOT NULL,



                valor REAL NOT NULL,



                data_movimentacao TEXT NOT NULL,



                categoria TEXT,



                FOREIGN KEY (id_servico)



                REFERENCES servicos(id)



                ON DELETE RESTRICT



            )

        """)





def adicionar_movimentacao_servico(

    id_servico,

    tipo,

    descricao,

    valor,

    categoria=None,

    data_movimentacao=None

):



    criar_tabela_movimentacoes_servico()



    tipo = tipo.upper().strip()



    valor = float(valor)



    if tipo not in ("ENTRADA", "SAIDA"):



        raise ValueError(

            "Tipo de movimentação inválido."

        )



    if valor <= 0:



        raise ValueError(

            "O valor deve ser maior que zero."

        )



    data_movimentacao = (

        data_movimentacao

        or datetime.now().strftime("%Y-%m-%d")

    )



    with conectar() as conn:



        servico = conn.execute("""

            SELECT id



            FROM servicos



            WHERE id = ?

        """, (id_servico,)).fetchone()



        if servico is None:



            raise ValueError(

                "Serviço não encontrado."

            )



        conn.execute("""

            INSERT INTO movimentacoes_servico (



                id_servico,

                tipo,

                descricao,

                valor,

                data_movimentacao,

                categoria



            )



            VALUES (?, ?, ?, ?, ?, ?)

        """, (



            id_servico,

            tipo,

            descricao.strip(),

            valor,

            data_movimentacao,

            categoria



        ))





def listar_movimentacoes_servico(id_servico):



    criar_tabela_movimentacoes_servico()



    with conectar() as conn:



        return conn.execute("""

            SELECT



                id_movimentacao,

                id_servico,

                tipo,

                descricao,

                valor,

                data_movimentacao,

                categoria



            FROM movimentacoes_servico



            WHERE id_servico = ?



            ORDER BY id_movimentacao DESC

        """, (id_servico,)).fetchall()





def editar_movimentacao_servico(

    id_movimentacao,

    descricao,

    valor,

    categoria=None,

    data_movimentacao=None

):



    valor = float(valor)



    if valor <= 0:



        raise ValueError(

            "O valor deve ser maior que zero."

        )



    with conectar() as conn:



        movimentacao = conn.execute("""

            SELECT id_movimentacao



            FROM movimentacoes_servico



            WHERE id_movimentacao = ?

        """, (id_movimentacao,)).fetchone()



        if movimentacao is None:



            raise ValueError(

                "Movimentação não encontrada."

            )



        if data_movimentacao is None:



            data_movimentacao = datetime.now().strftime(

                "%Y-%m-%d"

            )



        conn.execute("""

            UPDATE movimentacoes_servico



            SET



                descricao = ?,

                valor = ?,

                categoria = ?,

                data_movimentacao = ?



            WHERE id_movimentacao = ?

        """, (



            descricao.strip(),

            valor,

            categoria,

            data_movimentacao,

            id_movimentacao



        ))





def total_saidas_servico(id_servico):



    criar_tabela_movimentacoes_servico()



    with conectar() as conn:



        resultado = conn.execute("""

            SELECT COALESCE(

                SUM(valor),

                0

            ) AS total



            FROM movimentacoes_servico



            WHERE id_servico = ?



              AND tipo = 'SAIDA'

        """, (id_servico,)).fetchone()



        return float(

            resultado["total"] or 0

        )





def total_entradas_servico(id_servico):



    criar_tabela_movimentacoes_servico()



    with conectar() as conn:



        resultado = conn.execute("""

            SELECT COALESCE(

                SUM(valor),

                0

            ) AS total



            FROM movimentacoes_servico



            WHERE id_servico = ?



              AND tipo = 'ENTRADA'

        """, (id_servico,)).fetchone()



        return float(

            resultado["total"] or 0

        )





def saldo_servico(id_servico):



    entradas = total_entradas_servico(

        id_servico

    )



    saidas = total_saidas_servico(

        id_servico

    )



    return entradas - saidas





# ==========================================

# PAGAMENTOS DO CLIENTE

# ==========================================





def criar_tabela_pagamentos():



    with conectar() as conn:



        conn.execute("""

            CREATE TABLE IF NOT EXISTS pagamentos_servicos (



                id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,



                id_servico INTEGER NOT NULL,



                valor REAL NOT NULL,



                data_pagamento TEXT NOT NULL,



                FOREIGN KEY (id_servico)



                REFERENCES servicos(id)



                ON DELETE RESTRICT



            )

        """)





def total_pago_servico(id_servico):



    criar_tabela_pagamentos()



    with conectar() as conn:



        servico = conn.execute("""

            SELECT entrada



            FROM servicos



            WHERE id = ?

        """, (id_servico,)).fetchone()



        if servico is None:



            return 0.0



        entrada = float(

            servico["entrada"] or 0

        )



        pagamentos = conn.execute("""

            SELECT COALESCE(

                SUM(valor),

                0

            ) AS total



            FROM pagamentos_servicos



            WHERE id_servico = ?

        """, (id_servico,)).fetchone()



        return entrada + float(

            pagamentos["total"] or 0

        )





def restante_servico(id_servico):



    with conectar() as conn:



        servico = conn.execute("""

            SELECT valor_total



            FROM servicos



            WHERE id = ?

        """, (id_servico,)).fetchone()



        if servico is None:



            return 0.0



        valor_total = float(

            servico["valor_total"] or 0

        )



    total_pago = total_pago_servico(

        id_servico

    )



    restante = valor_total - total_pago



    return max(restante, 0.0)
# ==========================================

# PAGAMENTOS DO CLIENTE

# ==========================================


def registrar_pagamento_cliente(
    id_cliente,
    id_servico,
    valor
):

    valor = float(valor)

    if valor <= 0:

        raise ValueError(
            "O valor do pagamento deve ser maior que zero."
        )

    criar_tabela_pagamentos()

    criar_tabela_caixa()

    with conectar() as conn:

        servico = conn.execute("""
            SELECT

                id,

                id_cliente,

                descricao,

                valor_total,

                entrada

            FROM servicos

            WHERE id = ?

              AND id_cliente = ?

        """, (
            id_servico,
            id_cliente

        )).fetchone()

        if servico is None:

            raise ValueError(
                "Serviço não encontrado para este cliente."
            )

        valor_total = float(
            servico["valor_total"]
        )

    restante = restante_servico(
        id_servico
    )

    if valor > restante:

        raise ValueError(
            f"O cliente ainda deve R$ {restante:.2f}."
        )

    data_pagamento = datetime.now().strftime(
        "%Y-%m-%d"
    )

    with conectar() as conn:

        conn.execute("""
            INSERT INTO pagamentos_servicos (

                id_servico,

                valor,

                data_pagamento

            )

            VALUES (?, ?, ?)
        """, (

            id_servico,

            valor,

            data_pagamento

        ))

    # Pagamento do cliente entra no caixa geral.

    adicionar_caixa(

        tipo="ENTRADA",

        descricao=(

            f"Pagamento de cliente - "

            f"Serviço #{id_servico}"

        ),

        valor=valor,

        data_movimentacao=data_pagamento,

        id_servico=id_servico,

        origem="PAGAMENTO_CLIENTE"

    )

    novo_restante = restante_servico(
        id_servico
    )

    return {

        "valor_total": valor_total,

        "valor_pago": total_pago_servico(
            id_servico
        ),

        "restante": novo_restante

    }


# ==========================================

# CAIXA DA EMPRESA

# ==========================================


def criar_tabela_caixa():

    with conectar() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS caixa (

                id_caixa INTEGER PRIMARY KEY AUTOINCREMENT,

                tipo TEXT NOT NULL CHECK(

                    tipo IN ('ENTRADA', 'SAIDA')

                ),

                descricao TEXT NOT NULL,

                valor REAL NOT NULL,

                data_movimentacao TEXT NOT NULL,

                id_servico INTEGER,

                origem TEXT,

                FOREIGN KEY (id_servico)

                REFERENCES servicos(id)

            )

        """)


def adicionar_caixa(
    tipo,
    descricao,
    valor,
    data_movimentacao=None,
    id_servico=None,
    origem=None
):

    tipo = tipo.upper().strip()

    valor = float(valor)

    if tipo not in (
        "ENTRADA",
        "SAIDA"
    ):

        raise ValueError(
            "Tipo de caixa inválido."
        )

    if valor <= 0:

        raise ValueError(
            "O valor da movimentação deve ser maior que zero."
        )

    data_movimentacao = (
        data_movimentacao

        or datetime.now().strftime("%Y-%m-%d")
    )

    criar_tabela_caixa()

    with conectar() as conn:

        cursor = conn.execute("""
            INSERT INTO caixa (

                tipo,

                descricao,

                valor,

                data_movimentacao,

                id_servico,

                origem

            )

            VALUES (?, ?, ?, ?, ?, ?)
        """, (

            tipo,

            descricao.strip(),

            valor,

            data_movimentacao,

            id_servico,

            origem

        ))

        return cursor.lastrowid


def listar_caixa():

    criar_tabela_caixa()

    with conectar() as conn:

        return conn.execute("""
            SELECT *

            FROM caixa

            ORDER BY

                data_movimentacao DESC,

                id_caixa DESC

        """).fetchall()


def editar_caixa(
    id_caixa,
    tipo,
    descricao,
    valor,
    data_movimentacao=None
):

    tipo = tipo.upper().strip()

    valor = float(valor)

    if tipo not in (
        "ENTRADA",
        "SAIDA"
    ):

        raise ValueError(
            "Tipo de caixa inválido."
        )

    if valor <= 0:

        raise ValueError(
            "O valor deve ser maior que zero."
        )

    if data_movimentacao is None:

        data_movimentacao = datetime.now().strftime(
            "%Y-%m-%d"
        )

    with conectar() as conn:

        registro = conn.execute("""
            SELECT id_caixa

            FROM caixa

            WHERE id_caixa = ?

        """, (id_caixa,)).fetchone()

        if registro is None:

            raise ValueError(
                "Movimentação do caixa não encontrada."
            )

        conn.execute("""
            UPDATE caixa

            SET

                tipo = ?,

                descricao = ?,

                valor = ?,

                data_movimentacao = ?

            WHERE id_caixa = ?

        """, (

            tipo,

            descricao.strip(),

            valor,

            data_movimentacao,

            id_caixa

        ))


def saldo_caixa():

    criar_tabela_caixa()

    with conectar() as conn:

        entradas = conn.execute("""
            SELECT COALESCE(

                SUM(valor),

                0

            ) AS total

            FROM caixa

            WHERE tipo = 'ENTRADA'

        """).fetchone()["total"]

        saidas = conn.execute("""
            SELECT COALESCE(

                SUM(valor),

                0

            ) AS total

            FROM caixa

            WHERE tipo = 'SAIDA'

        """).fetchone()["total"]

        return float(
            entradas - saidas
        )


# ==========================================

# RELATÓRIOS

# ==========================================


def quantidade_clientes():

    with conectar() as conn:

        resultado = conn.execute("""
            SELECT COUNT(*) AS total

            FROM clientes

        """).fetchone()

        return int(
            resultado["total"] or 0
        )


def quantidade_servicos():

    with conectar() as conn:

        resultado = conn.execute("""
            SELECT COUNT(*) AS total

            FROM servicos

        """).fetchone()

        return int(
            resultado["total"] or 0
        )


def resumo_mes(ano, mes):

    ano = int(ano)

    mes = int(mes)

    periodo = f"{ano:04d}-{mes:02d}"

    with conectar() as conn:

        entradas_caixa = conn.execute("""
            SELECT COALESCE(

                SUM(valor),

                0

            ) AS total

            FROM caixa

            WHERE tipo = 'ENTRADA'

              AND substr(

                  data_movimentacao,

                  1,

                  7

              ) = ?

        """, (periodo,)).fetchone()["total"]

        saidas_caixa = conn.execute("""
            SELECT COALESCE(

                SUM(valor),

                0

            ) AS total

            FROM caixa

            WHERE tipo = 'SAIDA'

              AND substr(

                  data_movimentacao,

                  1,

                  7

              ) = ?

        """, (periodo,)).fetchone()["total"]

        servicos = conn.execute("""
            SELECT COUNT(*) AS total

            FROM servicos

            WHERE substr(

                data_cadastro,

                1,

                7

            ) = ?

        """, (periodo,)).fetchone()["total"]

        clientes = conn.execute("""
            SELECT COUNT(*) AS total

            FROM clientes

            WHERE substr(

                data_cadastro,

                1,

                7

            ) = ?

        """, (periodo,)).fetchone()["total"]

    return {

        "entradas": float(
            entradas_caixa or 0
        ),

        "saidas": float(
            saidas_caixa or 0
        ),

        "saldo": float(
            (entradas_caixa or 0)

            -

            (saidas_caixa or 0)
        ),

        "servicos": int(
            servicos or 0
        ),

        "clientes": int(
            clientes or 0
        )

    }


# ==========================================

# DOCUMENTOS

# ==========================================


def criar_tabela_documentos():

    with conectar() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS documentos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                id_cliente INTEGER NOT NULL,

                id_servico INTEGER,

                tipo TEXT NOT NULL,

                descricao TEXT,

                nome_arquivo TEXT NOT NULL,

                caminho_arquivo TEXT NOT NULL,

                data_documento TEXT NOT NULL,

                data_cadastro TEXT NOT NULL,

                FOREIGN KEY (id_cliente)

                REFERENCES clientes(id)

                ON DELETE RESTRICT,

                FOREIGN KEY (id_servico)

                REFERENCES servicos(id)

                ON DELETE RESTRICT

            )

        """)


def cadastrar_documento(
    id_cliente,
    id_servico,
    tipo,
    descricao,
    nome_arquivo,
    caminho_arquivo,
    data_documento=None
):

    if not id_cliente:

        raise ValueError(
            "O cliente é obrigatório."
        )

    if not tipo or not tipo.strip():

        raise ValueError(
            "O tipo do documento é obrigatório."
        )

    if not nome_arquivo or not nome_arquivo.strip():

        raise ValueError(
            "O nome do arquivo é obrigatório."
        )

    if not caminho_arquivo or not caminho_arquivo.strip():

        raise ValueError(
            "O caminho do arquivo é obrigatório."
        )

    data_cadastro = datetime.now().strftime(
        "%Y-%m-%d"
    )

    if not data_documento:

        data_documento = data_cadastro

    with conectar() as conn:

        cliente = conn.execute("""
            SELECT id

            FROM clientes

            WHERE id = ?

        """, (
            id_cliente,

        )).fetchone()

        if cliente is None:

            raise ValueError(
                "Cliente não encontrado."
            )

        if id_servico:

            servico = conn.execute("""
                SELECT

                    id,

                    id_cliente

                FROM servicos

                WHERE id = ?

            """, (

                id_servico,

            )).fetchone()

            if servico is None:

                raise ValueError(
                    "Serviço não encontrado."
                )

            if int(
                servico["id_cliente"]
            ) != int(id_cliente):

                raise ValueError(
                    "O serviço não pertence ao cliente informado."
                )

        cursor = conn.execute("""
            INSERT INTO documentos (

                id_cliente,

                id_servico,

                tipo,

                descricao,

                nome_arquivo,

                caminho_arquivo,

                data_documento,

                data_cadastro

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            id_cliente,

            id_servico,

            tipo.strip(),

            (descricao or "").strip(),

            nome_arquivo.strip(),

            caminho_arquivo.strip(),

            data_documento,

            data_cadastro

        ))

        return cursor.lastrowid


def listar_documentos_cliente(
    id_cliente
):

    criar_tabela_documentos()

    with conectar() as conn:

        return conn.execute("""
            SELECT

                d.id,

                d.id_cliente,

                d.id_servico,

                d.tipo,

                d.descricao,

                d.nome_arquivo,

                d.caminho_arquivo,

                d.data_documento,

                d.data_cadastro,

                s.descricao AS descricao_servico

            FROM documentos d

            LEFT JOIN servicos s

                ON s.id = d.id_servico

            WHERE d.id_cliente = ?

            ORDER BY

                d.data_documento DESC,

                d.id DESC

        """, (

            id_cliente,

        )).fetchall()


def listar_documentos():

    criar_tabela_documentos()

    with conectar() as conn:

        return conn.execute("""
            SELECT

                d.id,

                d.id_cliente,

                d.id_servico,

                d.tipo,

                d.descricao,

                d.nome_arquivo,

                d.caminho_arquivo,

                d.data_documento,

                d.data_cadastro,

                c.nome AS nome_cliente,

                s.descricao AS descricao_servico

            FROM documentos d

            INNER JOIN clientes c

                ON c.id = d.id_cliente

            LEFT JOIN servicos s

                ON s.id = d.id_servico

            ORDER BY

                d.data_documento DESC,

                d.id DESC

        """).fetchall()


def obter_documento(id_documento):

    criar_tabela_documentos()

    with conectar() as conn:

        return conn.execute("""
            SELECT

                d.id,

                d.id_cliente,

                d.id_servico,

                d.tipo,

                d.descricao,

                d.nome_arquivo,

                d.caminho_arquivo,

                d.data_documento,

                d.data_cadastro,

                c.nome AS nome_cliente,

                s.descricao AS descricao_servico

            FROM documentos d

            INNER JOIN clientes c

                ON c.id = d.id_cliente

            LEFT JOIN servicos s

                ON s.id = d.id_servico

            WHERE d.id = ?

        """, (

            id_documento,

        )).fetchone()


def editar_documento(
    id_documento,
    id_cliente,
    id_servico,
    tipo,
    descricao,
    nome_arquivo,
    caminho_arquivo,
    data_documento
):

    if not id_cliente:

        raise ValueError(
            "O cliente é obrigatório."
        )

    if not tipo or not tipo.strip():

        raise ValueError(
            "O tipo do documento é obrigatório."
        )

    with conectar() as conn:

        documento = conn.execute("""
            SELECT id

            FROM documentos

            WHERE id = ?

        """, (

            id_documento,

        )).fetchone()

        if documento is None:

            raise ValueError(
                "Documento não encontrado."
            )

        cliente = conn.execute("""
            SELECT id

            FROM clientes

            WHERE id = ?

        """, (

            id_cliente,

        )).fetchone()

        if cliente is None:

            raise ValueError(
                "Cliente não encontrado."
            )

        if id_servico:

            servico = conn.execute("""
                SELECT

                    id,

                    id_cliente

                FROM servicos

                WHERE id = ?

            """, (

                id_servico,

            )).fetchone()

            if servico is None:

                raise ValueError(
                    "Serviço não encontrado."
                )

            if int(
                servico["id_cliente"]
            ) != int(id_cliente):

                raise ValueError(
                    "O serviço não pertence ao cliente informado."
                )

        conn.execute("""
            UPDATE documentos

            SET

                id_cliente = ?,

                id_servico = ?,

                tipo = ?,

                descricao = ?,

                nome_arquivo = ?,

                caminho_arquivo = ?,

                data_documento = ?

            WHERE id = ?

        """, (

            id_cliente,

            id_servico,

            tipo.strip(),

            (descricao or "").strip(),

            nome_arquivo.strip(),

            caminho_arquivo.strip(),

            data_documento,

            id_documento

        ))


# ==========================================

# INICIALIZAÇÃO

# ==========================================


criar_banco()

def remover_documento(id_documento):
    with conectar() as conn:
        documento = conn.execute("""
            SELECT id, caminho_arquivo
            FROM documentos
            WHERE id = ?
        """, (id_documento,)).fetchone()

        if documento is None:
            raise ValueError(
                "Documento não encontrado."
            )

        conn.execute("""
            DELETE FROM documentos
            WHERE id = ?
        """, (id_documento,))

        return documento["caminho_arquivo"]