from flet import Page, Container, Text
from .vmodels.view_factory import ViewFactory


class Pontos:
    def __init__(self, page: Page):
        self.page = page


        self.get = ViewFactory.get_view(page, view_controls=[self.container_main()], view_name='Pontos')

    def container_main(self) -> Container:
        return Container(
            Text('pontos')
        )
