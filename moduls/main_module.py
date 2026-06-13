import sys
import tkinter as tk
import threading
from typing import Literal, Self, Callable
from .MyExceptions import RootWindowObjectAlreadyExistsException
from ._widgets import WidgetManager
from .socketsystem import NetManager

class RootClass():
    __singleton_Self_object__: None | Self = None

    def runApp(self) -> None:
        self.root.mainloop()


    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__singleton_Self_object__ is None:
            obj = super().__new__(cls)
            cls.__singleton_Self_object__ = obj
            return obj
        raise RootWindowObjectAlreadyExistsException('Объект RootWindow уже был создан.')

    def create_thread(self, name: str, thread: threading.Thread) -> int:
        if not isinstance(name, str):
            sys.exit(
                f"Аргумент name должен быть str, получен: {type(name).__name__}"
            )
        if not isinstance(thread, threading.Thread):
            sys.exit(
                f"Аргумент thread должен быть объектом threading.Thread, получен: {type(thread).__name__}"
            )
        current_id = self._id_of_threads
        stop_event = threading.Event()

        old_args = thread._args if thread._args is not None else ()
        thread._args = (stop_event, *old_args)
        
        self.threads[current_id] = [name, thread, stop_event]
        self._id_of_threads += 1

        return current_id

    def emergency_return_to_main_window(self, message: str='') -> None:
        if not isinstance(message, str):
            self.emergency_return_to_main_window(self.PROGRAMMER_ERROR)
            raise TypeError(f'message в emergency_return_to_main_window является {type(message)}. Не str.')

        for id in list(self.threads.keys()):
            self.change_flagdestroy_of_thread(id)
            
        self.root.after(0, lambda: self.mainwidgets.set_choice_menu_if_error(message=message if message else ''))

    def change_flagdestroy_of_thread(self, id: int | None=None) -> None:
        if id is None:
            sys.exit("id отсутствует")

        if not isinstance(id, int):
            sys.exit(f"id должно быть int, получили {type(id).__name__}")

        if id not in self.threads:
            print(f"Поток с ID {id} не найден. Возможно, он уже завершен.")
            return

        event: threading.Event = self.threads[id][2]
        event.set()
    
    def set_config_for_netmanager(self, server_or_client: Literal[0, 1]=-1, port: int=-1, getsocket: str = '') -> None:
        self.netmanager.set_config(server_or_client=server_or_client, port=port, getsocket=getsocket)

    def __init__(self, root_tk: tk.Tk | None = None) -> None:
        self.root = root_tk if isinstance(root_tk, tk.Tk) else tk.Tk()
        self.root.resizable(False, False)
        self._id_of_threads = 0
        self.threads = {} 
        self.PROGRAMMER_ERROR = "PROGRAMMER_ERROR"
        '''Структура threads:
            id: ['name_of_thread', threading.Thread, threading.Event]
        '''

        self.mainwidgets = WidgetManager(self)
        self.netmanager = NetManager(rootmanager=self)

