import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import from_file
import from_link
from event_bus import event_bus
from db_manager import database
from utility.utility import myprint as mprint
from utility.bcolors import bcolors as bc

results_zero = {'F': {'F1': {'min': 0,
                        'avg': 0,
                        'max': 0},
                 'F2': {'min': 0,
                        'avg': 0,
                        'max': 0},
                 'F3': {'min': 0,
                        'avg': 0,
                        'max': 0},
                 'F4': {'min': 0,
                        'avg': 0,
                        'max': 0},
                 'G_F': {'min': 0,
                         'avg': 0,
                         'max': 0}},
           'A': {'A1': {'min': 0,
                        'avg': 0,
                        'max': 0},
                 'A1.1': {'min': 0,
                          'avg': 0,
                          'max': 0},
                 'A1.2': {'min': 0,
                          'avg': 0,
                          'max': 0},
                 'G_A': {'min': 0,
                         'avg': 0,
                         'max': 0}},
           'I': {'I1': {'min': 0,
                        'avg': 0,
                        'max': 0},
                 'I2': {'min': 0,
                        'avg': 0,
                        'max': 0},
                 'I3': {'min': 0,
                        'avg': 0,
                        'max': 0},
                 'G_I': {'min': 0,
                         'avg': 0,
                         'max': 0}},
           'R': {'R1': {'min': 0,
                        'avg': 0,
                        'max': 0},
                 'R1.1': {'min': 0,
                          'avg': 0,
                          'max': 0},
                 'R1.2': {'min': 0,
                          'avg': 0,
                          'max': 0},
                 'R1.3': {'min': 0,
                          'avg': 0,
                          'max': 0},
                 'G_R': {'min': 0,
                         'avg': 0,
                         'max': 0},
                 }}

result_zero_linkfile = {'F': {'F1': 0,
                              'F2': 0,
                              'F3': 0,
                              'F4': 0,
                              'G_F': 0},
                        'A': {'A1': 0,
                              'A1.1': 0,
                              'A1.2': 0,
                              'G_A': 0},
                        'I': {'I1': 0,
                              'I2': 0,
                              'I3': 0,
                              'G_I': 0},
                        'R': {'R1': 0,
                              'R1.1': 0,
                              'R1.2': 0,
                              'R1.3': 0,
                              'G_R': 0,
                              }}


