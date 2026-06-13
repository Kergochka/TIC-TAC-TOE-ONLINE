from __future__ import annotations
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._widgets import WidgetManager

def set_another_state_turn_for_everyone(widgetmanager: WidgetManager) -> None:

    net = widgetmanager.rootmanager.netmanager
    if hasattr(net, 'servermanager') and net.servermanager is not None:
        manager = net.servermanager
    elif hasattr(net, 'clientmanager') and net.clientmanager is not None:
        manager = net.clientmanager
    else:
        return

    widgetmanager.widgets['status_label'].config(
        text="Твой ход" if manager.my_turn else "ОЖИДАНИЕ ХОДА..."
    )


def check_game_state(widgetmanager: WidgetManager) -> bool:

    net = widgetmanager.rootmanager.netmanager
    if hasattr(net, 'servermanager') and net.servermanager is not None:
        manager = net.servermanager
    elif hasattr(net, 'clientmanager') and net.clientmanager is not None:
        manager = net.clientmanager
    else:
        return False

    datagame = manager._datagame
    whoiam = manager.whoiam  # '1' (нолик) или '2' (крестик)

    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    winner_symbol = None
    for combo in win_combinations:
        if datagame[combo[0]] != '0' and datagame[combo[0]] == datagame[combo[1]] == datagame[combo[2]]:
            winner_symbol = datagame[combo[0]]
            break

    if winner_symbol is not None:
        lock_all_cells(widgetmanager)
        if winner_symbol == whoiam:
            widgetmanager.widgets['status_label'].config(text="ВЫ ПОБЕДИЛИ!", fg="green")
        else:
            widgetmanager.widgets['status_label'].config(text="ВЫ ПРОИГРАЛИ!", fg="red")
            
        widgetmanager.root.after(2500, lambda: widgetmanager.rootmanager.emergency_return_to_main_window())
        return True

    if '0' not in datagame:
        lock_all_cells(widgetmanager)
        widgetmanager.widgets['status_label'].config(text="НИЧЬЯ!", fg="#ff8c00")
        widgetmanager.root.after(2500, lambda: widgetmanager.rootmanager.emergency_return_to_main_window())
        return True

    return False

def update_board_from_network_client(widgetmanager: WidgetManager, data_str: str) -> None:
    net = widgetmanager.rootmanager.netmanager
    client = net.clientmanager

    if isinstance(data_str, tuple):
        actual_str = data_str[0]
    else:
        actual_str = data_str

    clean_data = actual_str[1:] 
    client._datagame = list(clean_data)

    for i in range(9):
        cell_value = clean_data[i]
        btn = widgetmanager.widgets.get(f'cell_{i}')
        if btn:
            if cell_value == '1':
                btn.config(text='O', disabledforeground='blue', state='disabled')
            elif cell_value == '2':
                btn.config(text='X', disabledforeground='#522525', state='disabled')
            else:
                btn.config(text='', state='normal')


    if not check_game_state(widgetmanager):
        set_another_state_turn_for_everyone(widgetmanager)
        if client.my_turn:
            for i in range(9):
                if client._datagame[i] == '0':
                    btn = widgetmanager.widgets.get(f'cell_{i}')
                    if btn:
                        btn.config(state='normal')
        else:
            lock_all_cells(widgetmanager)

def on_cell_click_client(widgetmanager: WidgetManager, cell_id: int) -> None:
    net = widgetmanager.rootmanager.netmanager
    client = net.clientmanager

    if not client.my_turn:
        return

    client._datagame[cell_id] = client.whoiam 

    btn = widgetmanager.widgets.get(f'cell_{cell_id}')
    if btn:
        my_text = 'X' if client.whoiam == '2' else 'O'
        btn.config(
            text=my_text, 
            state='disabled', 
            disabledforeground='#522525' if my_text == 'X' else 'blue'
        )
        
    lock_all_cells(widgetmanager)
    client.my_turn = False
    
    if not check_game_state(widgetmanager):
        set_another_state_turn_for_everyone(widgetmanager)
        
    client.start_game_event.set()

