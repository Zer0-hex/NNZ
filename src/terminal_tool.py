import re
import threading
import subprocess
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText, ScrolledFrame


def call(res_text, sp, func):
    for i in iter(sp.stdout.readline, b''):
        tmp = re.sub(r"\x1b\[.?.?m", '', i.decode())
        print(sp.poll())
        if sp.poll() is None and tmp != '':
            print(tmp)
            res_text.insert(END, tmp)
            res_text.text.yview_moveto(1)

        else:
            tmp = "[-] Success end ..."
            print(tmp)
            func()
            break


class TerminalToolWindow:
    Frame: ttk.Frame = None
    result_text: ScrolledText = None
    run_button: ttk.Button = None
    end_button: ttk.Button = None
    thread: threading.Thread = None
    sp: subprocess.Popen = None

    must_args = []
    nomust_input_args = []
    nomust_noinput_args = []

    def __init__(self, config):
        self.name = config['name']
        self.run_cmd = config['run_cmd']
        if 'must_args' in config:
            self.must_args = config['must_args']
        if 'nomust_input_args' in config:
            self.nomust_input_args = config['nomust_input_args']
        if 'nomust_noinput_args' in config:
            self.nomust_noinput_args = config['nomust_noinput_args']

    def init(self, notebook):
        self.Frame = ttk.Frame(notebook)
        notebook.add(self.Frame, text=self.name)
        self.init_left_option()
        self.init_right_result()

    def init_left_option(self):
        # 左侧选项面板
        option = ScrolledFrame(self.Frame, padding=5)
        option.hide_scrollbars()
        option.place(relwidth=0.382, relheight=1)

        option_frame = ttk.Frame(option, padding=5, borderwidth=1, relief='ridge')
        option_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        # 必选参数组
        must_arg_group = ttk.Frame(option_frame, padding=5)
        must_arg_group.pack(side=TOP, fill=X, pady=10, expand=YES)
        for arg in self.must_args:
            must_frame = ttk.Frame(must_arg_group, padding=5)
            must_frame.pack(side=TOP, fill=X)
            arg['arg_text'] = ttk.StringVar(value=arg['arg_text'])
            arg['arg_enable'] = ttk.BooleanVar(value=arg['arg_enable'])
            ttk.Label(must_frame, text=arg['arg_more'])\
                .pack(side=LEFT, fill=X, padx=(0, 5))
            ttk.Entry(must_frame, textvariable=arg['arg_text']) \
                .pack(side=RIGHT, fill=X, padx=(5, 0), expand=YES)

        self.run_button = ttk.Button(must_arg_group, text="Run", command=self.run)
        self.run_button.pack(side=LEFT, fill=X, expand=YES, padx=(0, 5))
        # Stop Button
        ttk.Button(must_arg_group, text="Stop", command=self.end)\
            .pack(side=LEFT, fill=X, expand=YES, padx=(5, 5))
        # Clear Button
        ttk.Button(must_arg_group, text="Clear", command=self.clear)\
            .pack(side=LEFT, fill=X, expand=YES)
        # 可选参数组
        nomust_arg_group = ttk.Frame(option_frame, padding=5)
        nomust_arg_group.pack(side=TOP, fill=X, pady=10, expand=YES)

        # 选项参数
        for arg in self.nomust_noinput_args:
            arg['arg_enable'] = ttk.BooleanVar(value=arg['arg_enable'])
            ttk.Checkbutton(nomust_arg_group, text=arg['arg_more'], variable=arg['arg_enable'], onvalue=True,
                            offvalue=False, bootstyle='round-toggle') \
                .pack(side=TOP, fill=X, ipady=5, ipadx=5)

        # 输入参数
        for arg in self.nomust_input_args:
            arg['arg_text'] = ttk.StringVar(value=arg['arg_text'])
            arg['arg_enable'] = ttk.BooleanVar(value=arg['arg_enable'])
            arg_frame = ttk.Frame(nomust_arg_group)
            arg_frame.pack(side=TOP, fill=X, pady=5)
            ttk.Checkbutton(arg_frame, text=arg['arg_more'], variable=arg['arg_enable'], onvalue=True, offvalue=False) \
                .pack(side=LEFT, fill=X, ipady=5, padx=(0, 5), anchor=NW)
            ttk.Entry(arg_frame, textvariable=arg['arg_text']) \
                .pack(side=LEFT, fill=X, expand=YES, anchor=NE)

        # 文件路径获取
        tool_frame = ttk.Frame(option_frame, padding=5)
        tool_frame.pack(side=TOP, fill=X, pady=10, expand=YES)

        ttk.Label(tool_frame, text="获取文件路径") \
            .pack(side=LEFT, fill=X, padx=(0, 5))
        file_path = ttk.StringVar()
        ttk.Entry(tool_frame, textvariable=file_path) \
            .pack(side=LEFT, fill=X, expand=YES)
        ttk.Button(tool_frame, text="选择文件", command=lambda: file_path.set(filedialog.askopenfilename())) \
            .pack(side=RIGHT, fill=X, padx=(5, 0))

    def init_right_result(self):
        # 右侧输出面板
        self.result_text = ScrolledText(self.Frame, padding=5, autohide=True, font=("Courier", 10))
        self.result_text.place(relx=0.382, rely=0, relwidth=0.618, relheight=1)
        # self.result_text.pack(side=RIGHT, fill=BOTH, expand=YES)

    def run(self):
        self.run_button['state'] = 'disabled'
        self.run_button.configure(text="Running")
        arg_str = " "

        for must_arg in self.must_args:
            arg_str += must_arg['arg_name']
            arg_str += must_arg['arg_text'].get()
            arg_str += " "

        for i in self.nomust_noinput_args:
            if i['arg_enable'].get():
                arg_str += i['arg_name']

        for i in self.nomust_input_args:
            if i['arg_enable'].get():
                arg_str += i['arg_name']
                arg_str += i['arg_text'].get()
            arg_str += " "

        cmd = self.run_cmd + arg_str
        print(f"[+] exec: {cmd}")
        s = self.result_text.winfo_width() // 12
        s = ("-" * s)[:-2] + '\n'
        self.result_text.insert(END, s)
        self.result_text.insert(END, f"$ {cmd}\n")
        self.result_text.insert(END, s)
        self.sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        self.thread = threading.Thread(target=call, args=(self.result_text, self.sp, lambda: self.end("[-] Success end ...")), daemon=True)
        self.thread.start()

    def end(self, end_str="[-] You kill it, good job!\n"):
        if self.sp:
            if self.sp.poll() is None:
                self.sp.kill()
                self.result_text.insert(END, end_str)
                self.result_text.text.yview_moveto(1)
                self.run_button['state'] = 'active'
                self.run_button.configure(text="Run")
            else:
                self.sp = None
                end_str = "[*] No work now, I advise you to be honest.\n"
                self.result_text.insert(END, end_str)
        else:
            end_str = "[*] What are you fucking doing?\n"
            self.result_text.insert(END, end_str)

    def clear(self):
        self.result_text.delete("1.0", END)