# GUI PAGE MANAGER
class TkinterApp(tk.Tk):
    mprint('LOADING PAGE MANAGER', bc.ENDC, 0)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        event_bus.subscribe(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.copyframes = {}

        for F in (StartPage, PortalPage, EvaluationPage, FileEvaluationPage, LinkFileEvaluationPage):
            frame = F(container, self)
            copyframe = F(container, self)

            self.frames[F] = frame
            self.copyframes[F] = copyframe

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        x_pos = screen_width - 50 - self.winfo_width()
        y_pos = 50
        self.geometry(f"+{x_pos}+{y_pos}")

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def handle_event(self, event):
        if event['type'] == 'topgui_start':
            event = {
                'type': 'gui_start',
                'x': self.winfo_x(),
                'width': self.winfo_width(),
                'y': self.winfo_y()
            }
            event_bus.publish(event)


# GUI START PAGE
class StartPage(tk.Frame):
    mprint('LOADING START PAGE', bc.ENDC, 0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='white')

        event_bus.subscribe(self)
        self.logo_frame = tk.Frame(self, background='white')
        self.logo_frame.grid(column=0, row=0, sticky='w')

        self.logo = ImageTk.PhotoImage(Image.open("gui_elements/eufair.png").resize((200, 160)))
        logo_label = tk.Label(self.logo_frame, background='white')
        logo_label.grid(row=0, column=0, sticky='w')
        logo_label.config(background="white", image=self.logo)

        options_portal_frame = tk.Frame(self, background='white', borderwidth=5)
        options_portal_frame.grid(column=0, row=1)

        options_link_frame = tk.Frame(self, background='white', borderwidth=5)
        options_link_frame.grid(column=0, row=2)

        options_file_frame = tk.Frame(self, background='white', borderwidth=5)
        options_file_frame.grid(column=0, row=3)

        self.option_portal_label = ImageTk.PhotoImage(Image.open("gui_elements/portal1.png").resize((1000, 180)))
        self.option_portal_label_hover = ImageTk.PhotoImage(
            Image.open("gui_elements/portal_hover1.png").resize((1000, 180)))
        self.option_link_label = ImageTk.PhotoImage(Image.open("gui_elements/url1.png").resize((1000, 180)))
        self.option_link_label_hover = ImageTk.PhotoImage(
            Image.open("gui_elements/url_hover1.png").resize((1000, 180)))
        self.option_file_label = ImageTk.PhotoImage(Image.open("gui_elements/file1.png").resize((1000, 180)))
        self.option_file_label_hover = ImageTk.PhotoImage(
            Image.open("gui_elements/file_hover1.png").resize((1000, 180)))

        self.labels_images = [self.option_portal_label, self.option_portal_label_hover,
                              self.option_link_label, self.option_link_label_hover,
                              self.option_file_label, self.option_file_label_hover]

        self.box_image = ImageTk.PhotoImage(
            Image.open("gui_elements/button_box.png").resize((1000, 180)))

        self.option_portal = tk.Button(options_portal_frame, background='white', highlightthickness=0, bd=0)
        self.option_portal.grid(row=0, column=0)
        self.option_portal.config(image=self.option_portal_label)
        self.option_portal.bind("<Enter>", self.on_enter)
        self.option_portal.bind("<Leave>", self.on_exit)
        # self.option_portal.bind("<Button-1>", lambda event: self.on_click(event, controller, PortalPage))
        self.option_portal.bind("<Button-1>", lambda x: controller.show_frame(PortalPage))

        self.option_link = tk.Button(options_link_frame, background='white', highlightthickness=0, bd=0)
        self.option_link.grid(row=1, column=0)
        self.option_link.config(image=self.option_link_label)
        self.option_link.bind("<Enter>", self.on_enter)
        self.option_link.bind("<Leave>", self.on_exit)
        self.option_link.bind("<Button-1>", lambda event : self.on_click_link(event, controller))

        self.entry_link=tk.Entry(options_link_frame, state='disabled', width=50, font=(None, 20), background='#D9D9D9')
        self.entry_link.grid(row=1,column=0)
        self.entry_link.lower()

        self.option_file = tk.Button(options_file_frame, background='white', highlightthickness=0, bd=0)
        self.option_file.grid(row=2, column=0)
        self.option_file.config(image=self.option_file_label)
        self.option_file.bind("<Enter>", self.on_enter)
        self.option_file.bind("<Leave>", self.on_exit)
        self.option_file.bind("<Button-1>", lambda event : self.on_click_file(event, controller))

        self.entry_file=tk.Entry(options_file_frame, state='disabled', width=50, font=(None, 20), background='#D9D9D9')
        self.entry_file.grid(row=2, column=0)
        self.entry_file.lower()

    def on_return_link(self, event, controller):
        url_ = self.entry_link.get()
        event_bus.publish({'type': 'chosen_url',
                           'url': url_})

        controller.show_frame(LinkFileEvaluationPage)

    def on_return_file(self, event, controller):
        path = self.entry_file.get()
        event_bus.publish({'type': 'chosen_file_path',
                           'path': path})

        controller.show_frame(LinkFileEvaluationPage)

    def on_click_link(self, event, controller):
        self.option_link.config(image=self.box_image)
        if self.entry_link.cget("state") == "disabled":
            self.entry_link.configure(state="normal")

        self.option_link.unbind('<Leave>')
        self.option_link.unbind('<Enter>')

        self.entry_link.lift()
        self.entry_link.bind('<Return>', lambda event: self.on_return_link(event, controller))

    def on_click_file(self, event, controller):
        self.option_file.config(image=self.box_image)
        if self.entry_file.cget("state") == "disabled":
            self.entry_file.configure(state="normal")

        self.option_file.unbind('<Leave>')
        self.option_file.unbind('<Enter>')

        self.entry_file.lift()
        self.entry_file.bind('<Return>', lambda event: self.on_return_file(event, controller))

    def handle_event(self, event):
        if event['type'] == 'home_clicked':
            self.option_portal.config(image = self.labels_images[0])
            self.option_link.config(image = self.labels_images[2])
            self.option_file.config(image= self.labels_images[4])
            if self.entry_link.get():
                self.entry_link.delete(0, tk.END)
            if self.entry_link.cget("state") == "normal":
                self.entry_link.configure(state="disabled")
                self.entry_link.lower()
                self.option_link.bind('<Leave>', self.on_exit)
                self.option_link.bind('<Enter>', self.on_enter)

            if self.entry_file.get():
                self.entry_file.delete(0, tk.END)
            if self.entry_file.cget("state") == "normal":
                self.entry_file.configure(state="disabled")
                self.entry_file.lower()
                self.option_file.bind('<Leave>', self.on_exit)
                self.option_file.bind('<Enter>', self.on_enter)



    def on_enter(self, e):
        image = int((e.widget['image'])[-1]) - 2
        e.widget['image'] = self.labels_images[image + 1]

    def on_exit(self, e):
        image = int((e.widget['image'])[-1]) - 2
        e.widget['image'] = self.labels_images[image - 1]

    def on_click(self, e, controller, page):
        self.update()

        controller.show_frame(page)


# GUI PORTAL CONSULTATION PAGE
class PortalPage(tk.Frame):
    mprint('LOADING PORTAL PAGE', bc.ENDC, 0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='white')

        event_bus.subscribe(self)

        self.logo_frame = tk.Frame(self, background='white')
        self.logo_frame.grid(column=0, row=0, sticky='w')

        self.logo = ImageTk.PhotoImage(Image.open("gui_elements/eufair.png").resize((200, 160)))
        logo_label = tk.Label(self.logo_frame, background='white')
        logo_label.grid(row=0, column=0, sticky='e')
        logo_label.config(background="white", image=self.logo)

        blank = tk.Label(self.logo_frame, background='white', width=85, height=1)
        blank.grid(row=0, column=1)

        self.home = ImageTk.PhotoImage(Image.open("gui_elements/home.png").resize((30, 30)))
        home_butt = tk.Label(blank, background='white')
        home_butt.grid(row=0, column=0, sticky='sw')
        home_butt.config(background="white", image=self.home)
        home_butt.bind('<Button-1>', lambda event: self.home_call(event, controller))

        self.canvas = tk.Canvas(self.logo_frame, width=200, height=200, background='white', highlightbackground='white')
        self.canvas.grid(row=0, column=2, sticky='e')

        # Coordinata del centro del pallino
        x = 190
        y = 15

        # Raggio del pallino
        raggio = 10

        self.oval = self.canvas.create_oval(x - raggio, y - raggio, x + raggio, y + raggio, fill='red', outline= 'red')

        self.tooltip = tk.Label(self.logo_frame, bg="yellow", relief="solid", borderwidth=1)
        self.tooltip_visible = False

        self.canvas.tag_bind(self.oval, "<Enter>", self.show_tooltip)
        self.canvas.tag_bind(self.oval, "<Leave>", self.hide_tooltip)

        self.search_frame = ttk.Notebook(self)

        self.search_frame.grid(row=1, column=0, sticky="nsew")
        search_dataset = ttk.Frame(self.search_frame)
        search_holder = ttk.Frame(self.search_frame)
        self.search_frame.add(search_dataset, text='Search dataset')
        self.search_frame.add(search_holder, text='Search holder')

        self.search_bar = ImageTk.PhotoImage(Image.open("gui_elements/europa_inbox.png").resize((1010, 35)))

        search_bar_dataset = tk.Label(search_dataset)
        search_bar_dataset.grid(row=0, column=0)
        search_bar_dataset.config(image=self.search_bar)

        self.text_meta = tk.Text(search_dataset, height=1, width=70, bd=0, bg="white", fg="grey", highlightthickness=0,
                                 borderwidth=0,
                                 undo=True, autoseparators=True, maxundo=-1, font=("Inter", 18))

        self.text_meta.grid(row=0, column=0)
        self.text_meta.insert("1.0", "Insert dataset ID (and hit enter)")

        self.text_meta.bind('<FocusOut>', self.on_text_focus_out)
        self.text_meta.bind('<FocusIn>', self.on_text_focus_in)
        self.text_meta.bind("<Return>", self.on_return)

        results_frame = tk.Frame(search_dataset)
        results_frame.grid(row=1, column=0, sticky='nsew')

        self.results = ttk.Treeview(results_frame)
        self.results["columns"] = ("ID", "Name", "Holder", "Description")
        self.results.heading("#0", text='')
        self.results.heading("ID", text='ID')
        self.results.heading("Name", text='Name')
        self.results.heading("Holder", text='Holder')
        self.results.heading("Description", text="Description")
        self.results.column("#0", width=0)
        self.results.column("ID", width=210)
        self.results.column("Name", width=210)
        self.results.column("Holder", width=110)
        self.results.column("Description", width=440)
        self.results.bind("<<TreeviewSelect>>", self.on_select)

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results.yview)
        self.results.configure(yscrollcommand=scrollbar.set)

        for i in range(20):
            self.results.insert("", "end", values=("", "", "", ""))

        self.results.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        info_frame = tk.Frame(self)
        info_frame.grid(row=2, column=0, sticky='nsew')

        name_label_text = tk.Label(info_frame)
        name_label_text.config(text='Dataset name:  ')
        name_label_text.grid(row=0, column=0, sticky='w')

        self.name_label = tk.Label(info_frame)
        self.name_label.config(background='white', text="                 ")
        self.name_label.grid(row=0, column=1, sticky='w')

        tk.Label(info_frame).grid(row=1, column=0)

        id_label_text = tk.Label(info_frame)
        id_label_text.config(text='Dataset ID:  ')
        id_label_text.grid(row=2, column=0, sticky='w')

        self.id_label = tk.Label(info_frame)
        self.id_label.config(background='white', text="                 ")
        self.id_label.grid(row=2, column=1, sticky='w')

        tk.Label(info_frame).grid(row=3, column=0)

        holder_label_text = tk.Label(info_frame)
        holder_label_text.config(text='Dataset holder:  ')
        holder_label_text.grid(row=4, column=0, sticky='w')

        self.holder_label = tk.Label(info_frame)
        self.holder_label.config(background='white', text="                 ")
        self.holder_label.grid(row=4, column=1, sticky='w')

        tk.Label(info_frame).grid(row=5, column=0)

        description_label_text = tk.Label(info_frame)
        description_label_text.config(text='Dataset description:  ')
        description_label_text.grid(row=6, column=0, sticky='w')

        description_label_frame = tk.Frame(info_frame)
        description_label_frame.grid(row=6, column=1, sticky='w')

        self.description_label = tk.Text(description_label_frame, width=100, height=5)
        self.description_label.grid(row=0, column=0, sticky='nsew')

        scrollbar1 = tk.Scrollbar(description_label_frame, command=self.description_label.yview)
        scrollbar1.grid(row=0, column=1, sticky="ns")

        self.description_label.config(yscrollcommand=scrollbar1.set)

        tk.Label(info_frame).grid(row=7, column=0)

        update_label_text = tk.Label(info_frame)
        update_label_text.config(text='Last update:  ')
        update_label_text.grid(row=8, column=0, sticky='w')

        self.update_label = tk.Label(info_frame)
        self.update_label.config(background='white', text="                 ")
        self.update_label.grid(row=8, column=1, sticky='w')

        select_frame = tk.Frame(self)
        select_frame.grid(row=3, column=0, sticky='nsew')

        tk.Label(select_frame, width=111).grid(row=0, column=0)

        self.select_des_label = tk.Label(select_frame, text='SELECT', fg='light grey')
        self.select_des_label.grid(row=0, column=1)

        self.select_label_image = ImageTk.PhotoImage(Image.open("gui_elements/right.png").resize((25, 25)))

        select_label = tk.Label(select_frame)
        select_label.grid(row=0, column=2, sticky='e')
        select_label.config(image=self.select_label_image)
        select_label.bind('<Enter>', self.on_select_enter)
        select_label.bind('<Leave>', self.on_select_leave)
        select_label.bind('<Button-1>', lambda x: controller.show_frame(EvaluationPage))



        search_bar_holder = tk.Label(search_holder)
        search_bar_holder.grid(row=0, column=0)
        search_bar_holder.config(image=self.search_bar)

        self.text_meta_holder = tk.Text(search_holder, height=1, width=70, bd=0, bg="white", fg="grey", highlightthickness=0,
                                 borderwidth=0,
                                 undo=True, autoseparators=True, maxundo=-1, font=("Inter", 18))

        self.text_meta_holder.grid(row=0, column=0)
        self.text_meta_holder.insert("1.0", "Insert holder ID (and hit enter)")

        self.text_meta_holder.bind('<FocusOut>', self.on_text_focus_out_holder)
        self.text_meta_holder.bind('<FocusIn>', self.on_text_focus_in_holder)
        self.text_meta_holder.bind("<Return>", self.on_return_holder)

        results_frame_holder = tk.Frame(search_holder)
        results_frame_holder.grid(row=1, column=0, sticky='nsew')

        self.results_holder = ttk.Treeview(results_frame_holder)
        self.results_holder["columns"] = ("ID", "Name", "Description")
        self.results_holder.heading("#0", text='')
        self.results_holder.heading("ID", text='ID')
        self.results_holder.heading("Name", text='Name')
        self.results_holder.heading("Description", text="Description")
        self.results_holder.column("#0", width=0)
        self.results_holder.column("ID", width=300)
        self.results_holder.column("Name", width=300)
        self.results_holder.column("Description", width=400)
        self.results_holder.bind("<<TreeviewSelect>>", self.on_select)

        scrollbar_holder = ttk.Scrollbar(results_frame_holder, orient="vertical", command=self.results_holder.yview)
        self.results_holder.configure(yscrollcommand=scrollbar_holder.set)

        for i in range(20):
            self.results_holder.insert("", "end", values=("", "", "", ""))

        self.results_holder.grid(row=0, column=0, sticky='nsew')
        scrollbar_holder.grid(row=0, column=1, sticky='ns')

        # info_frame_holder = tk.Frame(self)
        # info_frame_holder.grid(row=2, column=0, sticky='nsew')
        #
        # name_label_text_holder = tk.Label(info_frame_holder)
        # name_label_text_holder.config(text='Nome dataset:  ')
        # name_label_text_holder.grid(row=0, column=0, sticky='w')
        #
        # self.name_label_holder = tk.Label(info_frame)
        # self.name_label_holder.config(background='white', text="                 ")
        # self.name_label_holder.grid(row=0, column=1, sticky='w')
        #
        # tk.Label(info_frame_holder).grid(row=1, column=0)
        #
        # id_label_text_holder = tk.Label(info_frame_holder)
        # id_label_text_holder.config(text='ID dataset:  ')
        # id_label_text_holder.grid(row=2, column=0, sticky='w')
        #
        # self.id_label_holder = tk.Label(info_frame_holder)
        # self.id_label_holder.config(background='white', text="                 ")
        # self.id_label_holder.grid(row=2, column=1, sticky='w')
        #
        # tk.Label(info_frame_holder).grid(row=3, column=0)

        # holder_label_text = tk.Label(info_frame)
        # holder_label_text.config(text='Holder dataset:  ')
        # holder_label_text.grid(row=4, column=0, sticky='w')
        #
        # self.holder_label = tk.Label(info_frame)
        # self.holder_label.config(background='white', text="                 ")
        # self.holder_label.grid(row=4, column=1, sticky='w')

        # tk.Label(info_frame_holder).grid(row=4, column=0)
        #
        # description_label_text_holder = tk.Label(info_frame_holder)
        # description_label_text_holder.config(text='Descrizione dataset:  ')
        # description_label_text_holder.grid(row=6, column=0, sticky='w')
        #
        # description_label_frame_holder = tk.Frame(info_frame_holder)
        # description_label_frame_holder.grid(row=6, column=1, sticky='w')
        #
        # self.description_label_holder = tk.Text(description_label_frame_holder, width=100, height=5)
        # self.description_label_holder.grid(row=0, column=0, sticky='nsew')
        #
        # scrollbar2 = tk.Scrollbar(description_label_frame, command=self.description_label.yview)
        # scrollbar2.grid(row=0, column=1, sticky="ns")
        #
        # self.description_label.config(yscrollcommand=scrollbar2.set)
        #
        # tk.Label(info_frame_holder).grid(row=7, column=0)
        #
        # update_label_text_holder = tk.Label(info_frame_holder)
        # update_label_text_holder.config(text='Data ultimo update:  ')
        # update_label_text_holder.grid(row=8, column=0, sticky='w')
        #
        # self.update_label_holder = tk.Label(info_frame_holder)
        # self.update_label_holder.config(background='white', text="                 ")
        # self.update_label_holder.grid(row=8, column=1, sticky='w')
        #
        # select_frame_holder = tk.Frame(self)
        # select_frame_holder.grid(row=3, column=0, sticky='nsew')
        #
        # tk.Label(select_frame_holder, width=111).grid(row=0, column=0)
        #
        # self.select_des_label_holder = tk.Label(select_frame_holder, text='SELEZIONA', fg='light grey')
        # self.select_des_label_holder.grid(row=0, column=1)

        # select_label_holder = tk.Label(select_frame_holder)
        # select_label_holder.grid(row=0, column=2, sticky='e')
        # select_label_holder.config(image=self.select_label_image)
        # select_label_holder.bind('<Enter>', self.on_select_enter_holder)
        # select_label_holder.bind('<Leave>', self.on_select_leave_holder)
        # select_label_holder.bind('<Button-1>', lambda x: controller.show_frame(EvaluationPage))

    def home_call(self, event, controller):
        home_event = {'type': 'home_clicked'}
        event_bus.publish(home_event)
        controller.show_frame(StartPage)

    # def on_select_enter_holder(self, e):
    #     self.select_des_label_holder.config(fg='black')
    #
    # def on_select_leave_holder(self, e):
    #     self.select_des_label_holder.config(fg='light grey')

    def on_select_enter(self, e):
        self.select_des_label.config(fg='black')

    def on_select_leave(self, e):
        self.select_des_label.config(fg='light grey')

    def on_text_focus_out_holder(self, e):
        if not self.text_meta_holder.get("1.0", "end-1c"):
            self.text_meta_holder.delete("1.0", tk.END)
            self.text_meta_holder.insert("1.0", "Inserire l'ID dell'holder (e premi invio)")

    def on_text_focus_in_holder(self, e):
        if self.text_meta_holder.get("1.0", "end-1c") == "Inserire l'ID dell'holder (e premi invio)":
            self.text_meta_holder.delete("1.0", tk.END)

    def on_select_holder(self, e):
        selected_el = self.results_holder.selection()
        values = None
        devalue = []
        for item in selected_el:
            values = self.results.item(item)['values']
            for value in values[0]:
                if not value:
                    value = ''
                devalue.append(value)
        if values:
            self.name_label.config(text=self.results.item(selected_el[0])['values'][1])
            self.id_label.config(text=self.results.item(selected_el[0])['values'][0])
            # self.holder_label.config(text=self.results.item(selected_el[0])['values'][2])
            self.description_label.delete("1.0", tk.END)
            self.description_label.insert("1.0", self.results.item(selected_el[0])['values'][3])
            self.update_label.config(text=self.results.item(selected_el[0])['values'][4])
            event_bus.publish({'type': 'chosen_holder',
                               'id': self.results.item(selected_el[0])['values'][0]})

    def on_return_holder(self, e):
        data_found = database.search_holder(self.text_meta_holder.get("1.0", "end-1c"))
        self.results_holder.delete(*self.results_holder.get_children())
        self.text_meta_holder.delete("1.0", tk.END)
        for data in data_found:
            values = []
            for value in data:
                if value is None:
                    value = ""
                values.append(value)
            self.results_holder.insert("", "end", values=values)

    def on_text_focus_out(self, e):
        if not self.text_meta.get("1.0", "end-1c"):
            self.text_meta.delete("1.0", tk.END)
            self.text_meta.insert("1.0", "Inserire l'ID del dataset (e premi invio)")

    def on_text_focus_in(self, e):
        if self.text_meta.get("1.0", "end-1c") == "Inserire l'ID del dataset (e premi invio)":
            self.text_meta.delete("1.0", tk.END)

    def on_select(self, e):
        if self.search_frame.index(self.search_frame.select()) == 0:
            selected_el = self.results.selection()
            values = None
            for item in selected_el:
                values = self.results.item(item)['values']
            if values:
                self.name_label.config(text=self.results.item(selected_el[0])['values'][1])
                self.id_label.config(text=self.results.item(selected_el[0])['values'][0])
                self.holder_label.config(text=self.results.item(selected_el[0])['values'][2])
                self.description_label.delete("1.0", tk.END)
                self.description_label.insert("1.0", self.results.item(selected_el[0])['values'][3])
                self.update_label.config(text=self.results.item(selected_el[0])['values'][4])
                event_bus.publish({'type': 'chosen_dataset',
                                   'id': self.results.item(selected_el[0])['values'][0]})

        elif self.search_frame.index(self.search_frame.select()) == 1:
            selected_el = self.results_holder.selection()
            values = None
            for item in selected_el:
                values = self.results_holder.item(item)['values']
            if values:
                self.name_label.config(text=self.results_holder.item(selected_el[0])['values'][1])
                self.id_label.config(text=self.results_holder.item(selected_el[0])['values'][0])
                # self.holder_label.config(text=self.results.item(selected_el[0])['values'][2])
                self.description_label.delete("1.0", tk.END)
                self.description_label.insert("1.0", self.results_holder.item(selected_el[0])['values'][2])
                # self.update_label.config(text=self.results.item(selected_el[0])['values'][4])
                event_bus.publish({'type': 'chosen_holder',
                                   'id': self.results_holder.item(selected_el[0])['values'][0]})


    def on_return(self, e):
        data_found = database.search_dataset(self.text_meta.get("1.0", "end-1c"))
        self.results.delete(*self.results.get_children())
        self.text_meta.delete("1.0", tk.END)
        for data in data_found:
            self.results.insert("", "end", values=data)

    def show_tooltip(self, event):
        if not self.tooltip_visible:
            color = self.canvas.itemconfig(self.oval)['fill'][4]
            if color == 'red':
                self.tooltip.config(text="Operazioni di controllo sul sistema in corso prima dell'aggiornamento")
            elif color == 'yellow':
                self.tooltip.config(text="Aggiornamento del database in corso")
            elif color == 'green':
                self.tooltip.config(text="Il database è aggiornato")

            self.tooltip.update_idletasks()  # Aggiorna le dimensioni del tooltip

            x, y, w, h = self.canvas.coords(self.oval)
            tooltip_width = self.tooltip.winfo_width()
            tooltip_height = self.tooltip.winfo_height()
            tooltip_x = x + (w - tooltip_width) / 2
            tooltip_y = y + (h - tooltip_height) / 2

            self.tooltip.place(x=tooltip_x + 500 , y=tooltip_y)
            self.tooltip_visible = True

    def hide_tooltip(self, event):
        if self.tooltip_visible:
            self.tooltip.place_forget()
            self.tooltip_visible = False

    def handle_event(self, event):
        if event['type'] == 'portal_start':
            self.canvas.itemconfig(self.oval, fill='yellow', outline='yellow')
        elif event['type'] == 'update_done_toplevel':
            self.canvas.itemconfig(self.oval, fill='green', outline='green')
        elif event['type'] == 'home_clicked':
            if self.text_meta.get("1.0", "end-1c"):
                self.text_meta.delete("1.0", tk.END)
                self.text_meta.insert("1.0", "Inserire l'ID del dataset (e premi invio)")
            self.results.delete(*self.results.get_children())
            self.name_label.config(text='')
            self.id_label.config(text='')
            self.holder_label.config(text='')
            if self.description_label.get("1.0", "end-1c"):
                self.description_label.delete("1.0", tk.END)
            self.update_label.config(text='')


