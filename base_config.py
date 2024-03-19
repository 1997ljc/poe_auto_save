import json
import logging
import os
import random
import tkinter as tk
import tkinter.filedialog as tkf

import pyautogui

# currency_location left_up_location  right_down_location confirm_location right_path_location left_path_location
# global currency_location
# global left_up_location
# global right_down_location
# global confirm_location
# global right_path_location
# global left_path_location

global global_run_speed
global_run_speed = 2

global user_define_filter
global base_filter


def set_window(width, height, window, root):
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口的左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口的位置和大小
    window.geometry(f"{width}x{height}+{x}+{y}")


def set_location_0(root):
    window0 = tk.Toplevel(root)
    window0.title("设置位置1")
    set_window(350, 130, window0, root)
    label0 = tk.ttk.Label(window0, text="设置刷新货币位置！", style="poe_style.TLabel")
    label0.pack()

    def check_space(event):
        if event.keysym == "space":
            window0.destroy()
            x1, y1 = pyautogui.position()
            global currency_location
            currency_location = (x1, y1)

            set_location_1(root)

    window0.bind("<Key>", check_space)
    window0.focus_force()


def set_location_1(root):
    window1 = tk.Toplevel(root)
    window1.title("设置位置1")
    set_window(350, 130, window1, root)
    label1 = tk.ttk.Label(window1, text="设置第一列左上位置！", style="poe_style.TLabel")
    label1.pack()

    def check_space(event):
        if event.keysym == "space":
            window1.destroy()
            x1, y1 = pyautogui.position()
            global left_up_location
            left_up_location = (x1, y1)

            # set_location_2(root)

    window1.bind("<Key>", check_space)
    window1.focus_force()



def set_speed(root):

    show_set_speed_window = tk.Toplevel(root)
    show_set_speed_window.title("set_run_speed")
    set_window(350, 200, show_set_speed_window)
    # 输入框
    entry_speed = tk.Entry(show_set_speed_window, width=15, font=("Arial", 15))
    entry_speed.insert(0, "输入速度挡位,默认为2")  # 设置默认文本
    entry_speed.config(fg="gray")  # 设置前景色为白色，背景色为透明
    entry_speed.place(relx=0.5, rely=0.45, anchor="center")  # 输入框位置
    # 文本提示
    entry_speed_remind = tk.Label(show_set_speed_window, text="输入1(快)-1000(慢)的数字选择速度挡位！", font=("Courier", 12))
    entry_speed_remind.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本
    button_confirm = tk.ttk.Button(show_set_speed_window, text=" \n  确定  \n ", command=lambda: get_run_speed(entry_speed, show_set_speed_window))
    button_confirm.place(relx=0.7, rely=0.75, anchor="center")  # 设置按钮的位置


def get_run_speed(entry_speed, show_set_speed_window):
    global global_run_speed
    try:
        run_speed = entry_speed.get()
        run_speed = int(run_speed)
        global_run_speed = run_speed

        if (run_speed > 1000) or (run_speed < 1):
            raise ValueError
        show_set_speed_window.destroy()
    except ValueError:
        # raise Error!
        speed_error_window = tk.Toplevel(show_set_speed_window)
        speed_error_window.title("输入错误！！！！")
        set_window(300, 300, speed_error_window)
        # 文本提示
        entry_speed_remind = tk.Label(speed_error_window, text="请输入1-1000的数字！！！！",font=("Courier", 12))
        entry_speed_remind.place(relx=0.5, rely=0.2, anchor="center")  # 设置提示文本


