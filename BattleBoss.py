
import random

from rich.panel import Panel
from rich import print

from core import boss 
from core import player

from core.effect import PoisonEffect, BleedingEffect, FireEffect, StunEffect
from core.event.shop import ShopEvent
from utils.input_until import get_valid_int_input

from utils.rich_UI import UI

print(Panel("Добро пожаловать в [bold]Battle Boss[/bold] — текстовую RPG-игру.\nВ которой вам предстоит сражаться с боссами, улучшать своё снаряжение и выживать как можно дольше!", title="BattleBoss"))

P1 = player.choose_playerclass() # Создание игрока

B1 = boss.random_boss() # Создание Босса

input("Нажмите чтобы начать... ")

UI.update_stats(P1, B1)
UI.show_control()
P1.inventory.drop_item_ring()

while P1.hp > 0:

    if P1.bosses_killed%10==0 and P1.bosses_killed!= 0:
        shop = ShopEvent()
        shop.trigger(P1)

    if B1.hp <= 0:
        P1.bosses_killed += 1

        # Улучшения характеристик

        P1.hp += 5
        P1.magic += 1
        P1.max_hp += 5
        P1.max_magic += 1
        P1.money += 3
        # Выдача предметов

        x = random.randint(0, 1)

        if x == 0 : # Выдача брони
            P1.inventory.drop_item_armor()

        if x == 1 : # Выдача меча
            P1.inventory.drop_item_sword(P1.bosses_killed)

        UI.add_message_to_main(f"Поздравлю, игрок! Вы смогли победить босса под номером {P1.bosses_killed}")
        UI.add_message_to_main(f"Ваша максимальное здоровье теперь {P1.max_hp} Максимальное количество магии {P1.max_magic}")
        UI.add_message_to_main("Магия увеличена на 1, здоровье на 5. Также вы нашли 3 монеты!")
        B1 = boss.random_boss() # Создание Босса
        UI.update_stats(P1, B1)
        UI.add_message_to_main("Этот босс бьет сильнее предыдущего на 1 урон.")

    if not P1.has_effect(StunEffect) :

    # Защита от дураков (цифры)
        hod_igroka = get_valid_int_input(
            "Ваш ход от [blue]0[/blue] до [blue]5[/blue]\n",
            [0, 1, 2, 3, 4, 5]
        )
    # Лечение игрока
        if hod_igroka == 2 and P1.magic > 0:
            P1.healf()

    # Восполнение магии игрока
        if hod_igroka == 3 and P1.money > 0:
            P1.magic_add()

    # Удар игрока
        if hod_igroka == 1:
            B1.hp -= P1.attack()
            
    # Инвентарь
        if (hod_igroka == 4) and (len(P1.inventory.inventory)>0):
            P1.player_choose_item()

    # Продажа
        if (hod_igroka == 5) and (len(P1.inventory.inventory)>0):
            P1.money += P1.inventory.sell_item()
      
    if B1.hp > 0:
        if B1.hp / B1.HP_MAX < 0.5:  # Проверяем, если HP < 50%
            if B1.magic > 0:  # Если есть магия, лечимся
                B1.health_add()
            else:  # Если магия закончилась, босс атакует или кастует эффект
                if (random.randint(0, 1) == 1) and (B1.magic > B1.magic_for_spell_effect) : 
                    B1.cast_spell_effect(P1)
                else :
                    P1.hp -= B1.attack(P1.bosses_killed, P1.armor_defense, P1.dodge, P1.parry)
        else :
            x = random.randint(0, 2)
            if (x == 0) and (B1.recharge < B1.RECHARGE_MAX):
                B1.add_recharge()  # Копит супер-удар
            elif (x == 1) and (B1.magic > B1.magic_for_spell_effect) :
                B1.cast_spell_effect(P1)
            else :
                P1.hp -= B1.attack(P1.bosses_killed, P1.armor_defense, P1.dodge, P1.parry)
    
    P1.effect_update()
    P1.rounds = P1.rounds + 1
    UI.update_stats(P1, B1)

# Проигрыш игрока, записываем рекорд

else:
    print(f"Вы погибли! Но вы смогли убить {P1.bosses_killed} боссов!")
    f = open("BattleBossrecords.txt", "r+")
    last_line = int(f.readlines()[-1])
    print(last_line)
    if last_line < P1.rounds :
        x = str(P1.rounds)
        f.write(x)
        print(f"Вы поставили новый рекорд: {x} раундов")
    else :
        print(f"Рекорд: {last_line} раундов")
    f.close()
input("")