def create_game_board_client(widgetmanager: WidgetManager) -> None:
    widgetmanager.destroy_wigdets()

    bg_color = widgetmanager.root.cget('bg')
    widgetmanager.root.config(bg=bg_color)
    board_size = 400
    
    net = widgetmanager.rootmanager.netmanager

    status_label = tk.Label(
        widgetmanager.root,
        text="Твой ход" if net.clientmanager.my_turn else "ОЖИДАНИЕ ХОДА...",
        font=('Trebuchet MS', 14, 'bold'),
        bg=bg_color,
        fg='#522525'
    )
    status_label.place(relx=0.5, rely=0.08, anchor='center')
    widgetmanager.widgets['status_label'] = status_label
        
    canvas = tk.Canvas(widgetmanager.root, bg=bg_color, highlightthickness=0, bd=0)
    canvas.place(relx=0.5, rely=0.5, anchor='center', width=board_size, height=board_size)
    widgetmanager.widgets['game_canvas'] = canvas 

    lines = [133, 267]
    main_color = '#522525'   
    shadow_color = '#250a0a' 
    light_color = '#ffffff'  
        
    for pos in lines:
        canvas.create_line(pos + 3, 10, pos + 3, board_size - 10, fill=light_color, width=2)
        canvas.create_line(pos - 3, 10, pos - 3, board_size - 10, fill=shadow_color, width=2)
        canvas.create_line(pos, 10, pos, board_size - 10, fill=main_color, width=6)

        canvas.create_line(10, pos + 3, board_size - 10, pos + 3, fill=light_color, width=2)
        canvas.create_line(10, pos - 3, board_size - 10, pos - 3, fill=shadow_color, width=2)
        canvas.create_line(10, pos, board_size - 10, pos, fill=main_color, width=6)

    cell_size = board_size // 3
        
    for row in range(3):
        for col in range(3):
            cell_id = row * 3 + col   
            btn = tk.Button(
                canvas,
                text='',
                font=('Trebuchet MS', 48, 'bold'),
                bg=bg_color,
                activebackground=bg_color,
                relief='flat',
                bd=0,
                highlightthickness=0,
                command=lambda c_id=cell_id: on_cell_click_client(widgetmanager, c_id)
            )
                
            x_center = col * cell_size + (cell_size // 2)
            y_center = row * cell_size + (cell_size // 2)
            
            canvas.create_window(x_center, y_center, window=btn, width=cell_size - 12, height=cell_size - 12)
            widgetmanager.widgets[f'cell_{cell_id}'] = btn
            
    if not net.clientmanager.my_turn:
        lock_all_cells(widgetmanager)

def start_game_widget_host(widgetmanager: WidgetManager) -> None:
    widgetmanager.widgets['goto_gamebtn'].config(state='disabled')
    widgetmanager.rootmanager.netmanager.servermanager.start_game_event.set()

def update_board_from_network_host(widgetmanager: WidgetManager, data_str: str) -> None:
    net = widgetmanager.rootmanager.netmanager
    server = net.servermanager

    if isinstance(data_str, tuple):
        actual_str = data_str[0]
    else:
        actual_str = data_str

    clean_data = actual_str[1:] 
    server._datagame = list(clean_data)
    
    for i in range(9):
        cell_value = clean_data[i]
        btn = widgetmanager.widgets.get(f'cell_{i}')
        
        if btn:
            if cell_value == '1':   
                btn.config(text='O', disabledforeground='blue', state='disabled')
            elif cell_value == '2': 
                btn.config(text='X', disabledforeground='#522525', state='disabled')
            else:                   
                btn.config(text='', state='normal')
                
    if not check_game_state(widgetmanager):
        set_another_state_turn_for_everyone(widgetmanager)
        if server.my_turn:
            for i in range(9):
                if server._datagame[i] == '0':
                    btn = widgetmanager.widgets.get(f'cell_{i}')
                    if btn:
                        btn.config(state='normal')
        else:
            lock_all_cells(widgetmanager)

def lock_all_cells(widgetmanager: WidgetManager) -> None:
    for i in range(9):
        btn = widgetmanager.widgets.get(f'cell_{i}')
        if btn:
            btn.config(state='disabled')

def on_cell_click_host(widgetmanager: WidgetManager, cell_id: int) -> None:
    net = widgetmanager.rootmanager.netmanager
    server = net.servermanager
    
    if not server.my_turn:
        return

    server._datagame[cell_id] = server.whoiam 

    btn = widgetmanager.widgets.get(f'cell_{cell_id}')
    if btn:
        my_text = 'X' if server.whoiam == '2' else 'O'
        btn.config(text=my_text, state='disabled', disabledforeground='#522525' if my_text == 'X' else 'blue')
        
    lock_all_cells(widgetmanager)
    server.my_turn = False
    
    if not check_game_state(widgetmanager):
        set_another_state_turn_for_everyone(widgetmanager)
        
    server.start_game_event.set()

def create_game_board_host(widgetmanager: WidgetManager) -> None:
    widgetmanager.destroy_wigdets()

    bg_color = widgetmanager.root.cget('bg')
    widgetmanager.root.config(bg=bg_color)
    board_size = 400
    
    net = widgetmanager.rootmanager.netmanager

    status_label = tk.Label(
        widgetmanager.root,
        text="Твой ход" if net.servermanager.my_turn else "ОЖИДАНИЕ ХОДА...",
        font=('Trebuchet MS', 14, 'bold'),
        bg=bg_color,
        fg='#522525'
    )
    status_label.place(relx=0.5, rely=0.08, anchor='center')
    widgetmanager.widgets['status_label'] = status_label
        
    canvas = tk.Canvas(widgetmanager.root, bg=bg_color, highlightthickness=0, bd=0)
    canvas.place(relx=0.5, rely=0.5, anchor='center', width=board_size, height=board_size)
    widgetmanager.widgets['game_canvas'] = canvas 
    
    lines = [133, 267]
    main_color = '#522525'   
    shadow_color = '#250a0a' 
    light_color = '#ffffff'  
        
    for pos in lines:
        canvas.create_line(pos + 3, 10, pos + 3, board_size - 10, fill=light_color, width=2)
        canvas.create_line(pos - 3, 10, pos - 3, board_size - 10, fill=shadow_color, width=2)
        canvas.create_line(pos, 10, pos, board_size - 10, fill=main_color, width=6)

        canvas.create_line(10, pos + 3, board_size - 10, pos + 3, fill=light_color, width=2)
        canvas.create_line(10, pos - 3, board_size - 10, pos - 3, fill=shadow_color, width=2)
        canvas.create_line(10, pos, board_size - 10, pos, fill=main_color, width=6)

    cell_size = board_size // 3
        
    for row in range(3):
        for col in range(3):
            cell_id = row * 3 + col   
            btn = tk.Button(
                canvas,
                text='',
                font=('Trebuchet MS', 48, 'bold'),
                bg=bg_color,
                activebackground=bg_color,
                relief='flat',
                bd=0,
                highlightthickness=0,
                command=lambda c_id=cell_id: on_cell_click_host(widgetmanager, c_id)
            )
                
            x_center = col * cell_size + (cell_size // 2)
            y_center = row * cell_size + (cell_size // 2)
            
            canvas.create_window(x_center, y_center, window=btn, width=cell_size - 12, height=cell_size - 12)
            widgetmanager.widgets[f'cell_{cell_id}'] = btn

    if not net.servermanager.my_turn:
        lock_all_cells(widgetmanager)

def startgamefunc_client(widgetmanager: WidgetManager, takesocket: str) -> None:
    widgetmanager.widgets['startgamebtn'].config(state='disabled')
    widgetmanager.rootmanager.set_config_for_netmanager(server_or_client=1, getsocket=takesocket)

def startgamefunc_host(widgetmanager: WidgetManager, port: str | int) -> None:
    try:
        port_int = int(port)
    except ValueError:
        widgetmanager.rootmanager.emergency_return_to_main_window(widgetmanager.rootmanager.PROGRAMMER_ERROR)
        raise TypeError('Порт должен быть числом.')
        
    widgetmanager.destroy_wigdets()
    goto_gamebtn = tk.Button(widgetmanager.root, text='play', font=('Trebuchet MS', 12), command=lambda: start_game_widget_host(widgetmanager=widgetmanager), state='disabled')
    goto_gamebtn.pack(pady=(150, 0))
    players_label = tk.Label(widgetmanager.root, text='Players: 1/2', font=('Trebuchet MS', 12))
    players_label.pack()
    widgetmanager.widgets['goto_gamebtn'] = goto_gamebtn
    widgetmanager.widgets['players_label'] = players_label
    widgetmanager.rootmanager.netmanager.set_config(server_or_client=0, port=port_int)

def choice_clientmenuBTN_func(widgetmanager: WidgetManager) -> None:
    widgetmanager.destroy_wigdets()
    
    entry_ip = tk.Entry(widgetmanager.root, font=('Trebuchet MS', 12), width=15)
    entry_ip.insert(0, '127.0.0.1:55556')
    
    startgamebtn = tk.Button(widgetmanager.root, text='Start game', width=8, height=2, font=('Trebuchet MS', 12), command=lambda: startgamefunc_client(widgetmanager, ipget if (ipget := entry_ip.get()) != 'localhost' else '127.0.0.1:55556'))
    back_btn = tk.Button(widgetmanager.root, text='Back', width=8, height=2, font=('Trebuchet MS', 12), command=widgetmanager.choice_role_menu)
    
    startgamebtn.pack(pady=(150, 0))
    entry_ip.pack(pady=10)
    back_btn.pack(pady=10)
    
    widgetmanager.widgets['entry_ip'] = entry_ip
    widgetmanager.widgets['startgamebtn'] = startgamebtn
    widgetmanager.widgets['back_btn'] = back_btn

def choice_hostmenuBTN_func(widgetmanager: WidgetManager) -> None:
    widgetmanager.destroy_wigdets()
    
    entry_port = tk.Entry(widgetmanager.root, font=('Trebuchet MS', 14), width=15)
    entry_port.insert(0, 'Port')
    
    setportbtn = tk.Button(widgetmanager.root, text='Set port', font=('Trebuchet MS', 12), command=lambda: startgamefunc_host(widgetmanager, portget if (portget := entry_port.get()) != 'Port' and portget else 55556))
    
    back_btn = tk.Button(widgetmanager.root, text='Back', width=8, height=2, font=('Trebuchet MS', 12), command=widgetmanager.choice_role_menu)
    
    setportbtn.pack(pady=(150, 0))
    entry_port.pack(pady=10)
    back_btn.pack(pady=10)

    widgetmanager.widgets['entry_port'] = entry_port
    widgetmanager.widgets['setportbtn'] = setportbtn
    widgetmanager.widgets['back_btn'] = back_btn

def wait_host_func(widgetmanager: WidgetManager) -> None:
    widgetmanager.destroy_wigdets()
    label_wait = tk.Label(widgetmanager.root, text='Waiting for the host..', font=('Trebuchet MS', 12))
    label_wait.pack(pady=(150, 0))
    widgetmanager.widgets['label_wait'] = label_wait