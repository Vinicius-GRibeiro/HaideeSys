from flet import Page, Container
from vmodels.view_factory import ViewFactory

class Inicio:
    def __init__(self, page: Page):
        self.get = ViewFactory.get_view(page, view_controls=[self.container_main()])

    def container_main(self) -> Container:
        return Container(

        )
