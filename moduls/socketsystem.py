from __future__ import annotations
from typing import Literal, Self
from exceptions import ServerInstanceAlreadyExists, PortMustBeSpecified, SocketMustBeSpecifed
from typing import TYPE_CHECKING
import socket
import threading

if TYPE_CHECKING:
    from main_module import RootWindow


class ClietnSocketSystem():
    def connect_client(self) -> None:
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.connect((self._ip, self._port))
        self.window.root.after(0, self.window._mainwidgets.wait_host)
        

    def connect_client_theard(self) -> None:
        self.server_thread = threading.Thread(target=self.connect_client, daemon=True)
        self.server_thread.start()


    def __init__(self, window: RootWindow, getsocket: str) -> None:
        self.window = window
        self._socket = getsocket
        self._ip = self._socket.split(':')[0]
        self._port = int(self._socket.split(':')[1])
        self.connect_ending = False
        self.connect_client_theard()

class HostSocketSystem():
    def start_theard_server(self) -> None:
        self.server_thread = threading.Thread(target=self.init_server, daemon=True)
        self.server_thread.start()

    def init_server(self) -> None:
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind(('0.0.0.0', self._port))
        self.socket_server.listen(1)
        self.connect_ending = False
        self.client, self.address_client = self.socket_server.accept()
        self.window.root.after(0, self.window._mainwidgets.change_window_after_connect_player_for_host)


    def __init__(self, window: RootWindow, port: int) -> None:
        self.window = window
        self._port = port
        self.start_theard_server()



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


    


    def check_socket(self) -> None: #$ TODO
        ...


    def __init__(self, window: RootWindow, server_or_client: Literal[0, 1], port: int=-1, getsocket: str='') -> None:

        if server_or_client == 0:
            if port == -1:
                raise PortMustBeSpecified('Port must be specified')
            self.GameCreated = HostSocketSystem(window, port)
            return

        if not getsocket:
            raise SocketMustBeSpecifed('Socket Must Be Specified')

        self.GameConnected = ClietnSocketSystem(window=window, getsocket=getsocket)