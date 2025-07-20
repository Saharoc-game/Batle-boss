import random
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.item.sword import Sword
from core.item.armor import Armor
from core.item.ring import Ring

from utils.input_until import get_valid_int_input
from utils.rich_UI import UI


class Inventory:
    """
    Класс Инвентарь.
    Используется внутри класса Игрок.
    Описывает логику хранения, экипировки, продажи и получения предметов.
    """

    def __init__(self):

        self.mass = 0

        # Пример предметов по умолчанию
        self.INVENTORY_STATS = [
                    {
                        "type": "sword",
                        "cost":3, 
                        "damage":5, 
                        "name": "Обычный меч", 
                        "description": "Простой, надежный меч с хорошим балансом и удобной рукоятью.",
                        "weight": 2
                    },

                    {  
                        "type": "sword",
                        "cost":3, 
                        "defenсe": 3, 
                        "name": "Кожаная броня", 
                        "description": "Легкая, удобная, немного снижает урон.",
                        "weight": 4.5
                    }
        ]

        self.inventory = [] # Сам инвентарь

    def choose_item(self):
        """
        Выбор предмета.
        Создаёт таблицу со всеми предметами и позволяет игроку выбрать предмет для экипировки.
        Возвращает словарь с параметрами выбранного предмета.
        """

        if len(self.inventory)<=0:
            UI.add_message_to_main("У вас нету предметов!")
            return None
        console = Console()
        console.print(Panel("[bold green]Выберите предмет, который вы экипируете[/bold green]"))

        valid_indexes = [0]


        # Создаём таблицу
        table = Table(show_header=True, header_style="bold magenta") 

        # Создаём колонки
        table.add_column("№", style="bold cyan", width=3, justify="center") 
        table.add_column("Название", style="bold yellow")
        table.add_column("Тип", style="green")
        table.add_column("Параметр", style="bold blue")

        for index, item in enumerate(self.inventory, start=1): # Добавляем предметы по очереди
            if item['type'] == 'sword': # Меч
                table.add_row(
                    str(index),
                    f"[white]{item['name']}[/white]",
                    "[yellow]Меч[/yellow]",
                    f"[red]Урон {item['damage']}[/red]"
                ) # Добавляем строчку
                valid_indexes.append(index)
            elif item['type'] == 'armor': # Броня
                table.add_row(
                    str(index),
                    f"[white]{item['name']}[/white]",
                    "[blue]Броня[/blue]",
                    f"[green]Защита {item['defence']}[/green]"
                ) # Добавляем строчу
                valid_indexes.append(index)
            elif item['type'] == 'ring' :
                table.add_row(
                    str(index),
                    f"[white]{item['name']}[/white]",
                    "[red]Кольцо[/red]",
                    f"[bright_red]Регенерация {item['heal']}[/bright_red]"
                ) # Добавляем строчку
                valid_indexes.append(index)

        UI.show_table_in_main(table) # Выводим таблицу

        ans = get_valid_int_input(
            "[bold green]Введите номер предмета:[/bold green] ",
            valid_indexes
        ) - 1 # Игрок выбирает предмет

        if 0 <= ans < len(self.inventory):
            selected_item = self.inventory[ans]
            if selected_item['type'] == 'sword':
                console.print(
                    Panel(
                        f"[bold green]Вы экипировали меч[/bold green] [yellow]{selected_item['name']}[/yellow] [bold green]с уроном[/bold green] [red]{selected_item['damage']}[/red]",
                        border_style="bright_blue"
                    )
                )
                UI.show_item_in_layoutitem(selected_item)
                return {'sword_damage': selected_item['damage']}
            
            elif selected_item['type'] == 'armor':
                console.print(
                    Panel(
                        f"[bold green]Вы экипировали броню[/bold green] [yellow]{selected_item['name']}[/yellow] [bold green]с защитой[/bold green] [green]{selected_item['defence']}[/green]",
                        border_style="bright_blue"
                    )
                )
                UI.show_item_in_layoutitem(selected_item)
                return {'armor_defence': selected_item['defence']}
            elif selected_item['type'] == 'ring' :
                console.print(
                    Panel(
                        f"[bold green]Вы экипировали кольцо[/bold green] [yellow]{selected_item['name']}[/yellow] [bold green]с регенерацией[/bold green] [green]{selected_item['heal']}[/green]",
                        border_style="bright_blue"
                    )

                )
                UI.show_item_in_layoutitem(selected_item)
                return {'ring_regen': selected_item['heal']}
        else:
            console.print(Panel("[red]Некорректный выбор[/red]", border_style="red"))

    def sell_item(self): 
        """
        Продажа предмета.
        Создаёт таблицу со всеми предметами и позволяет игроку выбрать предмет для продажи.
        Возвращает количество монет за проданный предмет.
        """

        if len(self.inventory)<=0:
            UI.add_message_to_main("У вас нету предметов!")
            return None
        
        console = Console()
        console.print(Panel("[bold cyan]Выберите предмет, который вы продадите[/bold cyan]", border_style="bright_blue"))

        valid_indexes = [0]

        # Создаём таблицу
        table = Table(show_header=True, header_style="bold magenta") 

        # Добавляем колонки
        table.add_column("№", style="bold cyan", width=3, justify="center")
        table.add_column("Название", style="bold yellow")
        table.add_column("Тип", style="green")
        table.add_column("Параметр", style="bold blue")
        table.add_column("Цена", style="bold yellow")

        for index, item in enumerate(self.inventory, start=1): # Добавляем предметы по очереди
            if item['type'] == 'sword': # Мечи
                table.add_row(
                    str(index),
                    f"[white]{item['name']}[/white]",
                    "[yellow]Меч[/yellow]",
                    f"[red]Урон {item['damage']}[/red]",
                    f"[bold gold1]{item['cost']} монет[/bold gold1]"
                ) # Добавляем строчу
                valid_indexes.append(index)
            elif item['type'] == 'armor': # Броня
                table.add_row(
                    str(index),
                    f"[white]{item['name']}[/white]",
                    "[blue]Броня[/blue]",
                    f"[green]Защита {item['defence']}[/green]",
                    f"[bold gold1]{item['cost']} монет[/bold gold1]"
                ) # Добавляем строчу
                valid_indexes.append(index)
            elif item['type'] == 'ring' :
                table.add_row(
                    str(index),
                    f"[white]{item['name']}[/white]",
                    "[red]Кольцо[/red]",
                    f"[bright_red]Регенерация {item['heal']}[/bright_red]",
                    f"[bold gold1]{item['cost']} монет[/bold gold1]"
                ) # Добавляем строчку
                valid_indexes.append(index)
        UI.show_table_in_main(table)

        ans = get_valid_int_input(
            "[bold green]Введите номер предмета:[/bold green] ",
            valid_indexes
        ) - 1 # Игрок выбирает предмет
        
        if ans == -1 :
            return 0

        if 0 <= ans < len(self.inventory):
            selected_item = self.inventory[ans]
            coins = selected_item['cost']
            self.mass -= selected_item['weight']
            self.inventory.pop(ans)
            if selected_item['type'] == 'sword':
                UI.add_message_to_main(
                        f"[bold green]Вы продали меч[/bold green] [yellow]{selected_item['name']}[/yellow] [bold green]за[/bold green] [bold gold1]{coins} монет[/bold gold1]"
                    )
            elif selected_item['type'] == 'armor':
                UI.add_message_to_main(
                        f"[bold green]Вы продали броню[/bold green] [yellow]{selected_item['name']}[/yellow] [bold green]за[/bold green] [bold gold1]{coins} монет[/bold gold1]"
                    )
            elif selected_item['type'] == 'ring':
                UI.add_message_to_main(
                        f"[bold green]Вы продали кольцо[/bold green] [yellow]{selected_item['name']}[/yellow] [bold green]за[/bold green] [bold gold1]{coins} монет[/bold gold1]"
                    )
            return coins # Возвращаем количество денег, которых надо прибавить
        else:
            console.print(Panel("[red]Некорректный выбор[/red]", border_style="red"))


    def drop_item_sword(self, bosses_killed): 
        """
        Добавляет меч в инвентарь в зависимости от количества убитых боссов.
        Стандарт
        Ничего не возвращаем
        """

        sword = Sword(bosses_killed) # Создаём предмет
        self.mass += sword.weight
        UI.add_message_to_main("У добавился предмет! Посмотрите его в инвентаре")
        # Создаём панель с параметрами предмета
        self.inventory.append(sword.create())
 

    def drop_item_armor(self): 
        """
        Добавляет броню в инвентарь.
        Стандарт
        Ничего не возвращаем
        """

        armor = Armor() # Создаём предмет
        self.mass += armor.weight
        UI.add_message_to_main("У добавился предмет! Посмотрите его в инвентаре")
        # Создаём панель с параметрами предмета
        self.inventory.append(armor.create())

    def drop_item_ring(self):
        """
        Добавляет кольцо в инвентарь
        Стандарт
        Ничего не возвращаем
        """

        ring = Ring() # Создаём предмет
        self.mass += ring.weight
        UI.add_message_to_main("У добавился предмет! Посмотрите его в инвентаре")
        # Создаём панель с параметрами предмета
        self.inventory.append(ring.create())