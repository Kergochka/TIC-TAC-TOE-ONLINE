from __future__ import annotations
from typing import Literal, Self
from exceptions import ServerInstanceAlreadyExists
from typing import TYPE_CHECKING
import socket
import threading

if TYPE_CHECKING:
    from main_module import RootWindow


#$ TODO: Почини этот ужас pls(((





class SystemConnection():
    __singleton_instance__ = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__singleton_instance__ is None:
            obj = super().__new__(cls)
            cls.__singleton_instance__ = obj
            return obj
        raise ServerInstanceAlreadyExists('Server instance already is exists.')


    def init_client(self, _socket: str) -> None:
        pass


    def init_server(self) -> None:
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind(('0.0.0.0', self.port))
        self.socket_server.listen(1)
        self.connect_ending = False
        self.client, self.address_client = self.socket_server.accept()
        self.window._mainwidgets._widgets['goto_gamebtn'].config(state='active')
        self.window._mainwidgets._widgets['players_label'].config(text='Players: 2/2')



    
    def start_theard_server(self) -> None:
        self.server_thread = threading.Thread(target=self.init_server, daemon=True)
        self.server_thread.start()

    def check_socket(self) -> None: #$ TODO
        ...


    def connect_clt(self) -> None:
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.connect((self.ip, self.port))
        self.window._mainwidgets.wait_host()
        

    def connect_clt_thrd(self) -> None:
        self.server_thread = threading.Thread(target=self.connect_clt, daemon=True)
        self.server_thread.start()  

    def __init__(self, window: RootWindow, server_or_client: Literal[0, 1], port: int=-1, takesocket: str='') -> None:



        if server_or_client == 0:
            self._flag = ('server', 0)
            if port == -1:
                raise Exception() ## заглушка просто. Потом сделать кастомное
            self.port = port
            self.window = window
            self.start_theard_server()
            return
        self._flag = ('client', 1)

        if not takesocket:
            raise Exception() ## заглушка просто. Потом сделать кастомное
        self.takesocket = takesocket
        self.ip = self.takesocket.split(':')[0]
        self.port = int(self.takesocket.split(':')[1])
        self.window = window
        self.connect_clt_thrd()
        