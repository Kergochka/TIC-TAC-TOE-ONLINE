from __future__ import annotations
import random
import socket
import threading
import struct
import string
from typing import Callable, Literal, Self, TYPE_CHECKING
from .functionsForButtons import (
    create_game_board_host,
    update_board_from_network_host, 
    update_board_from_network_client, 
    create_game_board_client
)

if TYPE_CHECKING:
    from main_module import RootClass

class ClientSocketManager:
    def __init__(self, sock: socket.socket | Literal[-1]=None, if_error_path: Callable | None | Literal[-1]=None) -> None:
        self._can_do = False if sock == -1 and if_error_path == -1 else True

        if not self._can_do:
            return

        if if_error_path is None or not callable(if_error_path):
            raise TypeError(f'Incorrect type if_error_path: {type(if_error_path).__name__}. Expected a function.')
            
        self._if_error_path = if_error_path
        self._buffer = bytearray()

        if sock is None or not isinstance(sock, socket.socket):
            self._if_error_path(f"Ожидался объект типа socket.socket, но получен {type(sock).__name__}")
            return

        self._sock = sock

    def set_config(self, sock: socket.socket, if_error_path: Callable) -> None:
        if not callable(if_error_path):
            raise TypeError(f'Incorrect type if_error_path: {type(if_error_path).__name__}. Expected a function.')
            
        self._if_error_path = if_error_path
        self._buffer = bytearray()
        if not isinstance(sock, socket.socket):
            self._if_error_path(f"Ожидался объект типа socket.socket, но получен {type(sock).__name__}")
            return
        self._sock = sock
        self._can_do = True

    def recv(self, max_bytes: int = 4096) -> bytes:
        if not self._can_do:
            raise RuntimeError("SocketReader is not configured. Run config() first.")

        if max_bytes <= 0:
            self._if_error_path(f"Критическая ошибка: недопустимый размер буфера max_bytes = {max_bytes}")
            return b""

        while b'\n' not in self._buffer:
            try:
                data = self._sock.recv(max_bytes)
                if not data:
                    break
                self._buffer.extend(data)
            except Exception as e:
                self._if_error_path(f"Ошибка при чтении из сокета: {e}")
                return b""

        if b'\n' in self._buffer:
            idx = self._buffer.index(b'\n')
            packet = bytes(self._buffer[:idx])
            del self._buffer[:idx + 1]
            return packet

        if self._buffer:
            packet = bytes(self._buffer)
            self._buffer.clear()
            return packet

        return b""

    def send(self, data: bytes) -> None:
        if not self._can_do:
            raise RuntimeError("SocketReader is not configured. Run config() first.")
        try:
            self._sock.sendall(data + b'\n')
        except Exception as e:
            self._if_error_path(f"Ошибка при отправке в сокет: {e}")