class PortalPageITA(tk.Frame):
    mprint('LOADING PORTAL PAGE', bc.ENDC, 0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='white')

        event_bus.subscribe(self)

        self.logo_frame = tk.Frame(self, background='white')
        self.logo_frame.grid(column=0, row=0, sticky='w')

        self.logo = ImageTk.PhotoImage(Image.open("gui_elements/eufair.png").resize((200, 160)))
        logo_label = tk.Label(self.logo_frame, background='white')
        logo_label.grid(row=0, column=0, sticky='e')
        logo_label.config(background="white", image=self.logo)

        blank = tk.Label(self.logo_frame, background='white', width=85, height=1)
        blank.grid(row=0, column=1)

        self.home = ImageTk.PhotoImage(Image.open("gui_elements/home.png").resize((30, 30)))
        home_butt = tk.Label(blank, background='white')
        home_butt.grid(row=0, column=0, sticky='sw')
        home_butt.config(background="white", image=self.home)
        home_butt.bind('<Button-1>', lambda event: self.home_call(event, controller))

        self.canvas = tk.Canvas(self.logo_frame, width=200, height=200, background='white', highlightbackground='white')
        self.canvas.grid(row=0, column=2, sticky='e')

        # Coordinata del centro del pallino
        x = 190
        y = 15

        # Raggio del pallino
        raggio = 10

        self.oval = self.canvas.create_oval(x - raggio, y - raggio, x + raggio, y + raggio, fill='red', outline= 'red')

        self.tooltip = tk.Label(self.logo_frame, bg="yellow", relief="solid", borderwidth=1)
        self.tooltip_visible = False

        self.canvas.tag_bind(self.oval, "<Enter>", self.show_tooltip)
        self.canvas.tag_bind(self.oval, "<Leave>", self.hide_tooltip)

        self.search_frame = ttk.Notebook(self)

        self.search_frame.grid(row=1, column=0, sticky="nsew")
        search_dataset = ttk.Frame(self.search_frame)
        search_holder = ttk.Frame(self.search_frame)
        self.search_frame.add(search_dataset, text='Ricerca per dataset')
        self.search_frame.add(search_holder, text='Ricerca per holder')

        self.search_bar = ImageTk.PhotoImage(Image.open("gui_elements/europa_inbox.png").resize((1010, 35)))

        search_bar_dataset = tk.Label(search_dataset)
        search_bar_dataset.grid(row=0, column=0)
        search_bar_dataset.config(image=self.search_bar)

        self.text_meta = tk.Text(search_dataset, height=1, width=70, bd=0, bg="white", fg="grey", highlightthickness=0,
                                 borderwidth=0,
                                 undo=True, autoseparators=True, maxundo=-1, font=("Inter", 18))

        self.text_meta.grid(row=0, column=0)
        self.text_meta.insert("1.0", "Inserire l'ID del dataset (e premi invio)")

        self.text_meta.bind('<FocusOut>', self.on_text_focus_out)
        self.text_meta.bind('<FocusIn>', self.on_text_focus_in)
        self.text_meta.bind("<Return>", self.on_return)

        results_frame = tk.Frame(search_dataset)
        results_frame.grid(row=1, column=0, sticky='nsew')

        self.results = ttk.Treeview(results_frame)
        self.results["columns"] = ("ID", "Nome", "Holder", "Descrizione")
        self.results.heading("#0", text='')
        self.results.heading("ID", text='ID')
        self.results.heading("Nome", text='Nome')
        self.results.heading("Holder", text='Holder')
        self.results.heading("Descrizione", text="Descrizione")
        self.results.column("#0", width=0)
        self.results.column("ID", width=210)
        self.results.column("Nome", width=210)
        self.results.column("Holder", width=110)
        self.results.column("Descrizione", width=440)
        self.results.bind("<<TreeviewSelect>>", self.on_select)

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results.yview)
        self.results.configure(yscrollcommand=scrollbar.set)

        for i in range(20):
            self.results.insert("", "end", values=("", "", "", ""))

        self.results.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        info_frame = tk.Frame(self)
        info_frame.grid(row=2, column=0, sticky='nsew')

        name_label_text = tk.Label(info_frame)
        name_label_text.config(text='Nome dataset:  ')
        name_label_text.grid(row=0, column=0, sticky='w')

        self.name_label = tk.Label(info_frame)
        self.name_label.config(background='white', text="                 ")
        self.name_label.grid(row=0, column=1, sticky='w')

        tk.Label(info_frame).grid(row=1, column=0)

        id_label_text = tk.Label(info_frame)
        id_label_text.config(text='ID dataset:  ')
        id_label_text.grid(row=2, column=0, sticky='w')

        self.id_label = tk.Label(info_frame)
        self.id_label.config(background='white', text="                 ")
        self.id_label.grid(row=2, column=1, sticky='w')

        tk.Label(info_frame).grid(row=3, column=0)

        holder_label_text = tk.Label(info_frame)
        holder_label_text.config(text='Holder dataset:  ')
        holder_label_text.grid(row=4, column=0, sticky='w')

        self.holder_label = tk.Label(info_frame)
        self.holder_label.config(background='white', text="                 ")
        self.holder_label.grid(row=4, column=1, sticky='w')

        tk.Label(info_frame).grid(row=5, column=0)

        description_label_text = tk.Label(info_frame)
        description_label_text.config(text='Descrizione dataset:  ')
        description_label_text.grid(row=6, column=0, sticky='w')

        description_label_frame = tk.Frame(info_frame)
        description_label_frame.grid(row=6, column=1, sticky='w')

        self.description_label = tk.Text(description_label_frame, width=100, height=5)
        self.description_label.grid(row=0, column=0, sticky='nsew')

        scrollbar1 = tk.Scrollbar(description_label_frame, command=self.description_label.yview)
        scrollbar1.grid(row=0, column=1, sticky="ns")

        self.description_label.config(yscrollcommand=scrollbar1.set)

        tk.Label(info_frame).grid(row=7, column=0)

        update_label_text = tk.Label(info_frame)
        update_label_text.config(text='Data ultimo update:  ')
        update_label_text.grid(row=8, column=0, sticky='w')

        self.update_label = tk.Label(info_frame)
        self.update_label.config(background='white', text="                 ")
        self.update_label.grid(row=8, column=1, sticky='w')

        select_frame = tk.Frame(self)
        select_frame.grid(row=3, column=0, sticky='nsew')

        tk.Label(select_frame, width=111).grid(row=0, column=0)

        self.select_des_label = tk.Label(select_frame, text='SELEZIONA', fg='light grey')
        self.select_des_label.grid(row=0, column=1)

        self.select_label_image = ImageTk.PhotoImage(Image.open("gui_elements/right.png").resize((25, 25)))

        select_label = tk.Label(select_frame)
        select_label.grid(row=0, column=2, sticky='e')
        select_label.config(image=self.select_label_image)
        select_label.bind('<Enter>', self.on_select_enter)
        select_label.bind('<Leave>', self.on_select_leave)
        select_label.bind('<Button-1>', lambda x: controller.show_frame(EvaluationPage))

        search_bar_holder = tk.Label(search_holder)
        search_bar_holder.grid(row=0, column=0)
        search_bar_holder.config(image=self.search_bar)

        self.text_meta_holder = tk.Text(search_holder, height=1, width=70, bd=0, bg="white", fg="grey", highlightthickness=0,
                                 borderwidth=0,
                                 undo=True, autoseparators=True, maxundo=-1, font=("Inter", 18))

        self.text_meta_holder.grid(row=0, column=0)
        self.text_meta_holder.insert("1.0", "Inserire l'ID dell'holder (e premi invio)")

        self.text_meta_holder.bind('<FocusOut>', self.on_text_focus_out_holder)
        self.text_meta_holder.bind('<FocusIn>', self.on_text_focus_in_holder)
        self.text_meta_holder.bind("<Return>", self.on_return_holder)

        results_frame_holder = tk.Frame(search_holder)
        results_frame_holder.grid(row=1, column=0, sticky='nsew')

        self.results_holder = ttk.Treeview(results_frame_holder)
        self.results_holder["columns"] = ("ID", "Nome", "Descrizione")
        self.results_holder.heading("#0", text='')
        self.results_holder.heading("ID", text='ID')
        self.results_holder.heading("Nome", text='Nome')
        self.results_holder.heading("Descrizione", text="Descrizione")
        self.results_holder.column("#0", width=0)
        self.results_holder.column("ID", width=300)
        self.results_holder.column("Nome", width=300)
        self.results_holder.column("Descrizione", width=400)
        self.results_holder.bind("<<TreeviewSelect>>", self.on_select)

        scrollbar_holder = ttk.Scrollbar(results_frame_holder, orient="vertical", command=self.results_holder.yview)
        self.results_holder.configure(yscrollcommand=scrollbar_holder.set)

        for i in range(20):
            self.results_holder.insert("", "end", values=("", "", "", ""))

        self.results_holder.grid(row=0, column=0, sticky='nsew')
        scrollbar_holder.grid(row=0, column=1, sticky='ns')

        # info_frame_holder = tk.Frame(self)
        # info_frame_holder.grid(row=2, column=0, sticky='nsew')
        #
        # name_label_text_holder = tk.Label(info_frame_holder)
        # name_label_text_holder.config(text='Nome dataset:  ')
        # name_label_text_holder.grid(row=0, column=0, sticky='w')
        #
        # self.name_label_holder = tk.Label(info_frame)
        # self.name_label_holder.config(background='white', text="                 ")
        # self.name_label_holder.grid(row=0, column=1, sticky='w')
        #
        # tk.Label(info_frame_holder).grid(row=1, column=0)
        #
        # id_label_text_holder = tk.Label(info_frame_holder)
        # id_label_text_holder.config(text='ID dataset:  ')
        # id_label_text_holder.grid(row=2, column=0, sticky='w')
        #
        # self.id_label_holder = tk.Label(info_frame_holder)
        # self.id_label_holder.config(background='white', text="                 ")
        # self.id_label_holder.grid(row=2, column=1, sticky='w')
        #
        # tk.Label(info_frame_holder).grid(row=3, column=0)

        # holder_label_text = tk.Label(info_frame)
        # holder_label_text.config(text='Holder dataset:  ')
        # holder_label_text.grid(row=4, column=0, sticky='w')
        #
        # self.holder_label = tk.Label(info_frame)
        # self.holder_label.config(background='white', text="                 ")
        # self.holder_label.grid(row=4, column=1, sticky='w')

        # tk.Label(info_frame_holder).grid(row=4, column=0)
        #
        # description_label_text_holder = tk.Label(info_frame_holder)
        # description_label_text_holder.config(text='Descrizione dataset:  ')
        # description_label_text_holder.grid(row=6, column=0, sticky='w')
        #
        # description_label_frame_holder = tk.Frame(info_frame_holder)
        # description_label_frame_holder.grid(row=6, column=1, sticky='w')
        #
        # self.description_label_holder = tk.Text(description_label_frame_holder, width=100, height=5)
        # self.description_label_holder.grid(row=0, column=0, sticky='nsew')
        #
        # scrollbar2 = tk.Scrollbar(description_label_frame, command=self.description_label.yview)
        # scrollbar2.grid(row=0, column=1, sticky="ns")
        #
        # self.description_label.config(yscrollcommand=scrollbar2.set)
        #
        # tk.Label(info_frame_holder).grid(row=7, column=0)
        #
        # update_label_text_holder = tk.Label(info_frame_holder)
        # update_label_text_holder.config(text='Data ultimo update:  ')
        # update_label_text_holder.grid(row=8, column=0, sticky='w')
        #
        # self.update_label_holder = tk.Label(info_frame_holder)
        # self.update_label_holder.config(background='white', text="                 ")
        # self.update_label_holder.grid(row=8, column=1, sticky='w')
        #
        # select_frame_holder = tk.Frame(self)
        # select_frame_holder.grid(row=3, column=0, sticky='nsew')
        #
        # tk.Label(select_frame_holder, width=111).grid(row=0, column=0)
        #
        # self.select_des_label_holder = tk.Label(select_frame_holder, text='SELEZIONA', fg='light grey')
        # self.select_des_label_holder.grid(row=0, column=1)

        # select_label_holder = tk.Label(select_frame_holder)
        # select_label_holder.grid(row=0, column=2, sticky='e')
        # select_label_holder.config(image=self.select_label_image)
        # select_label_holder.bind('<Enter>', self.on_select_enter_holder)
        # select_label_holder.bind('<Leave>', self.on_select_leave_holder)
        # select_label_holder.bind('<Button-1>', lambda x: controller.show_frame(EvaluationPage))

    def home_call(self, event, controller):
        home_event = {'type': 'home_clicked'}
        event_bus.publish(home_event)
        controller.show_frame(StartPage)

    # def on_select_enter_holder(self, e):
    #     self.select_des_label_holder.config(fg='black')
    #
    # def on_select_leave_holder(self, e):
    #     self.select_des_label_holder.config(fg='light grey')

    def on_select_enter(self, e):
        self.select_des_label.config(fg='black')

    def on_select_leave(self, e):
        self.select_des_label.config(fg='light grey')

    def on_text_focus_out_holder(self, e):
        if not self.text_meta_holder.get("1.0", "end-1c"):
            self.text_meta_holder.delete("1.0", tk.END)
            self.text_meta_holder.insert("1.0", "Inserire l'ID dell'holder (e premi invio)")

    def on_text_focus_in_holder(self, e):
        if self.text_meta_holder.get("1.0", "end-1c") == "Inserire l'ID dell'holder (e premi invio)":
            self.text_meta_holder.delete("1.0", tk.END)

    def on_select_holder(self, e):
        selected_el = self.results_holder.selection()
        values = None
        devalue = []
        for item in selected_el:
            values = self.results.item(item)['values']
            for value in values[0]:
                if not value:
                    value = ''
                devalue.append(value)
        if values:
            self.name_label.config(text=self.results.item(selected_el[0])['values'][1])
            self.id_label.config(text=self.results.item(selected_el[0])['values'][0])
            # self.holder_label.config(text=self.results.item(selected_el[0])['values'][2])
            self.description_label.delete("1.0", tk.END)
            self.description_label.insert("1.0", self.results.item(selected_el[0])['values'][3])
            self.update_label.config(text=self.results.item(selected_el[0])['values'][4])
            event_bus.publish({'type': 'chosen_holder',
                               'id': self.results.item(selected_el[0])['values'][0]})

    def on_return_holder(self, e):
        data_found = database.search_holder(self.text_meta_holder.get("1.0", "end-1c"))
        self.results_holder.delete(*self.results_holder.get_children())
        self.text_meta_holder.delete("1.0", tk.END)
        for data in data_found:
            values = []
            for value in data:
                if value is None:
                    value = ""
                values.append(value)
            self.results_holder.insert("", "end", values=values)

    def on_text_focus_out(self, e):
        if not self.text_meta.get("1.0", "end-1c"):
            self.text_meta.delete("1.0", tk.END)
            self.text_meta.insert("1.0", "Inserire l'ID del dataset (e premi invio)")

    def on_text_focus_in(self, e):
        if self.text_meta.get("1.0", "end-1c") == "Inserire l'ID del dataset (e premi invio)":
            self.text_meta.delete("1.0", tk.END)

    def on_select(self, e):
        if self.search_frame.index(self.search_frame.select()) == 0:
            selected_el = self.results.selection()
            values = None
            for item in selected_el:
                values = self.results.item(item)['values']
            if values:
                self.name_label.config(text=self.results.item(selected_el[0])['values'][1])
                self.id_label.config(text=self.results.item(selected_el[0])['values'][0])
                self.holder_label.config(text=self.results.item(selected_el[0])['values'][2])
                self.description_label.delete("1.0", tk.END)
                self.description_label.insert("1.0", self.results.item(selected_el[0])['values'][3])
                self.update_label.config(text=self.results.item(selected_el[0])['values'][4])
                event_bus.publish({'type': 'chosen_dataset',
                                   'id': self.results.item(selected_el[0])['values'][0]})

        elif self.search_frame.index(self.search_frame.select()) == 1:
            selected_el = self.results_holder.selection()
            values = None
            for item in selected_el:
                values = self.results_holder.item(item)['values']
            if values:
                self.name_label.config(text=self.results_holder.item(selected_el[0])['values'][1])
                self.id_label.config(text=self.results_holder.item(selected_el[0])['values'][0])
                # self.holder_label.config(text=self.results.item(selected_el[0])['values'][2])
                self.description_label.delete("1.0", tk.END)
                self.description_label.insert("1.0", self.results_holder.item(selected_el[0])['values'][2])
                # self.update_label.config(text=self.results.item(selected_el[0])['values'][4])
                event_bus.publish({'type': 'chosen_holder',
                                   'id': self.results_holder.item(selected_el[0])['values'][0]})


    def on_return(self, e):
        data_found = database.search_dataset(self.text_meta.get("1.0", "end-1c"))
        self.results.delete(*self.results.get_children())
        self.text_meta.delete("1.0", tk.END)
        for data in data_found:
            self.results.insert("", "end", values=data)

    def show_tooltip(self, event):
        if not self.tooltip_visible:
            color = self.canvas.itemconfig(self.oval)['fill'][4]
            if color == 'red':
                self.tooltip.config(text="Operazioni di controllo sul sistema in corso prima dell'aggiornamento")
            elif color == 'yellow':
                self.tooltip.config(text="Aggiornamento del database in corso")
            elif color == 'green':
                self.tooltip.config(text="Il database è aggiornato")

            self.tooltip.update_idletasks()  # Aggiorna le dimensioni del tooltip

            x, y, w, h = self.canvas.coords(self.oval)
            tooltip_width = self.tooltip.winfo_width()
            tooltip_height = self.tooltip.winfo_height()
            tooltip_x = x + (w - tooltip_width) / 2
            tooltip_y = y + (h - tooltip_height) / 2

            self.tooltip.place(x=tooltip_x + 500 , y=tooltip_y)
            self.tooltip_visible = True

    def hide_tooltip(self, event):
        if self.tooltip_visible:
            self.tooltip.place_forget()
            self.tooltip_visible = False

    def handle_event(self, event):
        if event['type'] == 'portal_start':
            self.canvas.itemconfig(self.oval, fill='yellow', outline='yellow')
        elif event['type'] == 'update_done_toplevel':
            self.canvas.itemconfig(self.oval, fill='green', outline='green')
        elif event['type'] == 'home_clicked':
            if self.text_meta.get("1.0", "end-1c"):
                self.text_meta.delete("1.0", tk.END)
                self.text_meta.insert("1.0", "Inserire l'ID del dataset (e premi invio)")
            self.results.delete(*self.results.get_children())
            self.name_label.config(text='')
            self.id_label.config(text='')
            self.holder_label.config(text='')
            if self.description_label.get("1.0", "end-1c"):
                self.description_label.delete("1.0", tk.END)
            self.update_label.config(text='')


