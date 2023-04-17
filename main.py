import tkinter as tk
import tkinter.messagebox as tkm
import customtkinter as ctk
import os
import openai
import sqlite3
from datetime import datetime
import pytz

# Connect to openAI
API_KEY = "***"
os.environ['OPENAI_Key'] = API_KEY
openai.api_key = os.environ['OPENAI_Key']

# set app theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Connect to the database
conn = sqlite3.connect('chatbot.db')
c = conn.cursor()
# Set timezone to India (GMT+5:30)
timezone = pytz.timezone('Asia/Kolkata')
# Create the table to store chat history if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now', 'utc'))
    )
''')
conn.commit()


# Main app class
class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # configure window
        self.title("ChatBot")
        self.geometry(f"{1600}x{900}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame,
                                       text="ChatBot",
                                       font=ctk.CTkFont(size=24,
                                                        weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(
            self.sidebar_frame,
            font=ctk.CTkFont(size=16, weight="normal"),
            height=50,
            command=lambda: self.clear_history(),
            text="Clear History")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame,
                                                  text="Appearance Mode:",
                                                  anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6,
                                              column=0,
                                              padx=20,
                                              pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame,
                                          text="UI Scaling:",
                                          anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # History Bar
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame,
                                       text="History",
                                       font=ctk.CTkFont(size=20,
                                                        weight="normal"))
        self.logo_label.grid(row=0, column=0, padx=60, pady=(20, 0))

        # Create a Text widget to display history
        self.history_text = ctk.CTkTextbox(
            self.sidebar_frame,
            height=ctk.CTk.winfo_screenheight(self),
            width=800,
            font=ctk.CTkFont(size=14, weight="bold"))
        self.history_text.grid(row=1, column=0, padx=10, pady=10)

        # Add content to the Text widget
        self.entry = ctk.CTkEntry(self, placeholder_text="Ask Here")
        self.entry.grid(row=3,
                        column=1,
                        columnspan=2,
                        padx=(20, 20),
                        pady=(20, 20),
                        sticky="nsew")

        # create main button
        self.main_button_1 = ctk.CTkButton(master=self,
                                           width=100,
                                           fg_color="transparent",
                                           border_width=2,
                                           text="Search",
                                           text_color=("gray10", "#DCE4EE"),
                                           command=lambda: self.ans())

        self.main_button_1.grid(row=3,
                                column=3,
                                columnspan=1,
                                padx=(250, 250),
                                pady=(20, 20),
                                sticky="nsew")

        # create textbox
        self.textbox = ctk.CTkTextbox(self,
                                      width=250,
                                      font=ctk.CTkFont(size=16))

        self.textbox.grid(row=0,
                          column=1,
                          padx=(20, 20),
                          pady=(20, 0),
                          sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "Answers Here\n\n")
        self.textbox.configure(state="disabled")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.sidebar_frame.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
        self.sidebar_frame.set_widget_scaling(new_scaling_float)

    def clear_history(self):
        c.execute("DELETE FROM chat_history")
        conn.commit()
        self.history()

    def ans(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0",
                            "\n\n" + str(self.get_response(self.entry.get())))
        self.textbox.configure(state="disabled")

    def history(self):
        c.execute("SELECT * FROM chat_history ORDER BY created_at DESC")
        rows = c.fetchall()
        print(rows)
        self.history_text.configure(state="normal")
        self.history_text.delete("0.0", "end")
        for row in rows:
            self.history_text.insert(ctk.END, f"\n\nDATE and TIME: {row[3]}\n")
            self.history_text.insert(ctk.END, f"Query: {row[1]}\n")
            self.history_text.insert(ctk.END, f"Response: {row[2]}\n\n")
        self.history_text.configure(state="disabled")

    def get_response(self, prompt):
        response = openai.Completion.create(model='text-davinci-003',
                                            prompt=prompt,
                                            max_tokens=1000)

        answer = response.choices[0].text.strip()

        # Store the chat history in the database with current time in India
        current_time = datetime.now(timezone)
        current_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
        c.execute(
            'INSERT INTO chat_history (query, response, created_at) VALUES (?, ?, ?)',
            (self.entry.get(), answer, current_time))
        conn.commit()
        self.history()
        return (answer)


if __name__ == "__main__":
    app = App()
    app.history()
    app.mainloop()
