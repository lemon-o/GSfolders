import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import messagebox


def create_folders(folder_path):
    folder_name = folder_name_entry.get()
    num_folders = num_folders_entry.get()

    if folder_name_entry.get() == '加“/”可创建子文件夹':
        messagebox.showerror("出错了", "请输入文件夹名称")
        return
    
    if not folder_name_entry.get().strip():
        messagebox.showerror("出错了", "请输入文件夹名称")
        return

    try:
        num_folders = int(num_folders)
        if num_folders <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("出错了", "请输入正整数的文件夹数量")
        return

    success_count = 0
    fail_count = 0
    if '/' in folder_name:
        folder_names = folder_name.split('/')
        num_levels = len(folder_names)
        parent_folder_name = folder_names[0]
        sub_folder_name = folder_names[-1]
        for i in range(1, num_folders+1):
            if num_folders == 1:
                folder_path_i = os.path.join(folder_path, folder_name)
            else:
                parent_folder_path = os.path.join(folder_path, f"{parent_folder_name}_{i}")
                os.makedirs(parent_folder_path, exist_ok=True)
                current_path = parent_folder_path
                for j in range(num_levels-2):
                    current_folder_name = folder_names[j+1]
                    current_path = os.path.join(current_path, current_folder_name)
                    os.makedirs(current_path, exist_ok=True)
                folder_path_i = os.path.join(current_path, sub_folder_name)

            try:
                os.makedirs(folder_path_i)
                success_count += 1
            except:
                fail_count += 1

    elif '&' in folder_name:
        folder_names = folder_name.replace('&', ' ').strip().split()
        for i in range(1, num_folders+1):
            if num_folders == 1:
                for name in folder_names:
                    folder_path_i = os.path.join(folder_path, name.strip())
                    try:
                        os.makedirs(folder_path_i)
                        success_count += 1
                    except:
                        fail_count += 1
            else:
                dir_name = f"{folder_name}_{i}"
                folder_path_i = os.path.join(folder_path, dir_name)
                os.makedirs(folder_path_i, exist_ok=True)
                for name in folder_names:
                    sub_folder_path = os.path.join(folder_path_i, name.strip())
                    try:
                        os.makedirs(sub_folder_path)
                        success_count += 1
                    except:
                        fail_count += 1

    else:
        for i in range(1, num_folders+1):
            if num_folders == 1:
                folder_path_i = os.path.join(folder_path, folder_name)
            else:
                folder_path_i = os.path.join(folder_path, f"{folder_name}_{i}")

            try:
                os.makedirs(folder_path_i)
                success_count += 1
            except:
                fail_count += 1
    if success_count > 0:
        messagebox.showinfo("提示", f"成功创建 {success_count} 个文件夹。")
    else:
        messagebox.showerror("出错了", f"创建文件夹失败，共有 {fail_count} 个文件夹创建失败。")

def select_path():
    folder_path = filedialog.askdirectory()
    if folder_path:
        create_folders(folder_path)

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

root = tk.Tk()
root.title("GSfolders")

icon = tk.PhotoImage(file='./icon.png')
root.iconphoto(True, icon)


# 让窗口居中
root.geometry("350x230+{}+{}".format(int(root.winfo_screenwidth()/2 - 150), int(root.winfo_screenheight()/2 - 100)))

font = ("黑体", 12)
default_font = tkFont.Font(family='黑体', size=12, slant='italic')

# 使用 ttk.Style 创建样式对象
style = ttk.Style()

# 设置应用程序样式主题
# theme_name = style.theme_names()[0]
style.theme_use("vista")

# 配置 TButton 样式
style.configure("TButton",
                padding=5,
                relief="flat",
                font=font,
                foreground="#3B3E41", ## 注意这里
                background="#F0F0F0",
                bordercolor="#A5A5A5",
                darkcolor="#A5A5A5",
                lightcolor="#A5A5A5")

# 配置 TEntry 样式
style.configure("TEntry",
                padding=5,
                relief="flat",
                font=default_font,
                foreground="#3B3E41", ## 注意这里
                background="#FFFFFF",
                bordercolor="#A5A5A5",
                darkcolor="#A5A5A5",
                lightcolor="#A5A5A5")

folder_name_label = tk.Label(root, text="文件夹名称", font=font, fg="#3B3E41")
folder_name_label.pack(pady=(10,1))

folder_name_entry = ttk.Entry(root, width=22, justify='center', font=default_font, style="TEntry", foreground='#808080')
folder_name_entry.pack(pady=(5,10))

folder_name_entry.insert(0, '加“/”可创建子文件夹')

def on_entry_click(event):
    if folder_name_entry.get() == '加“/”可创建子文件夹':
        folder_name_entry.delete(0, tk.END) # 删除当前的文字
        folder_name_entry.config(foreground='#333333', font=('黑体', 12))

def on_entry_leave(event):
    if not folder_name_entry.get():
        folder_name_entry.insert(0, '加“/”可创建子文件夹')
        folder_name_entry.config(foreground='#808080', font=default_font)

# 绑定单击和离开事件
folder_name_entry.bind("<Button-1>", on_entry_click)
folder_name_entry.bind("<FocusOut>", on_entry_leave)

num_folders_label = tk.Label(root, text="文件夹数量:", font=font, fg="#3B3E41" )
num_folders_label.pack(pady=(3,1))

num_folders_entry = ttk.Entry(root, justify='center', font=font, width=22, style="TEntry")
num_folders_entry.pack(pady=(5,10))

def create_folders_callback():
    select_path()

create_button = ttk.Button(root, text="创建文件夹", command=create_folders_callback, style="TButton")
create_button.pack(pady=20)

root.mainloop()