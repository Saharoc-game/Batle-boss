from core.effect.poison import PoisonEffect

from utils.rich_UI import UI

class FireEffect(PoisonEffect) :
     
    """Эффект Огонь: Каждый ход отнимает damage. Длится duration ходов. Каждый ход снижает урон на 30% """

    def __init__(self, duration: int, damage: int):
        """ Создаём новый эффект. Принимаем duration и damage"""
        super().__init__(duration, damage)
        UI.add_message_to_main(f"[red]Вас подожгли![/red] Вы будете гореть [blue]{duration}[/blue] ходов. А так же сила [blue]{damage}[/blue] ")
        self.damage = damage

    def apply(self, target):
        """Обновляем эффект. Отнимаем у target урон эффекта. Также снижаем damage на 30%"""
        target.hp -= self.damage
        self.damage = int(self.damage - (self.damage * 0.3))

