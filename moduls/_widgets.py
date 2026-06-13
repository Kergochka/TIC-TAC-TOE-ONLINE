from __future__ import annotations
from typing import TYPE_CHECKING
from .functionsForButtons import choice_hostmenuBTN_func, choice_clientmenuBTN_func, wait_host_func
import tkinter as tk

if TYPE_CHECKING:
    from main_module import RootClass



class WidgetManager():

    def __init__(self, object: RootClass) -> None:
        from moduls.main_module import RootClass
        if object.__class__.__name__ != 'RootClass':
            self.rootmanager.emergency_return_to_main_window(self.rootmanager.PROGRAMMER_ERROR)
            raise TypeError("Полученный объект в WidgetManager должен быть объектом RootClass")

        self.rootmanager = object
        self.root = self.rootmanager.root
        self.widgets = {}

        self.root.geometry('600x600')
        self.root.title('Tic-tac-toe')
        self.set_startmain_menu()

    def destroy_wigdets(self) -> None:
        for namewidget in list(self.widgets.keys()):
            self.widgets[namewidget].destroy()
            del self.widgets[namewidget]


    def set_startmain_menu(self) -> None:
        self.destroy_wigdets()
        LabelNameOfGame = tk.Label(self.root, text='TIC-TAC-TOE', fg='#522525', font=('Trebuchet MS', 20), width=11, height=0)
        LabelNameOfGame.pack(pady=(25, 0))
        start_btn = tk.Button(self.root, text='start', width=8, height=2, font=('Trebuchet MS', 12), command=lambda: (self.choice_role_menu()))
        start_btn.pack(pady=(150, 0))
        self.widgets['LabelNameOfGame'] = LabelNameOfGame
        self.widgets['start_btn'] = start_btn

    def choice_role_menu(self) -> None:
            self.destroy_wigdets()
            
            client_btn = tk.Button(self.root, text='Connect', width=8, height=2, font=('Trebuchet MS', 12), command=lambda: choice_clientmenuBTN_func(widgetmanager=self))
            host_btn = tk.Button(self.root, text='Hosting', width=8, height=2, font=('Trebuchet MS', 12), command=lambda: choice_hostmenuBTN_func(widgetmanager=self))

            back_btn = tk.Button(self.root, text='Back', width=8, height=2, font=('Trebuchet MS', 12), command=self.set_startmain_menu)
            
            client_btn.pack(pady=(150, 0))
            host_btn.pack(pady=(10, 0))
            back_btn.pack(pady=(10, 0))
            
            self.widgets['client_btn'] = client_btn
            self.widgets['host_btn'] = host_btn
            self.widgets['back_btn'] = back_btn

    def wait_host(self) -> None:
        wait_host_func(widgetmanager=self)

    def set_choice_menu_if_error(self, message: str) -> None:
                self.set_startmain_menu()
                if message:
                    canvas = tk.Canvas(self.root, width=250, height=180, bg='#3c3e42', highlightthickness=0)
                    canvas.pack(pady=(110, 0))    
                    font_error = ('Trebuchet MS', 18, 'bold')
                    font_msg = ('Trebuchet MS', 13, 'bold')    

                    canvas.create_polygon(35, 13, 15, 43, 55, 43, fill='#ffd700', outline='black', width=2)
                    canvas.create_text(35, 29, text="!", fill='black', font=('Trebuchet MS', 16, 'bold'))
                    
                    canvas.create_text(125, 39, text="ERROR", fill='black', font=font_error, width=200, justify='center')
                    canvas.create_text(127, 37, text="ERROR", fill='black', font=font_error, width=200, justify='center')
                    canvas.create_text(126, 38, text="ERROR", fill='black', font=font_error, width=200, justify='center')
                    canvas.create_text(126, 35, text="ERROR", fill='#ff3333', font=font_error, width=200, justify='center')   
                    
                    canvas.create_text(125, 112, text=message, fill='black', font=font_msg, width=200, justify='center')
                    canvas.create_text(127, 112, text=message, fill='black', font=font_msg, width=200, justify='center')
                    canvas.create_text(126, 113, text=message, fill='black', font=font_msg, width=200, justify='center')
                    canvas.create_text(126, 110, text=message, fill='white', font=font_msg, width=200, justify='center')
                    self.widgets['label_cause'] = canvas


    def change_window_after_connect_player_for_host(self) -> None:
        self.widgets['goto_gamebtn'].config(state='active')
        self.widgets['players_label'].config(text='Players: 2/2')