class EvaluationPage(tk.Frame):
    mprint('LOADING EVALUATION PAGE', bc.ENDC, 0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='white')

        event_bus.subscribe(self)
        self.controller = controller
        self.logo_frame = tk.Frame(self, background='white')
        self.logo_frame.grid(column=0, row=0, sticky='w')

        self.logo = ImageTk.PhotoImage(Image.open("gui_elements/eufair.png").resize((200, 160)))
        logo_label = tk.Label(self.logo_frame, background='white')
        logo_label.grid(row=0, column=0, sticky='e')
        logo_label.config(background="white", image=self.logo)

        blank = tk.Label(self.logo_frame, background='white')
        blank.grid(row=0, column=1)

        self.home = ImageTk.PhotoImage(Image.open("gui_elements/home.png").resize((30, 30)))
        home_butt = tk.Label(blank, background='white')
        home_butt.grid(row=0, column=0, sticky='sw')
        home_butt.config(background="white", image=self.home)
        home_butt.bind('<Button-1>', lambda event: self.home_call(event, controller))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.choose_frame = tk.Frame(self)
        self.choose_frame.grid(row=1, column=0)
        self.choose_frame.config(background='white')


        # Opzioni per la casella di selezione 1
        self.options1 = ["dati.gov.it", "data.europa.eu", "native"]
        self.option1 = tk.StringVar()
        self.option1.set('chose portal')

        # Creazione della casella di selezione 1
        option_menu1 = tk.OptionMenu(self.choose_frame, self.option1, *self.options1)
        option_menu1.grid(row=0, column=0, padx=5, pady=5)
        option_menu1.config(background='white')

        # Opzioni per la casella di selezione 2
        self.options2 = ["DCAT_AP", "DCAT_AP-IT", "merged"]
        self.option2 = tk.StringVar()
        self.option2.set('chose method')

        # Creazione della casella di selezione 2
        option_menu2 = tk.OptionMenu(self.choose_frame, self.option2, *self.options2)
        option_menu2.grid(row=0, column=1, padx=5, pady=5)
        option_menu2.config(background='white')

        button = tk.Button(self.choose_frame, text="Invio", command=self.handle_button_click, background='white')
        button.grid(row=0, column=2, padx=5, pady=5)

        file_frame = tk.Frame(self, background='white')
        file_frame.grid(row=3,column=0)

        self.file_label = tk.Label(file_frame, background='white', text='')
        self.file_label.grid(row=0, column=0, sticky='nsew')

        self.dataset_id = ''

        self.holder_id = ''

        self.file_list = []


        self.canvas = self.plot_results(results_zero, self)
        self.canvas.get_tk_widget().grid(row=2, column=0)

    def go_to_file(self, e):
        event_bus.publish({'type': 'chosen_file',
                           'files': self.file_list})
        self.controller.show_frame(FileEvaluationPage)

    def go_to_file_holder(self, e):
        event_bus.publish({'type': 'chosen_file_holder'})
        self.controller.show_frame(FileEvaluationPage)

    def handle_button_click(self):
        results = database.get_last_meta_eval(self.dataset_id, self.option1.get(), self.option2.get())
        if self.dataset_id and results:
            self.canvas = self.plot_results(results, self)
            self.canvas.get_tk_widget().grid(row=2, column=0)
        elif self.holder_id and database.get_last_meta_eval_holder(self.holder_id, self.option1.get(), self.option2.get()):
            results = database.get_last_meta_eval_holder(self.holder_id, self.option1.get(), self.option2.get())
            self.canvas = self.plot_results(results, self)
            self.canvas.get_tk_widget().grid(row=2, column=0)
        else:
            self.canvas = self.no_results(results_zero, self)
            self.canvas.get_tk_widget().grid(row=2, column=0)

    def no_results(self, results, master):
        fig, axs = plt.subplots(2, 2, figsize=(9, 6))
        axs = axs.flatten()
        for ax in axs:
            ax.text(0.5, 0.5, "NO DATA", horizontalalignment='center', verticalalignment='center', fontsize=12)
            ax.axis('off')

        # Creazione dell'oggetto FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()

        return canvas

    def plot_results(self, results, master):
        try:
            # Crea la figura di Matplotlib e genera il grafico
            fig, axs = plt.subplots(2, 2, figsize=(9, 6))
            axs = axs.flatten()
            titles = list(results.keys())

            metrics = ['min', 'avg', 'max']
            width = 0.2  # Larghezza di ogni colonna

            for i, title in enumerate(titles):
                data = results[title]
                sub_titles = list(data.keys())
                sub_data = [data[key] for key in sub_titles]

                x = range(len(sub_titles))  # Posizioni degli indici x per i gruppi di colonne

                for j, metric in enumerate(metrics):
                    values = [float(sub_data[j][metric]) for j in range(len(sub_titles))]

                    axs[i].bar([xi + j * width for xi in x], values, width=width, label=metric)

                axs[i].set_xticks([xi + width for xi in x])  # Posizionamento dei ticks sull'asse x
                axs[i].set_xticklabels(sub_titles)
                axs[i].set_title(title)
                axs[i].legend()
        except:
            # In caso di errore, genera i 4 grafici vuoti
            fig, axs = plt.subplots(2, 2, figsize=(9, 6))
            axs = axs.flatten()
            for ax in axs:
                ax.text(0.5, 0.5, "ERROR", horizontalalignment='center', verticalalignment='center', fontsize=12)
                ax.axis('off')

        # Creazione dell'oggetto FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()

        return canvas

        # self.populate_content()

    def home_call(self, event, controller):
        home_event = {'type': 'home_clicked'}
        event_bus.publish(home_event)
        controller.show_frame(StartPage)

    def handle_event(self, event):
        if event['type'] == 'chosen_dataset':
            self.dataset_id = event['id']
            self.file_list = database.get_name(self.dataset_id, 'dataset')
            print(self.file_list)

            if self.file_list:
                self.file_label.config(
                    text='Il dataset ha dei file valutati. Per passare alla valutazione dei file clicca qui.',
                    underline=True)
                self.file_label.bind('<Button-1>', self.go_to_file)
            else:
                self.file_label.config(
                    text='',
                    underline=False)
                if '<Button-1>' in self.file_label.bindtags():
                    self.file_label.unbind('<Button-1>')
        elif event['type'] == 'home_clicked':
            self.canvas = self.plot_results(results_zero, self)
            self.canvas.get_tk_widget().grid(row=2, column=0)
            matplotlib.pyplot.close()

        elif event['type'] == 'chosen_holder':
            self.holder_id = event['id']
            self.file_list = database.get_name(self.holder_id, 'holder')
            print(self.file_list)

            if self.file_list:
                self.file_label.config(
                    text="L'holder ha dei file valutati. Per passare alla valutazione dei file clicca qui.",
                    underline=True)
                self.file_label.bind('<Button-1>', self.go_to_file_holder)
            else:
                self.file_label.config(
                    text='',
                    underline=False)
                if '<Button-1>' in self.file_label.bindtags():
                    self.file_label.unbind('<Button-1>')


