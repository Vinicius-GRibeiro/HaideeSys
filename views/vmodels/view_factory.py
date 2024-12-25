from flet import Page, View, Row, Container, Column, CrossAxisAlignment


class ViewFactory:
    @classmethod
    def get_view(cls, page: Page, view_controls: list[Container]) -> View:
        '''

        :param page: Página do aplicativo flet
        :param view_controls: lista de Containers que serão adicionados logo após o menu, em uma linha, ou seja, horizontalmente
        :return:
        '''
        return View(
            spacing=0, padding=0, bgcolor='grey',
            controls=[
                Row(
                    controls=[
                        # TODO: ADD MENU CONTROL
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
