from __future__ import annotations
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _widgets import _CreateMainWidgets

def startgamefunc_client(window: _CreateMainWidgets, takesocket: str) -> None:
    window._widgets['startgamebtn'].config(state='disabled')
    window.window.create_socketClient(takesocket)

def startgamefunc_host(window: _CreateMainWidgets, port: str) -> None:

    if not isinstance(port, int):
        raise TypeError('Порт должен быть числом.')

    window.destroy_wigdets()
    goto_gamebtn = tk.Button(window.root, text='play', font=('Trebuchet MS', 12), command=lambda: window.window.start_game_server(), state='disabled')
    goto_gamebtn.pack(pady=(150, 0))
    players_label = tk.Label(window.root, text='Players: 1/2', font=('Trebuchet MS', 12))
    players_label.pack()
    window._widgets['goto_gamebtn'] = goto_gamebtn
    window._widgets['players_label'] = players_label

    window.window.create_socketServer(int(port))

def choice_clientmenuBTN_func(window: _CreateMainWidgets) -> None:
    entry_ip = tk.Entry(window.root, font=('Trebuchet MS', 12), width=15)
    entry_ip.insert(0, '127.0.0.1:55556')
    startgamebtn = tk.Button(window.root, text='Start game', width=8, height=2, font=('Trebuchet MS', 12), command=lambda: startgamefunc_client(window, ipget if (ipget := entry_ip.get()) != 'localhost' else '127.0.0.1:55556'))
    window.destroy_wigdets()
    startgamebtn.pack(pady=(175, 0))
    entry_ip.pack()
    window._widgets['entry_ip'] = entry_ip
    window._widgets['startgamebtn'] = startgamebtn

def choice_hostmenuBTN_func(window: _CreateMainWidgets) -> None:
    entry_port = tk.Entry(window.root, font=('Trebuchet MS', 14), width=15)
    setportbtn = tk.Button(window.root, text='Set port', font=('Trebuchet MS', 12), command=lambda: startgamefunc_host(window, portget if (portget := entry_port.get()) != 'Port' and portget else 55556))
    entry_port.insert(0, 'Port')
    window.destroy_wigdets()
    setportbtn.pack(pady=(150, 0))
    entry_port.pack()

    window._widgets['entry_port'] = entry_port
    window._widgets['setportbtn'] = setportbtn

def wait_host_func(window: _CreateMainWidgets) -> None:
    window.destroy_wigdets()
    label_wait = tk.Label(window.root, text='Waiting for the host..', font=('Trebuchet MS', 12))
    label_wait.pack(pady=(150, 0))
    window._widgets['label_wait'] = label_wait