class ServerSocketManager:
    def __init__(
        self, 
        socket_server: socket.socket | Literal[-1] = None, 
        if_error_path: Callable | None | Literal[-1] = None, 
        socket_client: socket.socket | Literal[-1] = None,
        ip_client: tuple | None | Literal[-1] = None
    ) -> None:
        
        if socket_server == -1 and if_error_path == -1 and socket_client == -1 and ip_client == -1:
            self._can_do = False
            return

        if if_error_path is None or not callable(if_error_path):
            raise TypeError(f'Incorrect type if_error_path: {type(if_error_path).__name__}. Expected a function.')
            
        self._if_error_path = if_error_path
        self._buffer = bytearray()

        if socket_server is None or not isinstance(socket_server, socket.socket):
            self._if_error_path(f"Ожидался объект типа socket.socket для сервера, но получен {type(socket_server).__name__}")
            return

        if socket_client is None or not isinstance(socket_client, socket.socket):
            self._if_error_path(f"Ожидался объект типа socket.socket для клиента, но получен {type(socket_client).__name__}")
            return

        if ip_client is None or not isinstance(ip_client, tuple):
            self._if_error_path(f"Ожидались метаданные клиента типа tuple, но получен {type(ip_client).__name__}")
            return

        self._sock_server = socket_server
        self._sock_client = socket_client
        self._ip_client = ip_client
        self._can_do = True

    def set_config(
        self, 
        socket_server: socket.socket | None = None, 
        if_error_path: Callable | None = None, 
        socket_client: socket.socket | None = None,
        ip_client: tuple | None = None
    ) -> None:
        
        if if_error_path is None or not callable(if_error_path):
            raise TypeError(f'Incorrect type if_error_path: {type(if_error_path).__name__}. Expected a function.')
            
        self._if_error_path = if_error_path
        self._buffer = bytearray()

        if socket_server is None or not isinstance(socket_server, socket.socket):
            self._if_error_path(f"Ожидался объект типа socket.socket для сервера, но получен {type(socket_server).__name__}")
            return

        if socket_client is None or not isinstance(socket_client, socket.socket):
            self._if_error_path(f"Ожидался объект типа socket.socket для клиента, но получен {type(socket_client).__name__}")
            return

        if ip_client is None or not isinstance(ip_client, tuple):
            self._if_error_path(f"Ожидались метаданные клиента типа tuple, но получен {type(ip_client).__name__}")
            return
            
        self._sock_server = socket_server
        self._sock_client = socket_client
        self._ip_client = ip_client
        self._can_do = True

    def recv(self, max_bytes: int = 4096) -> bytes:
        if not self._can_do:
            raise RuntimeError("ServerSocketManager is not configured. Run set_config() first.")

        if max_bytes <= 0:
            self._if_error_path(f"Критическая ошибка: недопустимый размер буфера max_bytes = {max_bytes}")
            return b""

        is_connected = True
        while b'\n' not in self._buffer and is_connected:
            try:
                data = self._sock_client.recv(max_bytes)
                if not data:
                    is_connected = False  
                    break                 
                self._buffer.extend(data)
            except Exception as e:
                self._if_error_path(f"Ошибка при чтении из сокета сервера (клиентского): {e}")
                return b""

        if b'\n' in self._buffer:
            idx = self._buffer.index(b'\n')
            packet = bytes(self._buffer[:idx])
            del self._buffer[:idx + 1]
            return packet

        if self._buffer:
            packet = bytes(self._buffer)
            self._buffer.clear()
            return packet

        return b""

    def send(self, data: bytes) -> None:
        if not self._can_do:
            raise RuntimeError("ServerSocketManager is not configured. Run set_config() first.")
        try:
            self._sock_client.sendall(data + b'\n')
        except Exception as e:
            self._if_error_path(f"Ошибка при отправке в сокет сервера (клиентскому): {e}")

class BaseSocketSystem:
    __singleton_instance__ = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls is BaseSocketSystem:
            raise TypeError('Нельзя создавать экземпляр класса BaseSocketSystem напрямую')

        if cls.__singleton_instance__ is None:
            obj = super().__new__(cls)
            cls.__singleton_instance__ = obj
            return obj
        return cls.__singleton_instance__
    
    def __init__(self, rootmanager: RootClass) -> None:
        self.rootmanager = rootmanager
        
        self._NEXT = b'F1'  
        self._BYE = b'F0'

        self._CH1 = b'C1'
        self._CH2 = b'C2'

        self._datagame = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self._datagame_bytes = struct.pack('10s', b'D000000000') 
        self.whoiam: None | Literal['1', '2'] = None 
        self.my_turn: bool = False


        self._validate_exceptions = ({'F': ('Incorrect flag', 'Missing flag'), 'D': ('Data size is incorrect for the flag', 'Incorrect data', 'Missing data', 'Data size is incorrect')})

    def update_databytes(self) -> None:
        data_str = ''.join(self._datagame)
        packet_str = 'D' + data_str
        self._datagame_bytes = packet_str.encode('utf-8')

    def check_validate_data(self, data: bytes) -> tuple[str, Literal['F', 'D', 'C']] | Literal[b'']:
        if not isinstance(data, bytes):
            self.rootmanager.emergency_return_to_main_window('Проверка данных не прошла успешно: data не является экземпляром bytes')
            return b''

        unpack_data: str = data.decode('utf-8')

        if not unpack_data:
            self.rootmanager.emergency_return_to_main_window(self._validate_exceptions[0].get('F')[1] + '; ' + self._validate_exceptions[0].get('D')[2])
            return b''

        if len(data) < 2:
            self.rootmanager.emergency_return_to_main_window(self._validate_exceptions[0].get('D')[3])
            return b''
        flag = unpack_data[0].upper()
        if flag not in string.ascii_uppercase:
            self.rootmanager.emergency_return_to_main_window(self._validate_exceptions[0].get('F')[1])
            return b''

        if flag not in ['F', 'D', 'C']:
            self.rootmanager.emergency_return_to_main_window(self._validate_exceptions[0].get('F')[0])
            return b''

        if flag == 'F':
            if len(unpack_data) != 2:
                self.rootmanager.emergency_return_to_main_window(self._validate_exceptions[0].get('D')[0])
                return b''
            if data == self._BYE:
                self.rootmanager.emergency_return_to_main_window()
                return b''
            return (unpack_data, 'F')

        if flag == 'C':
            if len(unpack_data) != 2:
                self.rootmanager.emergency_return_to_main_window(self._validate_exceptions[0].get('D')[0])
                return b''
            if data == self._BYE:
                self.rootmanager.emergency_return_to_main_window()
                return b''
            return (unpack_data, 'C')

        if len(data) != 10:
            self.rootmanager.emergency_return_to_main_window(self._validate_exceptions[0].get('D')[0])
            return b''

        for i in unpack_data[1:]:
            if i not in ['0', '1', '2']:
                self.rootmanager.emergency_return_to_main_window(self._validate_exceptions[0].get('D')[1])
                return b''
        return (unpack_data, 'D')
     
