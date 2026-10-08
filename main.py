import flet as ft

from pages.login import mostrar_login
from database import criar_banco, criar_tabela_servicos


def main(page: ft.Page):

    criar_banco()
    criar_tabela_servicos()

    mostrar_login(page)


ft.run(main, assets_dir="assets")