class LinkFileEvaluationPage(tk.Frame):
    mprint('LOADING link and file EVALUATION PAGE', bc.ENDC, 0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='white')

        event_bus.subscribe(self)
        self.controller = controller
        self.logo_frame = tk.Frame(self, background='white')
        self.logo_frame.grid(column=0, row=0, sticky='w')

        self.logo = ImageTk.PhotoImage(Image.open("gui_elements/eufair.png").resize((200, 160)))
        logo_label = tk.Label(self.logo_frame, background='white')
        logo_label.grid(row=0, column=0, sticky='e')
        logo_label.config(background="white", image=self.logo)

        blank = tk.Label(self.logo_frame, background='white')
        blank.grid(row=0, column=1)

        self.home = ImageTk.PhotoImage(Image.open("gui_elements/home.png").resize((30, 30)))
        home_butt = tk.Label(blank, background='white')
        home_butt.grid(row=0, column=0, sticky='sw')
        home_butt.config(background="white", image=self.home)
        home_butt.bind('<Button-1>', lambda event: self.home_call(event, controller))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.choose_frame = tk.Frame(self)
        self.choose_frame.grid(row=1, column=0)
        self.choose_frame.config(background='white')

        # Opzioni per la casella di selezione 2
        self.options2 = ["DCAT_AP", "DCAT_AP-IT", "merged"]
        self.option2 = tk.StringVar()
        self.option2.set('chose method')

        # Creazione della casella di selezione 2
        option_menu2 = tk.OptionMenu(self.choose_frame, self.option2, *self.options2)
        option_menu2.grid(row=0, column=1, padx=5, pady=5)
        option_menu2.config(background='white')

        button = tk.Button(self.choose_frame, text="Invio", command=self.handle_button_click, background='white')
        button.grid(row=0, column=2, padx=5, pady=5)

        file_frame = tk.Frame(self, background='white')
        file_frame.grid(row=3,column=0)

        self.file_label = tk.Label(file_frame, background='white', text='')
        self.file_label.grid(row=0, column=0, sticky='nsew')

        self.url = ''
        self.file_path = ''

        self.canvas = self.create_graphs(result_zero_linkfile, self)
        self.canvas.get_tk_widget().grid(row=2, column=0)

    def handle_button_click(self):
        if self.url:
            print(self.url)
            results = from_link.try_ckan(self.url)
            print(results)
            self.canvas = self.create_graphs(results[self.option2.get()], self)
            self.canvas.get_tk_widget().grid(row=2, column=0)


    def no_results(self, master):
        fig, axs = plt.subplots(2, 2, figsize=(9, 6))
        axs = axs.flatten()
        for ax in axs:
            ax.text(0.5, 0.5, "NO DATA", horizontalalignment='center', verticalalignment='center', fontsize=12)
            ax.axis('off')

        # Creazione dell'oggetto FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()

        return canvas

    def create_graphs(self, data, master):
        try:
            primary_keys = list(data.keys())  # Chiavi primarie
            num_primary_keys = len(primary_keys)  # Numero di chiavi primarie
            fig, axs = plt.subplots(2, 2, figsize=(9, 6))  # Creazione dei grafici

            for i, primary_key in enumerate(primary_keys):
                secondary_keys = list(data[primary_key].keys())  # Chiavi secondarie per la chiave primaria corrente
                num_secondary_keys = len(secondary_keys)  # Numero di chiavi secondarie

                # Dati per la creazione delle colonne
                values = [data[primary_key][secondary_key] for secondary_key in secondary_keys]
                positions = range(num_secondary_keys)

                # Creazione del grafico a barre per la chiave primaria corrente
                ax = axs[i // 2, i % 2]  # Seleziona il sottoplot corrispondente
                ax.bar(positions, values)
                ax.set_title(primary_key)  # Impostazione del titolo del grafico
                ax.set_xlabel('Chiavi secondarie')  # Etichetta sull'asse x
                ax.set_ylabel('Valori')  # Etichetta sull'asse y

                # Etichette sull'asse x
                ax.set_xticks(positions)
                ax.set_xticklabels(secondary_keys, rotation=45)
        except:
            # In caso di errore, genera i 4 grafici vuoti
            fig, axs = plt.subplots(2, 2, figsize=(9, 6))
            axs = axs.flatten()
            for ax in axs:
                ax.text(0.5, 0.5, "ERROR", horizontalalignment='center', verticalalignment='center', fontsize=12)
                ax.axis('off')

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()

        return canvas

    def home_call(self, event, controller):
        home_event = {'type': 'home_clicked'}
        event_bus.publish(home_event)
        controller.show_frame(StartPage)

    def handle_event(self, event):
        if event['type'] == 'chosen_url':
            self.url = event['url']
        elif event['type'] == 'chosen_file_path':
            self.file_path = event['path']
            print(event)
            print(self.file_path)
            results = from_file.try_file(self.file_path)
            print(results)
            self.choose_frame.grid_remove()

            self.canvas = self.create_graphs(results, self)
            self.canvas.get_tk_widget().grid(row=2, column=0)

        elif event['type'] == 'home_clicked':
            self.url = ''
            self.file_path = ''
            if not self.choose_frame.winfo_viewable():
                self.choose_frame.grid()
            self.canvas = self.create_graphs(result_zero_linkfile, self)
            self.canvas.get_tk_widget().grid(row=2, column=0)
            matplotlib.pyplot.close()




class FileEvaluationPage(tk.Frame):
    mprint('LOADING EVALUATION PAGE', bc.ENDC, 0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='white')

        event_bus.subscribe(self)
        self.holder_mode = 0
        self.logo_frame = tk.Frame(self, background='white')
        self.logo_frame.grid(column=0, row=0, sticky='w')

        self.logo = ImageTk.PhotoImage(Image.open("gui_elements/eufair.png").resize((200, 160)))
        logo_label = tk.Label(self.logo_frame, background='white')
        logo_label.grid(row=0, column=0, sticky='e')
        logo_label.config(background="white", image=self.logo)

        blank = tk.Label(self.logo_frame, background='white')
        blank.grid(row=0, column=1)

        self.home = ImageTk.PhotoImage(Image.open("gui_elements/home.png").resize((30, 30)))
        home_butt = tk.Label(blank, background='white')
        home_butt.grid(row=0, column=0, sticky='sw')
        home_butt.config(background="white", image=self.home)
        home_butt.bind('<Button-1>', lambda event: self.home_call(event, controller))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.dataset_id=''
        self.holder_id=''

        self.file_list = ['']

        self.choose_frame = tk.Frame(self)
        self.choose_frame.grid(row=1, column=0)
        self.choose_frame.config(background='white')

        self.options2 = ["DCAT_AP", "DCAT_AP-IT", "merged"]
        self.option2 = tk.StringVar()
        self.option2.set('chose method')

        option_menu2 = tk.OptionMenu(self.choose_frame, self.option2, *self.options2)
        option_menu2.grid(row=0, column=0, padx=5, pady=5)
        option_menu2.config(background='white')

        self.options3 = self.file_list
        self.option3 = tk.StringVar()
        self.option3.set('chose file')

        self.option_menu3 = tk.OptionMenu(self.choose_frame, self.option3, *self.options3)
        self.option_menu3.grid(row=0, column=1, padx=5, pady=5)
        self.option_menu3.config(background='white')

        button = tk.Button(self.choose_frame, text="Invio", command=self.handle_button_click, background='white')
        button.grid(row=0, column=2, padx=5, pady=5)

        self.canvas = self.plot_results(results_zero, self)
        self.canvas.get_tk_widget().grid(row=2, column=0)

    def handle_button_click(self):
        if self.holder_mode == 0:
            print(self.dataset_id, self.option3.get(), self.option2.get())
            results = database.get_last_data_eval(self.dataset_id, self.option3.get(), self.option2.get())
            print(results)
            if self.dataset_id and results:
                self.canvas = self.plot_results(results, self)
                self.canvas.get_tk_widget().grid(row=2, column=0)
            else:
                self.canvas = self.no_results(results_zero, self)
                self.canvas.get_tk_widget().grid(row=2, column=0)
        else:
            results = database.get_last_data_eval_holder(self.holder_id, self.option2.get())
            if self.holder_id and results:
                self.canvas = self.plot_results(results, self)
                self.canvas.get_tk_widget().grid(row=2, column=0)
            else:
                self.canvas = self.no_results(results_zero, self)
                self.canvas.get_tk_widget().grid(row=2, column=0)

    def no_results(self, results, master):
        fig, axs = plt.subplots(2, 2, figsize=(9, 6))
        axs = axs.flatten()
        for ax in axs:
            ax.text(0.5, 0.5, "NO DATA", horizontalalignment='center', verticalalignment='center', fontsize=12)
            ax.axis('off')

        # Creazione dell'oggetto FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()

        return canvas

    def plot_results(self, results, master):
        try:
            # Crea la figura di Matplotlib e genera il grafico
            fig, axs = plt.subplots(2, 2, figsize=(9, 6))
            axs = axs.flatten()
            titles = list(results.keys())

            metrics = ['min', 'avg', 'max']
            width = 0.2  # Larghezza di ogni colonna

            for i, title in enumerate(titles):
                data = results[title]
                sub_titles = list(data.keys())
                sub_data = [data[key] for key in sub_titles]

                x = range(len(sub_titles))  # Posizioni degli indici x per i gruppi di colonne

                for j, metric in enumerate(metrics):
                    values = [float(sub_data[j][metric]) for j in range(len(sub_titles))]

                    axs[i].bar([xi + j * width for xi in x], values, width=width, label=metric)

                axs[i].set_xticks([xi + width for xi in x])  # Posizionamento dei ticks sull'asse x
                axs[i].set_xticklabels(sub_titles)
                axs[i].set_title(title)
                axs[i].legend()
        except:
            # In caso di errore, genera i 4 grafici vuoti
            fig, axs = plt.subplots(2, 2, figsize=(9, 6))
            axs = axs.flatten()
            for ax in axs:
                ax.text(0.5, 0.5, "ERROR", horizontalalignment='center', verticalalignment='center', fontsize=12)
                ax.axis('off')

        # Creazione dell'oggetto FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()

        return canvas

        # self.populate_content()

    def home_call(self, event, controller):
        home_event = {'type': 'home_clicked'}
        event_bus.publish(home_event)
        controller.show_frame(StartPage)

    def handle_event(self, event):
        if event['type'] == 'chosen_file':
            self.file_list = event['files']
            self.option_menu3['menu'].delete(0, 'end')

            # Aggiungi le nuove opzioni
            for option in self.file_list:
                self.option_menu3['menu'].add_command(label=option, command=tk._setit(self.option3, option))

        elif event['type'] == 'home_clicked':
            self.canvas = self.plot_results(results_zero, self)
            self.canvas.get_tk_widget().grid(row=2, column=0)
            self.file_list =['']
            self.option_menu3['menu'].delete(0, 'end')
            self.option3.set('chose file')
            self.option2.set('chose method')
            matplotlib.pyplot.close()


        elif event['type'] == 'chosen_dataset':
            self.holder_mode = 0
            self.dataset_id = event['id']

        elif event['type'] == 'chosen_holder':
            self.holder_mode = 1
            self.holder_id = event['id']

        elif event['type'] == 'chosen_file_holder':
            self.option_menu3['menu'].delete(0, 'end')
            self.holder_mode = 1


class DatabaseUpdatePageOver(tk.Toplevel):
    mprint('LOADING DATABASE UPDATE', bc.ENDC, 0)

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs, background="white")

        event_bus.subscribe(self)

        self.x, self.y, self.width = 0, 0, 0

        # self.after(2000, self.positioning())

        container = tk.Frame(self, background="white")
        container.grid(row=0, column=0)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.logo = ImageTk.PhotoImage(Image.open("gui_elements/eufair.png").resize((500, 375)))

        label = tk.Label(self)
        label.grid(row=0, column=0)
        label.config(background="white", image=self.logo)

        self.text = tk.Label(self, wraplength=400)
        self.text.config(background="white", font=("Inter", 17), text="LOADING..")
        self.text.grid(row=1, column=0)

        self.text1 = tk.Label(self, wraplength=400)
        self.text1.config(background="white", font=("Inter", 17), text="loading..")
        self.text1.grid(row=2, column=0)

        self.text2 = tk.Label(self, wraplength=400)
        self.text2.config(background="white", font=("Inter", 17), text="loading..")
        self.text2.grid(row=3, column=0)

        self.text3 = tk.Label(self, wraplength=400)
        self.text3.config(background="white", font=("Inter", 17), text="loading..")
        self.text3.grid(row=4, column=0)

        event_bus.publish(event={'type': 'topgui_start'})

    def handle_event(self, event):
        if event['type'] == 'update_text_toplevel':
            if 'text' in event:
                self.text.config(text=event['text'])
            if 'text1' in event:
                self.text1.config(text=event['text1'])
            if 'text2' in event:
                self.text2.config(text=event['text2'])
            if 'text3' in event:
                self.text3.config(text=event['text3'])
        elif event['type'] == 'update_done_toplevel':
            self.destroy()
        elif event['type'] == 'gui_start':
            self.update_idletasks()
            self.y = event['y']
            self.width = event['width']
            self.geometry("+{}+{}".format(self.winfo_screenwidth() - self.width - 50 - 50 - self.winfo_width(), 50))

        elif event['type'] == 'forced_closure':
            self.destroy()
        elif event['type'] == 'property_check':
            self.text.config(text='CHECKING FOR NEW PROPERTIES')
            self.text1.config(text='')
            self.text2.config(text='')
            self.text3.config(text='')

