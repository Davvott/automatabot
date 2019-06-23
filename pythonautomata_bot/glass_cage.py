"""Automata Bot Feeding Ground"""
from tkinter import *
from automatabot.pythonautomata_bot.automata_bot import AutomataBot
from automatabot.pythonautomata_bot.automata_grid import MainApp


def main():
    automatabot = AutomataBot()
    print(automatabot)

    root = Tk()
    root.title('AutomataBot')
    MainApp(root, bot=automatabot).pack(side="top", fill="both", expand=True, padx=5, pady=5)
    root.mainloop()


main()
