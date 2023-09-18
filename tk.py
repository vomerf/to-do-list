import tkinter as tk
from tkinter import ttk
import psycopg2


conn = psycopg2.connect(
    database="listdb",
    user="testuser",
    password="test",
    host="127.0.0.1",
    port="5432"
)

cur = conn.cursor()

cur.execute(
    '''CREATE TABLE IF NOT EXISTS lists
    (id SERIAL PRIMARY KEY, name TEXT)'''
)

root = tk.Tk()
root.title('Списки дел')
root.configure(bg="#1a205c")
root.geometry("900x600")

button_style = ttk.Style()
button_style.configure('TButton', font=('Helvetica', 16), padding=10)

frame = tk.Frame(root, bg='#28bf9c')
frame.pack()

entry_width = 30

entry = tk.Entry(frame, font=('Helvetica', 16), width=entry_width)
entry.pack()

entry.insert(0, "Введите текст...")
entry.config(foreground="turquoise")
entry.bind("<FocusIn>", lambda event: on_entry_click(event, entry))

lb = tk.Listbox(frame, selectbackground='purple', height=15, width=entry_width)
lb.pack()
lb.config(font=('Helvetica', 16))

sb = tk.Scrollbar(frame)
sb.pack(side=tk.RIGHT, fill=tk.Y)

lb.config(yscrollcommand=sb.set)
sb.config(command=lb.yview)


def on_entry_click(event, widget):
    if widget.get() == "Введите текст...":
        widget.delete(0, tk.END)
        widget.config(foreground="black") 


def add_list():
    name = entry.get()
    if name.strip():
        cur.execute("INSERT INTO lists (name) VALUES (%s)", (name,))
        conn.commit()
        entry.delete(0, tk.END)
        add_update_listbox()


def show_all_lists():
    update_listbox()


def remove_list():
    selected_item = lb.curselection()
    if selected_item:
        name = lb.get(selected_item[0])
        cur.execute("DELETE FROM lists WHERE name = %s", (name,))
        conn.commit()
        lb.delete(selected_item)
    else:
        print("Выберите элемент для удаления.")


def remove_all_lists():
    cur.execute("DELETE FROM lists")
    conn.commit()
    update_listbox()


def update_listbox():
    lb.delete(0, tk.END)

    cur.execute("SELECT * FROM lists")
    for row in cur.fetchall():
        lb.insert(tk.END, row[1])


def add_update_listbox():
    cur.execute("SELECT * FROM lists ORDER BY id DESC LIMIT 1")
    new_row = cur.fetchone()
    if new_row:
        lb.insert(tk.END, new_row[1])


btn_width = entry_width

btn_add = ttk.Button(
    root,
    text='Добавить',
    command=add_list,
    style='TButton',
    width=btn_width
)
btn_add.pack()

btn_show_all = ttk.Button(
    root,
    text='Показать все',
    command=show_all_lists,
    style='TButton',
    width=btn_width
)
btn_show_all.pack()

btn_remove = ttk.Button(
    root,
    text='Удалить',
    command=remove_list,
    style='TButton',
    width=btn_width
)
btn_remove.pack()

btn_remove_all = ttk.Button(
    root,
    text='Удалить все',
    command=remove_all_lists,
    style='TButton',
    width=btn_width
)
btn_remove_all.pack()


button_style.configure('TButton', background='blue', foreground='white')
btn_add.configure(style='TButton')
btn_show_all.configure(style='TButton')
btn_remove.configure(style='TButton')
btn_remove_all.configure(style='TButton')

canvas = tk.Canvas(root, width=900, height=600)
canvas.pack()

canvas.create_rectangle(0, 0, 900, 600, fill="#000000")  # Цвет фона

root.mainloop()
