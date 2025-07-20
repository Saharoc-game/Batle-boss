from rich import print

from core.effect.effectmain import Effect

from utils.rich_UI import UI

class StunEffect(Effect) :

    """Эффект Оглушение (Стан): Игрок пропускает ход. Длится 1 ход """

    def __init__(self):
        UI.add_message_to_main("[red]Вас оглушили![/red]")
        self.duration = 1