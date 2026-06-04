import tkinter as tk
from typing import Self
from _widgets import _CreateMainWidgets
from socketsystem import SystemConnection
from exceptions import RootWindowObjectAlreadyExistsException

class RootWindow():
    __singleton_window__: None | Self = None

    def runApp(self) -> None:
        self.root.mainloop()

    def create_socketServer(self, port: int) -> None:
        self.socketserver = SystemConnection(self, server_or_client=0, port=port)

    def start_game_server(self) -> None: #$ TODO
        print('Игра началась!')

    def create_socketClient(self, SocketIPPORT: str) -> None:
        if not isinstance(SocketIPPORT, str):
            raise TypeError('Сокет(IP:PORT) должен быть строкой.')
        self.socketserver = SystemConnection(self, server_or_client=1, takesocket=SocketIPPORT)

    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__singleton_window__ is None:
            obj = super().__new__(cls)
            cls.__singleton_window__ = obj
            return obj

        raise RootWindowObjectAlreadyExistsException('Объект RootWindow уже был создан.')
    
    def __init__(self, root_tk: tk.Tk | None = None) -> None:
        self.root = root_tk if isinstance(root_tk, tk.Tk) else tk.Tk()
        self._mainwidgets = _CreateMainWidgets(self)
        self.root.resizable(False, False)

if __name__ == '__main__':
    # test
    check_obj = RootWindow()
    check_obj.runApp()