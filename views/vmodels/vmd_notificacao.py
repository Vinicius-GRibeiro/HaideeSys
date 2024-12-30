from flet import (SnackBar, Page, Text, Colors, FontWeight, RoundedRectangleBorder, SnackBarBehavior,
                  DismissDirection, Row, Icon)


class Notificacao:
    def __init__(self, page: Page):
        self.page = page

    def notificar(self, msg: str, tipo: str = 'informacao', icone: str = None):
        cor_fundo = cor_texto = None


        match tipo:
            case 'informacao':
                cor_fundo = Colors.SECONDARY
                cor_texto = Colors.ON_SECONDARY
            case 'erro':
                cor_fundo = Colors.ERROR
                cor_texto = Colors.ON_ERROR

        sb = SnackBar(
            content=Row(
                controls=[
                    Icon(name=icone, color=cor_texto),
                    Text(value=msg, font_family='nunito', color=cor_texto, size=17, weight=FontWeight.W_700)
                ]
            ),
            bgcolor=cor_fundo,
            shape=RoundedRectangleBorder(10),
            behavior=SnackBarBehavior.FLOATING,
            width=self.page.width * .7,
            dismiss_direction=DismissDirection.HORIZONTAL,

        )

        self.page.snack_bar = sb
        self.page.snack_bar.open = True
        self.page.update()
