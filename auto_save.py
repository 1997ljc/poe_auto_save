import tkinter as tk
import keyboard as kb
import pyautogui
import random
import os
import base_config
import json

class GridCanvas(tk.Canvas):
    def __init__(self, master, rows, cols, cell_size, border_width=1, **kwargs):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.border_width = border_width
        self.grid = [[0] * cols for _ in range(rows)]  # 0 表示灰色，1 表示红色
        self.rects = {}

        width = cols * cell_size
        height = rows * cell_size
        super().__init__(master, width=width, height=height, **kwargs)

        self.bind("<Button-1>", self.on_click)

        self.draw_grid()

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x0, y0 = col * self.cell_size, row * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                rect_id = self.create_rectangle(x0, y0, x1, y1, fill="gray", outline="black", width=self.border_width)
                self.rects[(row, col)] = rect_id

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            rect_id = self.rects[(row, col)]
            if self.grid[row][col] == 0:
                self.itemconfig(rect_id, fill="red")
                self.grid[row][col] = 1
            else:
                self.itemconfig(rect_id, fill="gray")
                self.grid[row][col] = 0


class Application(tk.Tk):
    def __init__(self, config_file):
        super().__init__()
        self.title("自动存包")
        base_config.set_window(430, 400, self, self)

        #初始化变量
        self.position_list = [1726, 816, 2501, 1098]
        self.hotkey_0 = "space+f1"
        self.hotkey_1 = "space+f2"
        self.hotkey_2 = "space+f3"
        self.file_path = os.path.join(os.getcwd(), config_file)
        self.redcells = []

        self.check_backpack_position()

        self.rows, self.cols = 5, 12
        self.cell_size = 30

        self.grid_canvas = GridCanvas(self, self.rows, self.cols, self.cell_size)
        self.grid_canvas.pack()

        self.confirm_button = tk.Button(self, text="\n    确定    \n", command=self.confirm)
        self.confirm_button.place(relx=0.2, rely=0.65, anchor="center")


        self.label1 = tk.Label(self, text="背包左上x", font=("Courier", 8))
        self.label1.place(relx=0.4, rely=0.45, anchor="center")  # 设置提示文本
        self.entry_lu_x = tk.Entry(self,width=5)
        self.entry_lu_x.insert(0, f"{self.position_list[0]}")  # 设置默认文本
        self.entry_lu_x.config(fg="gray")  # 设置前景色为白色，背景色为透明
        self.entry_lu_x.place(relx=0.55, rely=0.45, anchor="center")

        self.label2 = tk.Label(self, text="背包左上y", font=("Courier", 8))
        self.label2.place(relx=0.4, rely=0.5, anchor="center")  # 设置提示文本
        self.entry_lu_y = tk.Entry(self,width=5)
        self.entry_lu_y.insert(0, f"{self.position_list[1]}")  # 设置默认文本
        self.entry_lu_y.config(fg="gray")  # 设置前景色为白色，背景色为透明
        self.entry_lu_y.place(relx=0.55, rely=0.5, anchor="center")

        self.label3 = tk.Label(self, text="背包右下x", font=("Courier", 8))
        self.label3.place(relx=0.7, rely=0.45, anchor="center")  # 设置提示文本
        self.entry_rd_x = tk.Entry(self,width=5)
        self.entry_rd_x.insert(0, f"{self.position_list[2]}")  # 设置默认文本
        self.entry_rd_x.config(fg="gray")  # 设置前景色为白色，背景色为透明
        self.entry_rd_x.place(relx=0.85, rely=0.45, anchor="center")

        self.label4 = tk.Label(self, text="背包右下y", font=("Courier", 8))
        self.label4.place(relx=0.7, rely=0.5, anchor="center")  # 设置提示文本
        self.entry_rd_y = tk.Entry(self,width=5)
        self.entry_rd_y.insert(0, f"{self.position_list[3]}")  # 设置默认文本
        self.entry_rd_y.config(fg="gray")  # 设置前景色为白色，背景色为透明
        self.entry_rd_y.place(relx=0.85, rely=0.5, anchor="center")

        self.label5 = tk.Label(self, text="随机存", font=("Courier", 12))
        self.label5.place(relx=0.45, rely=0.6, anchor="center")  # 设置提示文本
        self.entry_hotkey_0 = tk.Entry(self, width=20)
        self.entry_hotkey_0.insert(0, f"{self.hotkey_0}")  # 设置默认文本
        self.entry_hotkey_0.config(fg="gray")  # 设置前景色为白色，背景色为透明
        self.entry_hotkey_0.place(relx=0.75, rely=0.6, anchor="center")

        self.label6 = tk.Label(self, text="按排", font=("Courier", 12))
        self.label6.place(relx=0.45, rely=0.7, anchor="center")  # 设置提示文本
        self.entry_hotkey_1 = tk.Entry(self, width=20)
        self.entry_hotkey_1.insert(0, f"{self.hotkey_1}")  # 设置默认文本
        self.entry_hotkey_1.config(fg="gray")  # 设置前景色为白色，背景色为透明
        self.entry_hotkey_1.place(relx=0.75, rely=0.7, anchor="center")

        self.label7 = tk.Label(self, text="按列", font=("Courier", 12))
        self.label7.place(relx=0.45, rely=0.8, anchor="center")  # 设置提示文本
        self.entry_hotkey_2 = tk.Entry(self, width=20)
        self.entry_hotkey_2.insert(0, f"{self.hotkey_2}")  # 设置默认文本
        self.entry_hotkey_2.config(fg="gray")  # 设置前景色为白色，背景色为透明
        self.entry_hotkey_2.place(relx=0.75, rely=0.8, anchor="center")

        self.load_config()

    def auto_save_random(self):

        skip_blank_list = []
        blank_list = []

        x_step = (self.position_list[2] - self.position_list[0])/11.0
        y_step = (self.position_list[3] - self.position_list[1])/4.0

        for redcell in self.redcells:
            redcell = tuple(redcell)
            skip_blank_list.append(redcell)

        # 过滤掉不存的格子
        for y in range(5):
            for x in range(12):
                if (y, x) not in skip_blank_list:
                    blank_list.append((y, x))
                else:
                    print(f"{y},{x}被跳过")
        random.shuffle(blank_list)
        # 按住ctrl
        pyautogui.keyDown("ctrl")
        for each in blank_list:
            if kb.is_pressed('end'):
                break
            else:

                curr_location = ((self.position_list[0] + each[1] * x_step * 1.0) + 3 * random.random(),
                                 (self.position_list[1] + each[0] * y_step * 1.0) + 3 * random.random())
                pyautogui.moveTo(*curr_location, duration=0.01)
                # 点击鼠标左键
                pyautogui.click(button="left")
        # 松开ctrl
        pyautogui.keyUp("ctrl")

    def auto_save_row(self):

        x_step = (self.position_list[2] - self.position_list[0])/11.0
        y_step = (self.position_list[3] - self.position_list[1])/4.0
        break_flag_row = 0
        self.redcells = [tuple(redcell) for redcell in self.redcells]
        print(self.redcells)
        # 过滤掉不存的格子
        for y in range(5):
            # 按住ctrl
            pyautogui.keyDown("ctrl")
            for x in range(12):
                print((y,x))
                if (y, x) not in self.redcells:
                    if kb.is_pressed('end'):
                        break_flag_row = 1
                        break
                    else:
                        curr_location = ((self.position_list[0] + x * x_step * 1.0) + 3 * random.random(),
                                         (self.position_list[1] + y * y_step * 1.0) + 3 * random.random())
                        pyautogui.moveTo(*curr_location, duration=0.001)
                        # 点击鼠标左键
                        pyautogui.click(button="left")
                else:
                    print(f"{y},{x}被跳过")
            # 松开ctrl
            pyautogui.keyUp("ctrl")
            if break_flag_row == 1:
                break





    def auto_save_col(self):
        x_step = (self.position_list[2] - self.position_list[0])/11.0
        y_step = (self.position_list[3] - self.position_list[1])/4.0
        break_flag_col = 0
        self.redcells = [tuple(redcell) for redcell in self.redcells]
        # 过滤掉不存的格子
        for x in range(12):
            # 按住ctrl
            pyautogui.keyDown("ctrl")
            for y in range(5):
                if (y, x) not in self.redcells:
                    if kb.is_pressed('end'):
                        break_flag_col = 1
                        break
                    else:
                        curr_location = ((self.position_list[0] + x * x_step * 1.0) + 3 * random.random(),
                                         (self.position_list[1] + y * y_step * 1.0) + 3 * random.random())
                        pyautogui.moveTo(*curr_location, duration=0.001)
                        # 点击鼠标左键
                        pyautogui.click(button="left")
                else:
                    print(f"{y},{x}被跳过")
            # 松开ctrl
            pyautogui.keyUp("ctrl")
            if break_flag_col == 1:
                break

    def load_config(self):
        for redcell in self.redcells:
            row, col = redcell
            if 0 <= row < self.rows and 0 <= col < self.cols:
                rect_id = self.grid_canvas.rects[(row, col)]
                self.grid_canvas.itemconfig(rect_id, fill="red")
                self.grid_canvas.grid[row][col] = 1

    def confirm(self):
        red_cells = [(row, col) for row in range(self.rows) for col in range(self.cols) if self.grid_canvas.grid[row][col] == 1]
        print("红色格子的坐标：", red_cells)
        self.redcells = red_cells
        self.position_list = [int(self.entry_lu_x.get()), int(self.entry_lu_y.get()),
                              int(self.entry_rd_x.get()), int(self.entry_rd_y.get())]
        self.hotkey_0 = self.entry_hotkey_0.get()
        self.hotkey_1 = self.entry_hotkey_1.get()
        self.hotkey_2 = self.entry_hotkey_2.get()

        with open(self.file_path, "r") as file:
            all_config_json = json.load(file)
            all_config_json["redcells"] = self.redcells
            all_config_json["position"] = self.position_list
            all_config_json["hotkey_0"] = self.hotkey_0
            all_config_json["hotkey_1"] = self.hotkey_1
            all_config_json["hotkey_2"] = self.hotkey_2
        with open(self.file_path, "w") as file:
            json.dump(all_config_json, file, indent=4)


    def check_backpack_position(self):

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                all_config_json = json.load(file)
                self.position_list = all_config_json["position"]
                self.hotkey_0 = all_config_json["hotkey_0"]
                self.hotkey_1 = all_config_json["hotkey_1"]
                self.hotkey_2 = all_config_json["hotkey_2"]
                self.redcells = all_config_json["redcells"]
        else:
            with open(self.file_path, "w") as file:
                all_config_json = {}
                all_config_json["position"] = self.position_list
                all_config_json["hotkey_0"] = self.hotkey_0
                all_config_json["hotkey_1"] = self.hotkey_1
                all_config_json["hotkey_2"] = self.hotkey_2
                all_config_json["redcells"] = self.redcells

                json.dump(all_config_json, file, indent=4, ensure_ascii=False)


def main():
    config_file = ".AutoSaveConfig"
    app = Application(config_file)

    kb.add_hotkey(app.hotkey_0, app.auto_save_random)
    kb.add_hotkey(app.hotkey_1, app.auto_save_row)
    kb.add_hotkey(app.hotkey_2, app.auto_save_col)

    app.mainloop()


if __name__ == "__main__":
    main()
