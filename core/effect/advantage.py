from rich import print

from utils.rich_UI import UI

from core.effect.effectmain import Effect


class AdvantageEffect(Effect) :

    def __init__(self):
        """Создаём эффект. Длится duration ходов """
        self.duration = 2
        UI.add_message_to_main(f"У вас перевес! Ваш урон снижен на [red]30%[/red]")

    def apply(self, target):
        target.advantage = 30