class ClientSocketSystem(BaseSocketSystem):
    def __init__(self, rootmanager: RootClass, getsocket: str) -> None:
        super().__init__(rootmanager=rootmanager)
        self._ip, port_str = getsocket.split(':')
        self._port = int(port_str)
        self._client_socket_manager = ClientSocketManager(-1, -1)
        self._init_client_server()
 
    def close(self) -> None:
        self._socket_client.close()
        print('Поток клиента завершен')

    def __init_client_server(self, stop_event: threading.Event) -> None:
            self._socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client_socket_manager.set_config(sock=self._socket_client, if_error_path=self.rootmanager.emergency_return_to_main_window)
            
            try:
                # Устанавливаем таймаут подключения в 5 секунд, чтобы клиент не зависал бесконечно
                self._socket_client.settimeout(5.0)
                self._socket_client.connect((self._ip, self._port))
                # Возвращаем сокет в стандартный блокирующий режим для дальнейшей игры
                self._socket_client.settimeout(None)
            except (socket.error, OSError):
                # Если хост не запущен или IP неверный — возвращаем в меню с ошибкой
                self.rootmanager.emergency_return_to_main_window("Игра не найдена")
                self._socket_client.close()
                return

            self.rootmanager.root.after(0, self.rootmanager.mainwidgets.wait_host)

            self._client_socket_manager.send(self._NEXT)

            data = self._client_socket_manager.recv()
            if not data:
                self.close()
                return

            unpack_data = self.check_validate_data(data)
            if not unpack_data:
                self.close()
                return

            if data != self._NEXT:
                self.close()
                return

            data = self._client_socket_manager.recv()
            if not data:
                self.close()
                return

            unpack_data = self.check_validate_data(data)
            if not unpack_data:
                self.close()
                return

            if unpack_data[0] not in ['C1', 'C2']:
                self.close()
                return

            if unpack_data[0] == 'C1':
                self.whoiam = '1'
                self.my_turn = False
            else:
                self.whoiam = '2'
                self.my_turn = True

            self.start_game_event = threading.Event()
            self.start_game_event.clear()

            self.rootmanager.root.after(0, lambda: create_game_board_client(self.rootmanager.mainwidgets))

            while not stop_event.is_set():
                if self.my_turn:
                    self.start_game_event.wait()
                    self.start_game_event.clear()
                    
                    self.update_databytes()
                    self._client_socket_manager.send(self._datagame_bytes)

                if not self.my_turn:
                    data = self._client_socket_manager.recv()
                    if not data:
                        self.rootmanager.emergency_return_to_main_window("Соединение с хостом потеряно")
                        break
                        
                    unpack_data = self.check_validate_data(data)
                    if not unpack_data:
                        break

                    if unpack_data and unpack_data != b'':
                        self.my_turn = True
                        self.rootmanager.root.after(
                            0, 
                            update_board_from_network_client, 
                            self.rootmanager.mainwidgets, 
                            unpack_data
                        )

            self.close()

    def _init_client_server(self) -> None:
        self._client_server_thread = threading.Thread(target=self.__init_client_server, daemon=True)
        self._id_thread = self.rootmanager.create_thread('_client_server_thread', self._client_server_thread)
        self._client_server_thread.start()

