import tkinter as tk
import tkinter.messagebox as tkm
import customtkinter as ctk
import os
import openai

API_KEY = "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"
os.environ['OPENAI_Key'] = API_KEY
openai.api_key = os.environ['OPENAI_Key']

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # configure window
        self.title("ChatBot")
        self.geometry(f"{1100}x{600}")

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
                                       font=ctk.CTkFont(size=20,
                                                        weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, text="Home")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(
            self.sidebar_frame,
            command=self.sidebar_button_event,
            text="Settings")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
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
                                       font=ctk.CTkFont(size=18,
                                                        weight="normal"))
        self.logo_label.grid(row=0, column=0, padx=60, pady=(20, 0))

        # create main entry and button
        self.entry = ctk.CTkEntry(self, placeholder_text="Ask Here")
        self.entry.grid(row=3,
                        column=1,
                        columnspan=2,
                        padx=(20, 20),
                        pady=(20, 20),
                        sticky="nsew")

        self.main_button_1 = ctk.CTkButton(master=self,
                                           fg_color="transparent",
                                           border_width=2,
                                           text="Search",
                                           text_color=("gray10", "#DCE4EE"),
                                           command=lambda: self.ans())

        self.main_button_1.grid(row=3,
                                column=3,
                                padx=(20, 20),
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
        self.textbox.insert("0.0", "Answers Here\n\n"
                            )  # + str(self.search(prompt="What is the sun?")))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def ans(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "\n\n" + str(self.search(self.entry.get())))
        self.textbox.configure(state="disabled")

    def search(self, prompt):
        response = openai.Completion.create(model='text-davinci-003',
                                            prompt=prompt,
                                            max_tokens=1000)
        return (response.choices[0].text.strip())


if __name__ == "__main__":
    app = App()
    app.mainloop()