def save_all_config(root):
    # 弹出保存文件对话框
    filepath = tkf.asksaveasfilename(
        defaultextension=".json",  # 默认文件扩展名
        initialfile="tujen.json",  # 设置默认文件名
        initialdir=os.getcwd(),
        filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],  # 文件类型筛选
        title="保存配置文件",  # 对话框标题
    )
    try:
        config_data = {}
        location_list = [currency_location,
                         left_up_location,
                         right_down_location,
                         confirm_location,
                         right_path_location,
                         left_path_location]
        config_data["location"] = location_list
        config_data["global_run_speed"] = global_run_speed
        config_data["base_filter"] = base_filter
        config_data["user_define_filter"] = user_define_filter

        if filepath:
            # 用户选择了文件名，执行保存操作
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(config_data, file)

    except NameError:
        # 弹出窗口
        error_window = tk.Toplevel(root)
        error_window.title("请先设置坐标")
        set_window(200, 200, error_window, root)
        # 创建提示文本
        label_remind = tk.Label(error_window, text="\n\n\n\n请先设置坐标！！", font=("Courier", 15))
        label_remind.pack()


def read_all_config(root):
    # 弹出保存文件对话框
    filepath = tkf.askopenfilename(
        defaultextension=".json",  # 默认文件扩展名
        initialfile="tujen.json",  # 设置默认文件名
        initialdir=os.getcwd(),
        filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],  # 文件类型筛选
        title="读取配置文件",  # 对话框标题
    )

    if filepath.strip() == '':
        print("用户取消了保存操作。")
    else:
        # 从配置文件加载状态
        try:
            with open(filepath, "r", encoding="utf-8") as config_file:
                config_data = json.load(config_file)
                # 读取出来数组
                # for compass_in_config, switch_in_config in config_data.items():
                #     for compass, data in compass_var_dir.items():
                #         if compass == compass_in_config:
                #             var = data[1]
                #             var.set(switch_in_config)
        except FileNotFoundError:
            file_error_window = tk.Toplevel(root)
            file_error_window.title("配置读取出错！")
            set_window(200, 200, file_error_window, root)
            file_error_label = tk.Label(file_error_window, text="配置文件不存在！！")
            file_error_label.pack()


def attention_window(root, width, height, title ,msg, font_size, destort_root = 0):
    attention_window = tk.Toplevel(root)
    attention_window.title(title)
    set_window(width, height, attention_window, attention_window)
    attention_window.attributes('-topmost', True)
    label = tk.Label(attention_window, text=msg, font=("Times New Roman", font_size))
    label.place(relx=0.5, rely=0.5, anchor="center")

    def root_closing():
        attention_window.destroy()
        root.destroy()

    if destort_root == 1:
        # 绑定窗口关闭事件
        attention_window.protocol("WM_DELETE_WINDOW", root_closing)
    return attention_window


def gen_random_time(speed):
    return float(0.03 * speed + 0.0015 * random.randint(1, 50))


def gen_random_offset(position, tier=2.0):
    symbol = random.randint(0,1)
    if symbol == 0:
        return_value = float(position + tier*random.random())
    else:
        return_value = float(position - tier * random.random())

    return return_value


def multi_entry():
    entry_list = []
    # 创建主窗口
    root = tk.Tk()
    root.title("基础配置")
    set_window(600, 500, root, root)
    # 创建 20 个 Label 组件和 20 个输入框，并使用 grid 布局管理器均匀分布
    for i in range(16):
        # 创建 Label 组件
        label = tk.Label(root, text=f"i")
        label.grid(row=(2 * i) % 16, column=(2 * i) // 16, padx=5, pady=4)

        # 创建输入框，并设置对应的标签
        entry = tk.Entry(root)
        entry.grid(row=(2 * i + 1) % 16, column=(2 * i + 1) // 16, padx=5, pady=4)
        entry.insert(0, f"i")  # 设置默认文本
        entry.config(fg="gray")  # 设置前景色为白色，背景色为透明
        entry_list.append(entry)


def set_logging_msg():
    # 设置日志格式
    logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 重定向标准输出和标准错误输出到日志文件
    sys.stdout = open('output.log', 'a')
    sys.stderr = open('output.log', 'a')

    # 打印一些信息到标准输出
    print("这是一条打印信息到标准输出的消息。")

