from flet import (Page, TextButton, Container, ButtonStyle, Column, CrossAxisAlignment, Row, Text, Icon,
                  padding, icons, colors)
from dotenv import load_dotenv
from os import getenv

load_dotenv()

cor = {}

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
                bgcolor=cor['primary_lighter'] if self.selected_item == label else 'transparent',
                border_radius=10,
                width=200,
                content=Container(
                    padding=7,
                    content=Row(
                        controls=[
                            # Indicador de seleção
                            Container(height=30, width=4, border_radius=5,
                                      bgcolor=cor['white'] if self.selected_item == label else cor[
                                          'unselected_menu_item']),

                            # Divisor de espaçamento
                            Container(width=10, height=1),

                            # Icone
                            Container(content=Icon(name=icon, color=cor['white'], size=37)),

                            # Label
                            Container(content=Text(value=label, color=cor['white'], size=17))
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
            controls=[
                Container(
                    bgcolor=cor["primary_medium"],
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[

                            # Cabeçalho - Usuário
                            Container(
                                content=Row(
                                    controls=[
                                        Container(
                                            content=Text(value=getenv('CLASSNAME'), size=25, color="#FFFFFF",
                                                         font_family='protest'),
                                            padding=padding.symmetric(10, 25)
                                        ),
                                    ]
                                )
                            ),

                            # Divisor do cabeçalho
                            Container(height=.5, bgcolor=cor["white"], width=80, padding=padding.symmetric(10, 25)),

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
                                        Row(controls=[self._botao_menu("Configurações", icons.SETTINGS_ROUNDED)]),

                                        # Divisor para o botão de saída
                                        Container(width=200, height=1, bgcolor=colors.with_opacity(.5, cor["white"])),

                                        # Botão de saída
                                        Row(controls=[self._botao_menu("Sair", icons.EXIT_TO_APP_ROUNDED)]),
                                        Row(height=120)
                                    ]
                                )
                            )
                        ],
                    )
                )
            ]
        )
