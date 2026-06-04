from __future__ import annotations
from typing import TYPE_CHECKING
from functionsForButtons import choice_hostmenuBTN_func, choice_clientmenuBTN_func, wait_host_func
import tkinter as tk

if TYPE_CHECKING:
    from main_module import RootWindow

class _Widgets():
    def destroy_wigdets(self: _CreateMainWidgets) -> None:
        for namewidget, widget in self._widgets.items():
            widget: tk.Widget
            widget.destroy()
        self._widgets.clear()

    def set_startmain_menu(self: _CreateMainWidgets) -> None:
        label_NameStartGame = tk.Label(self.root, text='TIC-TAC-TOE', fg='#522525', font=('Trebuchet MS', 20), width=11, height=0)
        label_NameStartGame.pack(pady=(25, 0))
        start_btn = tk.Button(self.root, text='start', width=8, height=2, font=('Trebuchet MS', 12), command=lambda: (self.destroy_wigdets(), self.choice_role_menu()))
        start_btn.pack(pady=(150, 0))
        self._widgets['label_NameStartGame'] = label_NameStartGame
        self._widgets['start_btn'] = start_btn

    def choice_role_menu(self: _CreateMainWidgets) -> None:
        host_btn = tk.Button(self.root, text='Hosting', width=8, height=2, font=('Trebuchet MS', 12), command=lambda: choice_hostmenuBTN_func(window=self))
        client_btn = tk.Button(self.root, text='Connect', width=8, height=2, font=('Trebuchet MS', 12), command=lambda: choice_clientmenuBTN_func(window=self))
        client_btn.pack(pady=(150, 0))
        host_btn.pack(pady=(10, 0))
        self._widgets['client_btn'] = client_btn
        self._widgets['host_btn'] = host_btn

    def wait_host(self: _CreateMainWidgets) -> None:
        wait_host_func(window=self)
    
    def client_has_left(self: _CreateMainWidgets) -> None:
        self.destroy_wigdets()
        self.set_startmain_menu()

    def __init__(self: _CreateMainWidgets) -> None:
        self.set_startmain_menu()

class _CreateMainWidgets(_Widgets):

    def _init_widgets(self) -> None:
        self.root.geometry('600x600')
        self.root.title('tic-tac-toe')
        super().__init__()

    def __init__(self, object: RootWindow) -> None:

        if object.__class__.__name__ != 'RootWindow':
            raise TypeError("Полученный объект должен быть RootWindow для создания главных фреймов.")

        self.window = object
        self.root = self.window.root
        self._widgets = {}
        self._init_widgets()