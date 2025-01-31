from flet import Page, Container, Text, Colors, Column, Row, FontWeight, padding
from flet.core.padding import Padding
from flet.core.types import MainAxisAlignment

from .vmodels.view_factory import ViewFactory
from .vmodels.vmd_botoes import BotaoEscolhaCores


class Configuracoes:
    def __init__(self, page: Page):
        self.page = page

        self.btn_escolha_cores = BotaoEscolhaCores(self.page)
        self.get = ViewFactory.get_view(page, view_controls=[self.container_main()], view_name='Configurações')

    def container_main(self) -> Container:
        return Container(
            bgcolor=Colors.with_opacity(.08, Colors.TERTIARY),
            padding=20,
            border_radius=10,
            width=950,
            content= Column(
                controls=[
                    Row(
                        controls=[
                            Text('Tema', font_family='nunito', color=Colors.PRIMARY, weight=FontWeight.W_800, size=17),
                            self.btn_escolha_cores.get
                        ],
                        width=900,
                        alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),

                    Container(width=900, height=.5, bgcolor=Colors.PRIMARY, padding=padding.symmetric(10, 0))
                ]
            )
        )