class HostSocketSystem(BaseSocketSystem):
    def close(self) -> None:
        self._socket_server.close()
        print('Поток сервера завершен')

    def __init__(self, rootmanager: RootClass, port: int) -> None:
        super().__init__(rootmanager=rootmanager)
        self._port = port
        self._server_socket_manager = ServerSocketManager(-1, -1, -1, -1)
        self._init_server()

    def _init_server(self) -> None:
        self._server_thread = threading.Thread(target=self.__first_connect, daemon=True)
        self._id_thread = self.rootmanager.create_thread('_server_thread', self._server_thread)
        self.start_game_event = threading.Event()
        self.my_turn = True
        self._server_thread.start()

    def __first_connect(self, stop_event: threading.Event) -> None:
        self._socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket_server.bind(('0.0.0.0', self._port))
        self._socket_server.listen(1)

        self._client_socket, self._address_client = self._socket_server.accept()
        self._server_socket_manager.set_config(self._socket_server, self.rootmanager.emergency_return_to_main_window, self._client_socket, self._address_client)

        self.rootmanager.root.after(0, self.rootmanager.mainwidgets.change_window_after_connect_player_for_host)

        data = self._server_socket_manager.recv()

        if not data:
            self.rootmanager.emergency_return_to_main_window("Игрок отключился")
            self.close()
            return

        unpack_data = self.check_validate_data(data)
        if not unpack_data:
            self.close()
            return
        
        if data != self._NEXT:
            self.close()
            return
            
        self._stop_event = stop_event
        self._server_socket_manager.send(self._NEXT)
        self.start_game_event.wait()
        self.game_system()

    def game_system(self) -> None:
        self.whoiam = '1' if random.randint(1, 2) == 1 else '2'
        self.my_turn = True if self.whoiam == '2' else False
        
        self._server_socket_manager.send(self._CH1 if self.whoiam == '2' else self._CH2)
        self.rootmanager.root.after(0, lambda: create_game_board_host(self.rootmanager.mainwidgets))
        self.start_game_event.clear()

        while not self._stop_event.is_set():
            if self.my_turn:
                self.start_game_event.wait()
                self.start_game_event.clear()
                
                self.update_databytes()
                self._server_socket_manager.send(self._datagame_bytes)

            if not self.my_turn:
                data = self._server_socket_manager.recv()
                if not data:
                    self.rootmanager.emergency_return_to_main_window("Игрок отключился")
                    break
                    
                unpack_data = self.check_validate_data(data)
                if not unpack_data:
                    break
                
                if unpack_data and unpack_data != b'':
                    self.my_turn = True
                    self.rootmanager.root.after(
                        0, 
                        update_board_from_network_host, 
                        self.rootmanager.mainwidgets, 
                        unpack_data
                    )

        self.close()

class NetManager:
    def set_config(self, server_or_client: Literal[0, 1]=-1, port: int=-1, getsocket: str = '') -> None:
        if not isinstance(server_or_client, int) or server_or_client not in [0, 1]:
            self.rootmanager.emergency_return_to_main_window(f'Были даны некорректные данные в NetManager: флаг server_or_client не является классом int или не Literal[0, 1].')

        if server_or_client == 0:
            self._flag = ('server', 0)
            if port == -1:
                self.rootmanager.emergency_return_to_main_window(self.rootmanager.PROGRAMMER_ERROR)
                raise AttributeError('Port must be specified')
            self.type_socket: Literal['client', 'server'] = 'server'
            self.servermanager = HostSocketSystem(self.rootmanager, port)
            return   

        if not getsocket:
            self.rootmanager.emergency_return_to_main_window(self.rootmanager.PROGRAMMER_ERROR)
            raise AttributeError('Socket Must Be Specified')

        self.type_socket: Literal['client', 'server'] = 'client'
        self.clientmanager = ClientSocketSystem(rootmanager=self.rootmanager, getsocket=getsocket)

    def __init__(self, *, rootmanager: RootClass=None) -> None:
        if rootmanager.__class__.__name__ != 'RootClass' or rootmanager is None:
            self.rootmanager.emergency_return_to_main_window(self.rootmanager.PROGRAMMER_ERROR)
            raise TypeError('Аргумент window должен быть объектом класса RootClass')

        self.rootmanager = rootmanager
