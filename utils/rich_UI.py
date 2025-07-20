from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from rich.table import Table

class UIClass ():
    def __init__(self):
        self.layout = self.make_layout()
        self.messages = []
        self.MAX_LINES_MAIN = 56
        self.console = Console()

    def make_layout(self) :
        layout = Layout()
        layout.split_column(
            Layout(name="BattleBoss"),
            Layout(name="play_area")
        )
        layout["BattleBoss"].size = 3
        layout["BattleBoss"].update(
            Panel(Align.center("BattleBoss"))
        )
        layout["play_area"].split_row(
            Layout(name="main"),
            Layout(name="UI")
        )
        layout["main"].ratio = 3
        layout["UI"].split_column(
            Layout(name="stats"),
            Layout(name="control"),
            Layout(name="item")
        )
        layout["stats"].size = 5
        layout["control"].size = 7
        layout["item"].size = 10
        return layout

    def add_message_to_main(self, new_msg: str):
        self.messages.append(new_msg)

        while len(self.messages) >= self.MAX_LINES_MAIN:
            self.messages.pop(0)

        content = "\n".join(self.messages)
        self.layout["main"].update(Panel(content))

        self.console.print(self.layout)

    def show_table_in_main(self, table: Table) :
        self.layout["main"].update(Panel(table))

        self.console.print(self.layout)

    def show_item_in_layoutitem (self, item) :
        if item["type"] == "sword" :
            self.layout["item"].update(Panel(f"Тип предмета - {item["type"]}\n"
                                    f"Название - {item["name"]}\n"
                                    f"{item["description"]}\n"
                                    f"Вес - {item["weight"]}\n"
                                    f"Урон - {item["damage"]}\n"
                                    f"Цена - {item["cost"]}", title="Текущий Предмет"))
        if item["type"] == "armor" :
             self.layout["item"].update(Panel(f"Тип предмета - {item["type"]}\n"
                                    f"Название - {item["name"]}\n"
                                    f"{item["description"]}\n"
                                    f"Вес - {item["weight"]}\n"
                                    f"Защита - {item["defence"]} %\n"
                                    f"Цена - {item["cost"]}", title="Текущий Предмет"))
        if item["type"] == "ring" :
            self.layout["item"].update(Panel(f"Тип предмета - {item["type"]}\n"
                                    f"Название - {item["name"]}\n"
                                    f"{item["description"]}\n"
                                    f"Вес - {item["weight"]}\n"
                                    f"Регенирация - {item["heal"]}\n"
                                    f"Цена - {item["cost"]}", title="Текущий Предмет"))
            
        self.console.print(self.layout)
    
    def show_control(self):
        self.layout["control"].update(Panel("[bright_blue]1[/bright_blue] чтобы атаковать.\n[bright_blue]2[/bright_blue] чтобы восполнить здоровье.\n[bright_blue]3[/bright_blue] чтобы восполнить магию.\n[bright_blue]4[/bright_blue] чтобы открыть инвентарь.\n[bright_blue]5[/bright_blue] чтобы продать предмет.\n[bright_blue]0[/bright_blue] чтобы пропустить ход.", title="Управление"))

        self.console.print(self.layout)

    def update_stats(self, player, boss):
        self.layout["stats"].update(Panel(
            f"Ваше здоровье [blue]{player.hp}[/blue]. Ваша магия  [blue]{player.magic}[/blue]. Ваши деньги  [blue]{player.money}[/blue]\n"
            f"Здоровье босса [red]{boss.hp}[/red]. Магия босса [red]{boss.magic}[/red].\n" 
            f"Сейчас {player.rounds} раунд", title="Статистика"))
        
        self.console.print(self.layout)

UI = UIClass()