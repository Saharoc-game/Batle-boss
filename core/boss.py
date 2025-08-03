import random
from rich import print

from core.effect import PoisonEffect, BleedingEffect, FireEffect, StunEffect, RegenerationEffect

from utils.input_until import check_dogde_and_parry

from utils.rich_UI import UI


class Boss: 

    """Базовый класс босса. Описывает общую механику: здоровье, магия, супер-удар."""

    def __init__(self): 
        self.hp = int(random.choice([50, 55, 60]))
        self.magic = random.randint(3, 4)
        self.HP_MAX = self.hp
        self.RECHARGE_MAX = 10
        self.recharge = self.RECHARGE_MAX
        self.super_punch = "Супер удар" # Название супер удара
        
    def attack(self, bosses_killed, armor_defense, dodge, parry): # Атака Босса
        """
        Атака босса.
        Если накоплен супер удар, наносит большой урон.
        Иначе, обычный удар
        bosses_killed: число убитых боссов (увеличивает урон)
        armor_defense: процент защиты игрока
        dodge: шанс уклонения
        parry: шанс парирования 
        Возвращаем урон, который нужно отнять от игрока.
        """

        if self.recharge >= self.RECHARGE_MAX : # Супер удар
            self.damage = random.randint(10, 15)
            UI.add_message_to_main(f"Босс использует [cyan]{self.super_punch}[/cyan] и наносит - [red]{self.damage}[/red] урона")
            self.recharge = 0
            return self.damage
        
        else : # Обычная Атака
            x = random.randint(0, 5)
            self.damage = int(x - x * (armor_defense / 100) + bosses_killed)
            UI.add_message_to_main(f"Босс нанёс вам урон -  [red]{self.damage}[/red]")
            result = check_dogde_and_parry(dodge, parry, self.damage)
            if "player_damage" in result:
                damage = result["player_damage"]
            if "boss_damage" in result:
                self.hp -= result["boss_damage"]
            else :
                damage = 0
            return damage

    def health_add(self): # Лечение Босса
        """
        Лечение босса.
        Отнимает 1 магию.
        Увеличивает своё здоровье на 10
        Ничего не возвращает
        """

        self.magic -= 1
        self.hp += 10
        UI.add_message_to_main("Босс использовал заклинание [green]<Исцеление>[/green]")
    
    def add_recharge(self) : # Накопление супер удара
        """
        Накопление супер удара.
        Добавляет к перезарядке 2.5
        Ничего не возвращает
        """

        self.recharge += 2.5
        UI.add_message_to_main("Босс копит супер удар")

    def cast_spell_effect(self, target) : 
        """Базовый метод — эффект заклинания. Переопределяется в подклассах."""

        pass

class BossWar (Boss) : 
    """Босс воин. Отличается увеличенным здоровьем и эффектом оглушения"""

    def __init__(self):
        super().__init__()
        self.hp = random.choice([60, 65, 70])
        self.HP_MAX = self.hp
        self.super_punch = "Гнев Титана" # Название супер удара
        self.magic_for_spell_effect = 1 # Количество магии для накладывания эффекта

    def cast_spell_effect(self, target): # Босс накладывает эффект на игрока
        """
        Накладывает эффект оглушения на 1 ход
        Отнимаем 1 магию
        target: игрок
        """

        self.magic -= 1
        duration = 1
        UI.add_message_to_main(f"[red]Босс вас оглушил на [/red][blue]{duration}[/blue][red] ходов![/red]")
        stun = StunEffect() # Создаём эффект оглушения
        target.add_effect(stun) # Добавляем эффект оглушения

class BossWiz (Boss) :
    """Маг босс. Отличается увеличенной магией и эффектом горения"""

    def __init__(self): 
        super().__init__()
        self.magic = random.randint(6, 7)
        self.super_punch = "Пламя Затмений" # Название супер удара
        self.magic_for_spell_effect = 2 # Количество магии для накладывания эффекта

    def cast_spell_effect(self, target): # Босс накладывает эффект на игрока
        """
        Накладывает эффект горения на от 1 до 3 ходов
        Отнимаем 2 магии
        Урон эффекта: от 2 до 4
        target: игрок
        """

        UI.add_message_to_main("[red]Босс колдует на вас огонь![/red]")
        self.magic -= 2
        duration = random.randint(1,3)
        damage = random.randint(2,4)
        fire = FireEffect(duration, damage) # Создаём эффект горения
        target.add_effect(fire) # Добавляем эффект горения
        
class BossArc (Boss): 
    """Лучник босс. Отличается умененьшенным здоровьем, но магия для кастования эффекта не нужна"""

    def __init__(self): 
        super().__init__()
        self.hp = random.choice([40, 45, 50])
        self.HP_MAX = self.hp
        self.magic = random.randint(5,6)
        self.super_punch = "Дождь Призрачных Стрел" # Название супер удара
        self.magic_for_spell_effect = 0 # Количество магии для накладывания эффекта

    def cast_spell_effect(self, target): # Босс накладывает эффект на игрока
        """
        Накладывает эффект кровотечения от 1 до 2 ходов
        Отнимаем (боссу) 5 хп
        Урон эффекта: от 1 до 3
        target: игрок
        """

        UI.add_message_to_main("[red]В вас попала стрела! И у вас пошло кровотечение![/red]")
        self.hp -= 5
        duration = random.randint(1,2)
        damage = random.randint(1,3)
        bleeding = BleedingEffect(duration, damage) # Создаём эффект кровотечения
        target.add_effect(bleeding) # Добавляем эффект кровотечения
        
def random_boss() : # Создание случайного Босса
    x = random.randint(0, 2)
    if x == 0 :
        return BossWar() # Воин
    elif x == 1 :
        return BossWiz() # Маг
    else:
        return BossArc() # Лучник
