import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog

FONT_NORMAL = ('Ubuntu', 13, 'normal')
FONT_TITLE = ('Ubuntu', 18, 'bold')
BASE_COLOR = "#F1EAFF"
LABELS_COLOR = "#E5D4FF"
BUTTONS_COLOR = "#D0A2F7"
TEXT_BG_COLOR = 'white'

TIMER = 10


class GUI(tk.Tk):
    """Main gui class"""

    def __init__(self, title: str, geometry: list):
        super().__init__()
        self.title(title)
        self.maxsize(geometry[0], geometry[1])
        self.config(pady=20, padx=5, bg=BASE_COLOR)
        self.option_add('*Font', FONT_NORMAL)

        # Control variables
        self.start_timer = False
        self.timer_count = TIMER

        # Containing Frames
        self.top_frame = tk.Frame(self, width=geometry[0], height=200, bg=LABELS_COLOR)
        self.top_frame.grid(row=0, column=0, padx=5, pady=5)
        self.middle_frame = tk.Frame(self, width=geometry[0], height=100, bg=LABELS_COLOR)
        self.middle_frame.grid(row=1, column=0, padx=5, pady=5)
        self.bottom_frame = tk.Frame(self, width=geometry[0], height=300, bg=LABELS_COLOR)
        self.bottom_frame.grid(row=2, column=0, padx=5, pady=5)

        # Instruccions
        welcome_label = tk.Label(self.top_frame, text='WELCOME',
                                 background=LABELS_COLOR, font=FONT_TITLE)
        welcome_label.grid(row=0, column=0, padx=5, pady=5, ipadx=10, columnspan=2)

        instructions = ("When you are ready please press the Start button and start writing in the box\n"
                        "below, when you stop writing the timer will start to decrease, if it reaches 0\n"
                        "all the text you have written will be lost.")
        instructions_label = tk.Label(self.top_frame, text=instructions, background=LABELS_COLOR)
        instructions_label.grid(row=1, column=0, padx=5, pady=5, ipadx=10, columnspan=2)

        # Control
        self.start_button = tk.Button(self.middle_frame, text='Start',
                                      background=BUTTONS_COLOR, command=self.start)
        self.start_button.grid(row=0, column=0, padx=20, pady=3)

        self.stop_button = tk.Button(self.middle_frame, text='Stop',
                                     background=BUTTONS_COLOR, state=tk.DISABLED,
                                     command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=20, pady=3)

        self.save_button = tk.Button(self.middle_frame, text='Save text',
                                     background=BUTTONS_COLOR, state=tk.DISABLED,
                                     command=self.save_text)
        self.save_button.grid(row=0, column=2, padx=20, pady=3)

        self.timer_label = tk.Label(self.middle_frame, text='00',
                                    background=TEXT_BG_COLOR, width=8)
        self.timer_label.grid(row=0, column=3, padx=20, pady=3)

        self.user_input = tk.Text(self.bottom_frame, state=tk.DISABLED, height=10, width=62)
        self.user_input.grid(row=0, column=0, padx=10, pady=10,
                             columnspan=4)
        self.user_input.bind("<KeyRelease>", func=self.reset_timer)
        # self.user_input.config(width=62)

    def start(self):
        self.user_input['state'] = tk.NORMAL
        self.stop_button['state'] = tk.NORMAL
        self.save_button['state'] = tk.DISABLED
        self.start_button['state'] = tk.DISABLED

        self.user_input.delete('1.0', tk.END)

        if not self.start_timer:
            self.start_timer = True
            self.decrease_timer()

    def decrease_timer(self):
        if self.timer_count > 0 and self.start_timer:
            self.timer_label.config(text=self.timer_count)
            self.timer_count -= 1
            self.after(1000, self.decrease_timer)
        else:
            self.delete_text()

    def reset_timer(self, event):
        self.timer_count = TIMER
        print('Text modified')

    def delete_text(self):
        self.user_input['state'] = tk.NORMAL
        self.user_input.delete('1.0', tk.END)

        self.stop()
        self.save_button['state'] = tk.DISABLED
        tkinter.messagebox.showwarning('Time ran out!', message="The text has been deleted")

    def stop(self):
        self.timer_count = TIMER
        self.timer_label.config(text=self.timer_count)
        self.user_input['state'] = tk.DISABLED
        self.stop_button['state'] = tk.DISABLED
        self.save_button['state'] = tk.NORMAL
        self.start_button['state'] = tk.NORMAL

    def save_text(self):
        file_path = filedialog.asksaveasfilename(
            title='Save As',
            filetypes=(('All files', '*.*'),
                       ('text', '*.txt'))
        )
        written_text = self.user_input.get('1.0', tk.END)
        if not file_path or not written_text:
            return
        else:
            try:
                with open(file_path, 'w') as file:
                    file.write(written_text)

            except Exception as e:
                tk.messagebox.showerror(title="Error", message='There was an error saving the file!')
                print(e)








