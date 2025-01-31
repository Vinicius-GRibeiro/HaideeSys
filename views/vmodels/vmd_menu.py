import os

from flet import (Page, TextButton, Container, ButtonStyle, Column, CrossAxisAlignment, Row, Text, Icon,
                  padding, icons, Colors)
from dotenv import load_dotenv
from os import getenv

from flet.core.types import FontWeight

load_dotenv()

class Menu:
    def __init__(self, page: Page, selected_item: str):
        self.page = page
        self.selected_item = selected_item
        self.get = self._get()

    def _botao_menu(self, label: str, icon: str):
        btn = TextButton(
            on_click=lambda e: self._on_click_btn_menu(e, label),
            style=ButtonStyle(
                overlay_color='transparent'
            ),
            content=Container(
                bgcolor=Colors.PRIMARY_CONTAINER if self.selected_item == label else 'transparent',
                border_radius=10,
                width=200,
                content=Container(
                    padding=7,
                    content=Row(
                        controls=[
                            # Indicador de seleção
                            Container(height=30, width=4, border_radius=5,
                                      bgcolor='transparent' if label == 'Sair' else Colors.ON_PRIMARY_CONTAINER if self.selected_item == label else Colors.ON_PRIMARY),

                            # Divisor de espaçamento
                            Container(width=10, height=1),

                            # Icone
                            Container(content=Icon(name=icon, color=Colors.ON_PRIMARY_CONTAINER if self.selected_item == label else Colors.ON_PRIMARY, size=37)),

                            # Label
                            Container(content=Text(value=label, color=Colors.ON_PRIMARY_CONTAINER if self.selected_item == label else Colors.ON_PRIMARY, size=17))
                        ]
                    )
                )
            )
        )

        return btn

    @staticmethod
    def _on_click_btn_menu(e, label: str):
        match label:
            case 'Início':
                e.page.go('/')
            case 'Alunos':
                e.page.go('/alunos')
            case 'Turmas':
                e.page.go('/turmas')
            case 'Ocorrências':
                e.page.go('/ocorrencias')
            case 'Configurações':
                e.page.go('/config')
            case 'Pontos':
                e.page.go('/pontos')
            case 'Sair':
                ...

    def _get(self):
        return Column(
            height=self.page.window.height,
            controls=[
                Container(
                    expand=True,
                    bgcolor=Colors.PRIMARY,
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[

                            # Cabeçalho - Usuário
                            Container(
                                content=Column(
                                    spacing=0,
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Container(
                                            content=Text(value=os.getenv('APPNAMEINITIALS').upper(), size=70, color=Colors.ON_PRIMARY,
                                                         font_family='logo_iniciais'),
                                            padding=padding.only(left=25, right=25, top=10),
                                        ),

                                        Container(
                                            content=Text(value=os.getenv('APPNAME').upper(), size=30, color=Colors.ON_PRIMARY,
                                                         font_family='nunito', weight=FontWeight.W_800),
                                            padding=padding.only(left=25, right=25, bottom=10, top=-20),
                                        ),

                                        Row(
                                            controls=[
                                                Text(value='Oficina:', color=Colors.ON_PRIMARY, font_family='nunito', size=17, weight=FontWeight.W_500),
                                                Text(value=os.getenv('CLASSNAME').capitalize(), color=Colors.ON_PRIMARY, font_family='nunito', weight=FontWeight.W_300, size=15),
                                            ]
                                        ),

                                        Row(
                                            controls=[
                                                Text(value='Professor:', color=Colors.ON_PRIMARY, font_family='nunito', size=17, weight=FontWeight.W_500),
                                                Text(value=os.getenv('TEACHERNAME').capitalize(), color=Colors.ON_PRIMARY, font_family='nunito', weight=FontWeight.W_300, size=15),
                                            ]
                                        )
                                    ]
                                )
                            ),

                            # Divisor do cabeçalho
                            Container(height=2, bgcolor='transparent', width=1),
                            Container(height=.5, bgcolor=Colors.ON_PRIMARY, width=80, padding=padding.symmetric(10, 25)),

                            # Botões do menu
                            Container(
                                padding=10,
                                content=Column(
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    spacing=10,
                                    controls=[
                                        # Botões de opções do menu
                                        Row(controls=[self._botao_menu("Início", icons.HOME_ROUNDED)]),
                                        Row(controls=[self._botao_menu("Alunos", icons.FACE_ROUNDED)]),
                                        Row(controls=[self._botao_menu("Turmas", icons.PEOPLE_ROUNDED)]),
                                        Row(controls=[self._botao_menu("Ocorrências", icons.ASSIGNMENT_ROUNDED)]),
                                        Row(controls=[self._botao_menu("Pontos", icons.SCOREBOARD)]),
                                        Row(controls=[self._botao_menu("Configurações", icons.SETTINGS_ROUNDED)]),


                                        Container(
                                            content=Column(
                                                controls=[
                                                    Container(width=200, height=2, bgcolor=Colors.with_opacity(.5, Colors.ON_PRIMARY)),
                                                    Row(controls=[self._botao_menu("Sair", icons.EXIT_TO_APP_ROUNDED)]),
                                                ],
                                                horizontal_alignment=CrossAxisAlignment.CENTER
                                            ),
                                            padding=padding.only(top=15),
                                        ),

                                    ]
                                )
                            )
                        ],
                    )
                )
            ]
        )
