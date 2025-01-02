from flet import AlertDialog, Page, Colors
from abc import ABC, abstractmethod


class _Detalhes(ABC):
    def __init__(self, page: Page):
        self.page = page

        self.get = self._get()

    def _get(self) -> AlertDialog:
        return AlertDialog(
            bgcolor=Colors.SURFACE
        )


class DetalhesAluno(_Detalhes):
    def __init__(self, page: Page):
        super().__init__(page)