#
# class URLPage(tk.Frame):
#     mprint('LOADING URL PAGE', bc.ENDC, 0)
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent, background='white')
#
#         event_bus.subscribe(self)
#         self.controller = controller
#         self.logo_frame = tk.Frame(self, background='white')
#         self.logo_frame.grid(column=0, row=0, sticky='w')
#
#         self.logo = ImageTk.PhotoImage(Image.open("gui_elements/eufair.png").resize((200, 160)))
#         logo_label = tk.Label(self.logo_frame, background='white')
#         logo_label.grid(row=0, column=0, sticky='e')
#         logo_label.config(background="white", image=self.logo)
#
#         blank = tk.Label(self.logo_frame, background='white')
#         blank.grid(row=0, column=1)
#
#         self.home = ImageTk.PhotoImage(Image.open("gui_elements/home.png").resize((30, 30)))
#         home_butt = tk.Label(blank, background='white')
#         home_butt.grid(row=0, column=0, sticky='sw')
#         home_butt.config(background="white", image=self.home)
#         home_butt.bind('<Button-1>', lambda event: self.home_call(event, controller))
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)
#
#         self.choose_frame = tk.Frame(self)
#         self.choose_frame.grid(row=1, column=0)
#         self.choose_frame.config(background='white')
#
#
#         # Opzioni per la casella di selezione 1
#         self.options1 = ["dati.gov.it", "data.europa.eu", "native"]
#         self.option1 = tk.StringVar()
#         self.option1.set('chose portal')
#
#         # Creazione della casella di selezione 1
#         option_menu1 = tk.OptionMenu(self.choose_frame, self.option1, *self.options1)
#         option_menu1.grid(row=0, column=0, padx=5, pady=5)
#         option_menu1.config(background='white')
#
#         # Opzioni per la casella di selezione 2
#         self.options2 = ["DCAT_AP", "DCAT_AP-IT", "merged"]
#         self.option2 = tk.StringVar()
#         self.option2.set('chose method')
#
#         # Creazione della casella di selezione 2
#         option_menu2 = tk.OptionMenu(self.choose_frame, self.option2, *self.options2)
#         option_menu2.grid(row=0, column=1, padx=5, pady=5)
#         option_menu2.config(background='white')
#
#         button = tk.Button(self.choose_frame, text="Invio", command=self.handle_button_click, background='white')
#         button.grid(row=0, column=2, padx=5, pady=5)
#
#         file_frame = tk.Frame(self, background='white')
#         file_frame.grid(row=3,column=0)
#
#         self.file_label = tk.Label(file_frame, background='white', text='')
#         self.file_label.grid(row=0, column=0, sticky='nsew')
#
#         self.dataset_id = ''
#
#         self.holder_id = ''
#
#         self.file_list = []
#
#
#         self.canvas = self.plot_results(results_zero, self)
#         self.canvas.get_tk_widget().grid(row=2, column=0)
#

