import tkinter as tk
from tkinter import messagebox


class App:
    def init(self, root):
        self.root = root
        self.root.title("Main Window")

        self.button1 = tk.Button(root, text="مشتری", command=self.open_window1)
        self.button1.pack(pady=20)

        self.button2 = tk.Button(root, text="ادمین", command=self.open_window2)
        self.button2.pack(pady=20)

        self.window1 = None
        self.window2 = None

    def open_window1(self):
        if self.window1 is None or not self.window1.winfo_exists():
            self.window1 = tk.Toplevel(self.root)
            self.window1.title("Window 1")

            self.window1.protocol("WM_DELETE_WINDOW", self.on_close_window1)

            tk.Label(self.window1, text="نام کاربری").pack()
            self.entry1_1 = tk.Entry(self.window1)
            self.entry1_1.pack(pady=5)

            tk.Label(self.window1, text="رمز عبور").pack()
            self.entry1_2 = tk.Entry(self.window1)
            self.entry1_2.pack(pady=5)

            submit_btn = tk.Button(self.window1, text="Submit",
                                   command=lambda: self.submit_data(1, self.entry1_1.get(), self.entry1_2.get()))
            submit_btn.pack(pady=10)
        else:
            self.window1.lift()

    def open_window2(self):
        if self.window2 is None or not self.window2.winfo_exists():
            self.window2 = tk.Toplevel(self.root)
            self.window2.title("Window 2")

            self.window2.protocol("WM_DELETE_WINDOW", self.on_close_window2)

            tk.Label(self.window2, text="نام کاربری ").pack()
            self.entry2_1 = tk.Entry(self.window2)
            self.entry2_1.pack(pady=5)

            tk.Label(self.window2, text=" رمز عبور").pack()
            self.entry2_2 = tk.Entry(self.window2)
            self.entry2_2.pack(pady=5)

            submit_btn = tk.Button(self.window2, text="Submit",
                                   command=lambda: self.submit_data(2, self.entry2_1.get(), self.entry2_2.get()))
            submit_btn.pack(pady=10)
        else:
            self.window2.lift()

    def on_close_window1(self):
        self.window1.destroy()
        self.window1 = None

    def on_close_window2(self):
        self.window2.destroy()
        self.window2 = None

    def submit_data(self, window_num, data1, data2):
        messagebox.showinfo("Submission",
                            f"From Window {window_num}:\nEntry 1: {data1}\nEntry 2: {data2}")


if name == "main":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
