from flet import Page, View, Row, Container, Column, CrossAxisAlignment, colors
from .vmd_menu import Menu


class ViewFactory:
    @classmethod
    def get_view(cls, page: Page, view_controls: list[Container], view_name: str) -> View:
        '''

        :param page: Página do aplicativo flet
        :param view_controls: lista de Containers que serão adicionados logo após o menu, em uma linha, ou seja, horizontalmente
        :param view_name: Nome da View, para indicação no menu
        :return:
        '''
        return View(
            spacing=0, padding=0, bgcolor=colors.BACKGROUND,
            controls=[
                Row(
                    height=page.window.height,
                    controls=[
                        Column(
                            controls=[
                                Container(
                                    content=Menu(page=page, selected_item=view_name).get,
                                )
                            ]
                        ),

                        Container(
                            content=Column(
                                spacing=10, horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=view_controls
                            )
                        )
                    ]
                )
            ]
        )
