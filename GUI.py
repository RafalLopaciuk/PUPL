from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import data.main as core
from operator import attrgetter
import random
import codecs
import time


deleted_count = 0


def random_color():
    r = lambda: random.randint(100, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Program układający plany lekcyjne.")
        self.root.iconphoto(True, PhotoImage(file="./data/images/app_icon.png"))

        # Import icons
        self.photo1 = PhotoImage(file="./data/images/file.png")
        self.photoimage1 = self.photo1.subsample(10, 10)
        self.photo2 = PhotoImage(file="./data/images/folder.png")
        self.photoimage2 = self.photo2.subsample(10, 10)
        self.photo3 = PhotoImage(file="./data/images/floppy-disk.png")
        self.photoimage3 = self.photo3.subsample(10, 10)
        self.photo4 = PhotoImage(file="./data/images/export.png")
        self.photoimage4 = self.photo4.subsample(10, 10)
        self.photo5 = PhotoImage(file="./data/images/team.png")
        self.photoimage5 = self.photo5.subsample(10, 10)
        self.photo6 = PhotoImage(file="./data/images/teacher.png")
        self.photoimage6 = self.photo6.subsample(10, 10)
        self.photo7 = PhotoImage(file="./data/images/door.png")
        self.photoimage7 = self.photo7.subsample(10, 10)
        self.photo8 = PhotoImage(file="./data/images/book.png")
        self.photoimage8 = self.photo8.subsample(10, 10)
        self.photo9 = PhotoImage(file="./data/images/cogwheel.png")
        self.photoimage9 = self.photo9.subsample(10, 10)
        self.photo10 = PhotoImage(file="./data/images/wheel.png")
        self.photoimage10 = self.photo10.subsample(10, 10)

        # Top menu
        self.menu_top = Frame(self.root, bg="#ababab")
        self.button1 = Button(self.menu_top, text="Nowy plan", image=self.photoimage1, compound=TOP, padx=10, pady=5,
                              width=75, command=lambda: self.new_file())
        self.button2 = Button(self.menu_top, text="Otwórz plan", image=self.photoimage2, compound=TOP, padx=10, pady=5,
                              width=75, command=lambda: self.open_file())
        self.button3 = Button(self.menu_top, text="Zapisz plan", image=self.photoimage3, compound=TOP, padx=10, pady=5,
                              width=75, command=lambda: self.save_file())
        self.button4 = Button(self.menu_top, text="Eksportuj plan", image=self.photoimage4, compound=TOP, padx=10,
                              pady=5, width=75, command=lambda: self.export_timetable())
        self.button5 = Button(self.menu_top, text="Klasy", image=self.photoimage5, compound=TOP, padx=10, pady=5,
                              width=75, command=lambda: self.add_class())
        self.button6 = Button(self.menu_top, text="Nauczyciele", image=self.photoimage6, compound=TOP, padx=10,
                              pady=5, command=lambda: self.add_teacher())
        self.button7 = Button(self.menu_top, text="Sale zajęciowe", image=self.photoimage7, compound=TOP, padx=10,
                              width=75,
                              pady=5, command=lambda: self.add_room())
        self.button8 = Button(self.menu_top, text="Lekcje (aktywność)", image=self.photoimage8, compound=TOP, width=95,
                              padx=10, pady=5, command=lambda: self.add_course())
        self.button9 = Button(self.menu_top, text="GENERUJ PLAN", image=self.photoimage9, compound=TOP, padx=10,
                              pady=5, width=75, command=lambda: self.generate_button())
        self.button10 = Button(self.menu_top, text="Ustawienia", image=self.photoimage10, compound=TOP, padx=10, pady=5,
                               width=70, command=lambda: self.options())

        if not core.generate_ready:
            self.button9.config(state=DISABLED)

        self.button1.grid(row=0, column=0, padx=2)
        self.button2.grid(row=0, column=1, padx=2)
        self.button3.grid(row=0, column=2, padx=2)
        self.button4.grid(row=0, column=3, padx=2)
        self.button5.grid(row=0, column=4, padx=2)
        self.button6.grid(row=0, column=5, padx=2)
        self.button7.grid(row=0, column=6, padx=2)
        self.button8.grid(row=0, column=7, padx=2)
        self.button9.grid(row=0, column=8, padx=2)
        self.button10.grid(row=0, column=9, padx=2)

        # Body area
        self.content1 = Frame(self.root, background="white")

        # Status bar
        self.status_frame = Frame(self.root, height=10)
        self.status = Label(self.status_frame, text="", bg="#ababab")
        self.status.pack(fill="both", expand=True)

        self.menu_top.grid(row=0, column=0, sticky="ew")
        self.content1.grid(row=1, column=0, sticky="nsew")
        self.status_frame.grid(row=2, column=0, sticky="ew")

        self.body = Canvas(self.content1)
        self.body.config(bg="#ffffff")
        self.body.grid_columnconfigure(0, weight=1)

        self.T = Text(self.body)
        self.T.pack(side=LEFT, fill='both', expand=True, )

        self.T.insert(END, core.last_added)
        self.body.pack(fill='both', expand=True, side='left', padx=5, pady=5)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.mainloop()

    def new_file(self):
        export_window = Toplevel(self.root, padx=10, pady=10)
        export_window.grab_set()
        label_example = Label(export_window, text="Napewno chcesz utworzyć nowy projekt?", padx=10, pady=10)
        button_yes = Button(export_window, text="Tak", width=10, command=lambda: options_ok())
        button_no = Button(export_window, text="Nie", width=10, command=lambda: export_window.destroy())

        label_example.grid(row=0, column=0, columnspan=2)
        button_yes.grid(row=1, column=0)
        button_no.grid(row=1, column=1)

        def options_ok():
            core.new_start()
            for widget in self.content1.winfo_children():
                widget.destroy()
            self.body = Canvas(self.content1)
            self.body.config(bg="#ffffff")
            self.body.grid_columnconfigure(0, weight=1)

            self.T = Text(self.body)
            self.T.pack(side=LEFT, fill='both', expand=True, )

            self.T.insert(END, core.last_added)
            self.body.pack(fill='both', expand=True, side='left', padx=5, pady=5)

            self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Nowy projekt")
            export_window.destroy()

    def open_file(self):
        try:
            self.root.filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik z planem.",
                                                            filetypes=(
                                                                ("puplf files", "*.puplf"), ("all files", "*.*")))
            file = codecs.open(self.root.filename, "r", "utf-8")
            core.open_from_file(file)
            file.close()
            self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Otworzono: " + self.root.filename)
            if core.generated:
                self.generate_elements()
            else:
                for widget in self.content1.winfo_children():
                    widget.destroy()
                self.body = Canvas(self.content1)
                self.body.config(bg="#ffffff")
                self.body.grid_columnconfigure(0, weight=1)

                self.T = Text(self.body)
                self.T.pack(side=LEFT, fill='both', expand=True, )

                self.T.insert(END, core.last_added)
                self.body.pack(fill='both', expand=True, side='left', padx=5, pady=5)
        except Exception as e:
            self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Nie udało się otworzyć pliku.")
            # print(e)

    def save_file(self):
        try:
            files = [("puplf files", "*.puplf"), ('All Files', '*.*')]
            file = asksaveasfile(filetypes=files, defaultextension=files)
            name = file.name
            file.close()
            file = codecs.open(name, "w", "utf-8")
            core.save_to_file(file)
            file.close()
            self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Zapisano: " + name)
        except Exception as e:
            self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Nie udało się zapisać pliku.")
            print(e)

    def export_timetable(self):
        try:
            if core.generated:
                # try:
                path = filedialog.askdirectory()
                core.export_project(path)
                self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Wyeksportowano: " + path)
                # except Exception as e:
                #   self.status.config(text="Nie udało się wyeksportować")
            else:
                self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Wpierw WYGENERUJ plan, zanim zechcesz go wyeksportować.")
        except Exception as e:
            self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Nie udało się wyeksportować planu.")
            # print(e)

    def add_class(self):
        global deleted_count
        deleted_count = 0
        options_window = Toplevel(self.root, padx=10, pady=10)
        options_window.grab_set()
        label = Label(options_window, text="Programy nauczania", padx=10, pady=10)
        element_list = Listbox(options_window, width=40, height=20)

        core.curriculumsArray = sorted(core.curriculumsArray, key=attrgetter('name'))

        i = 0
        for item in core.curriculumsArray:
            item = str(i + 1) + " ) " + str(item)
            element_list.insert(END, str(item))
            i += 1

        frame = Frame(options_window)
        button_edit = Button(frame, text="Edytuj", width=10, command=lambda: options_edit())
        button_delete = Button(frame, text="Usuń", width=10, command=lambda: options_delete())
        information_Text = Label(options_window)

        button_add = Button(options_window, text="Dodaj", width=10, command=lambda: options_add())
        button_exit = Button(options_window, text="Zamknij", width=10,
                             command=lambda: options_window.destroy())

        label.grid(row=0, column=0, columnspan=2)
        element_list.grid(row=1, column=0, rowspan=2)
        frame.grid(row=1, column=1)
        button_edit.pack(pady=5)
        button_delete.pack(pady=5)
        information_Text.grid(row=2, column=1)

        button_add.grid(row=3, column=0, padx=10, pady=10)
        button_exit.grid(row=3, column=1, padx=10, pady=10)

        def options_add():
            element_window = Toplevel(self.root, padx=10, pady=10)
            element_window.grab_set()
            label_2 = Label(element_window, text="Dodawanie programu nauczania", padx=10, pady=10)

            label_1_2 = Label(element_window, text="Nazwa: ", padx=10, pady=10)
            entry_1_2 = Entry(element_window)

            label_2_2 = Label(element_window, text="Liczba uczniów: ", padx=10, pady=10)
            entry_2_2 = Spinbox(element_window, from_=1, to=50)

            button_ok_2 = Button(element_window, text="OK", width=10, command=lambda: options_ok())
            button_exit_2 = Button(element_window, text="Anuluj", width=10,
                                   command=lambda: element_window.destroy())

            label_2.grid(row=0, column=0, columnspan=2)

            label_1_2.grid(row=1, column=0)
            entry_1_2.grid(row=1, column=1)

            label_2_2.grid(row=2, column=0)
            entry_2_2.grid(row=2, column=1)

            button_ok_2.grid(row=3, column=0, padx=10, pady=10)
            button_exit_2.grid(row=3, column=1, padx=10, pady=10)

            def options_ok():
                try:
                    core.curriculumsArray.append(core.Curriculum(entry_1_2.get(), entry_2_2.get()))
                    element_list.insert(END, str(len(core.curriculumsArray)) + "\t " + str(core.curriculumsArray[-1]))
                    if self.T.winfo_exists() == 1:
                        self.T.insert(END, "\nKLASA: " + str(core.curriculumsArray[-1]))
                    # print("Dodano")
                except Exception as e:
                    # print("Error: " + str(e))
                    pass
                element_window.destroy()

        def options_edit():
            if not element_list.get(ANCHOR):
                information_Text.config(text="Wybierz\nelement\nz listy.")
                return
            information_Text.config(text="")
            try:
                # print(element_list.get(ANCHOR))
                id = int(str(element_list.get(ANCHOR).split(" ")[0])) - 1
                element_window = Toplevel(self.root, padx=10, pady=10)
                element_window.grab_set()
                label_2 = Label(element_window, text="Edycja klasy", padx=10, pady=10)

                label_1_2 = Label(element_window, text="Nazwa: ", padx=10, pady=10)
                v1 = StringVar(element_window, value=core.curriculumsArray[id].name)
                entry_1_2 = Entry(element_window, textvariable=v1)

                label_2_2 = Label(element_window, text="Liczba uczniów: ", padx=10, pady=10)
                v2 = StringVar(options_window)
                v2.set(core.curriculumsArray[id].number_of_students)
                entry_2_2 = Spinbox(element_window, from_=1, to=48, textvariable=v2)

                button_ok_2 = Button(element_window, text="OK", width=10, command=lambda: options_ok(id))
                button_exit_2 = Button(element_window, text="Anuluj", width=10,
                                       command=lambda: element_window.destroy())

                label_2.grid(row=0, column=0, columnspan=2)

                label_1_2.grid(row=1, column=0)
                entry_1_2.grid(row=1, column=1)

                label_2_2.grid(row=2, column=0)
                entry_2_2.grid(row=2, column=1)

                button_ok_2.grid(row=3, column=0, padx=10, pady=10)
                button_exit_2.grid(row=3, column=1, padx=10, pady=10)

                def options_ok(id):
                    try:
                        core.curriculumsArray[id].name = entry_1_2.get()
                        core.curriculumsArray[id].number_of_students = entry_2_2.get()
                        element_list.delete(id)
                        element_list.insert(id, str(id + 1) + " " + str(core.curriculumsArray[id]))
                        # print("Zedytowano")
                    except Exception as e:
                        # print("Error: " + str(e))
                        pass
                    element_window.destroy()
                    options_window.grab_set()
            except Exception as e:
                print("Error: " + str(e))

        def options_delete():
            global deleted_count
            if not element_list.get(ANCHOR):
                information_Text.config(text="Wybierz\nelement\nz listy.")
                return
            information_Text.config(text="")
            try:
                # core.curriculumsArray.remove(core.find_teacher_by_name(int(element_list.get(ANCHOR).split(" ")[0])))
                # del core.curriculumsArray[int(element_list.get(ANCHOR).split(" ")[0]) - 1]
                core.remove_curriculum(int(element_list.get(ANCHOR).split(" ")[0]) - 1)
                element_list.delete(ANCHOR)
                deleted_count += 1

                element_list.delete(0, 'end')
                i = 0
                for item in core.curriculumsArray:
                    item = str(i + 1) + " ) " + str(item)
                    element_list.insert(END, str(item))
                    i += 1
            except Exception as e:
                print("Error: " + str(e))

    def add_teacher(self):
        global deleted_count
        deleted_count = 0
        options_window = Toplevel(self.root, padx=10, pady=10)
        options_window.grab_set()
        label = Label(options_window, text="Nauczyciele", padx=10, pady=10)
        element_list = Listbox(options_window, width=40, height=20)

        core.teachersArray = sorted(core.teachersArray, key=attrgetter('surname'))

        i = 0
        for item in core.teachersArray:
            item = str(i + 1) + " ) " + str(item)
            element_list.insert(END, str(item))
            i += 1

        frame = Frame(options_window)
        button_edit = Button(frame, text="Edytuj", width=10, command=lambda: options_edit())
        button_delete = Button(frame, text="Usuń", width=10, command=lambda: options_delete())
        information_Text = Label(options_window)

        button_add = Button(options_window, text="Dodaj", width=10, command=lambda: options_add())
        button_exit = Button(options_window, text="Zamknij", width=10,
                             command=lambda: options_window.destroy())

        label.grid(row=0, column=0, columnspan=2)
        element_list.grid(row=1, column=0, rowspan=2)
        frame.grid(row=1, column=1)
        button_edit.pack(pady=5)
        button_delete.pack(pady=5)
        information_Text.grid(row=2, column=1)

        button_add.grid(row=3, column=0, padx=10, pady=10)
        button_exit.grid(row=3, column=1, padx=10, pady=10)

        def options_add():
            element_window = Toplevel(self.root, padx=10, pady=10)
            element_window.grab_set()
            label_2 = Label(element_window, text="Dodawanie nauczyciela", padx=10, pady=10)

            label_1_2 = Label(element_window, text="Imie: ", padx=10, pady=10)
            entry_1_2 = Entry(element_window)

            label_2_2 = Label(element_window, text="Nazwisko: ", padx=10, pady=10)
            entry_2_2 = Entry(element_window)

            label_3_2 = Label(element_window, text="(Edycja nauczyciela umożliwia dodanie niedostępnych godzin.)",
                              padx=10, pady=10)

            button_ok_2 = Button(element_window, text="OK", width=10, command=lambda: options_ok())
            button_exit_2 = Button(element_window, text="Anuluj", width=10,
                                   command=lambda: element_window.destroy())

            label_2.grid(row=0, column=0, columnspan=2)

            label_1_2.grid(row=1, column=0)
            entry_1_2.grid(row=1, column=1)

            label_2_2.grid(row=2, column=0)
            entry_2_2.grid(row=2, column=1)

            label_3_2.grid(row=3, column=0, columnspan=2)

            button_ok_2.grid(row=4, column=0, padx=10, pady=10)
            button_exit_2.grid(row=4, column=1, padx=10, pady=10)

            def options_ok():
                try:
                    core.teachersArray.append(core.Teacher(entry_1_2.get(), entry_2_2.get()))
                    element_list.insert(END, str(len(core.teachersArray)) + "\t " + str(core.teachersArray[-1]))
                    if self.T.winfo_exists() == 1:
                        self.T.insert(END, "\nNAUCZYCIEL: " + str(core.teachersArray[-1]))
                    # print("Dodano")
                except Exception as e:
                    # print("Error: " + str(e))
                    pass
                element_window.destroy()

        def options_edit():
            if not element_list.get(ANCHOR):
                information_Text.config(text="Wybierz\nelement\nz listy.")
                return
            information_Text.config(text="")
            try:
                # print(element_list.get(ANCHOR))
                id = int(str(element_list.get(ANCHOR).split(" ")[0])) - 1
                # print(core.teachersArray[id])
                element_window = Toplevel(self.root, padx=10, pady=10)
                element_window.grab_set()
                label_2 = Label(element_window, text="Edycja nauczyciela", padx=10, pady=10)

                label_1_2 = Label(element_window, text="Imie: ", padx=10, pady=10)
                v1 = StringVar(element_window, value=core.teachersArray[id].name)
                entry_1_2 = Entry(element_window, textvariable=v1, width=25)

                label_2_2 = Label(element_window, text="Nazwisko: ", padx=10, pady=10)
                v2 = StringVar(element_window, value=core.teachersArray[id].surname)
                entry_2_2 = Entry(element_window, textvariable=v2, width=25)

                label_T = Label(element_window, text="Niedostępne godziny", padx=10, pady=10)
                element_list_T = Listbox(element_window, width=25, height=10)

                for i in range(core.numbers_of_Time * core.numbers_of_Day):
                    if i in core.teachersArray[id].unavailable_hours:
                        element_list_T.insert(END, ("Dzień " + str((i // core.numbers_of_Time) + 1) + " Godzina " + str(
                            (i % core.numbers_of_Time) + 1)))
                    i += 1

                frameT = Frame(element_window)
                button_add_T = Button(frameT, text="Dodaj", width=10, command=lambda: options_add_T(id))
                button_delete_T = Button(frameT, text="Usuń", width=10, command=lambda: options_delete_T(id))

                button_ok_2 = Button(element_window, text="OK", width=10, command=lambda: options_ok(id))
                button_exit_2 = Button(element_window, text="Anuluj", width=10,
                                       command=lambda: element_window.destroy())

                label_2.grid(row=0, column=0, columnspan=2)

                label_1_2.grid(row=1, column=0)
                entry_1_2.grid(row=1, column=1)

                label_2_2.grid(row=2, column=0)
                entry_2_2.grid(row=2, column=1)

                label_T.grid(row=3, column=0)
                element_list_T.grid(row=3, column=1, rowspan=2)
                frameT.grid(row=4, column=0)
                button_add_T.pack(pady=5)
                button_delete_T.pack(pady=5)

                button_ok_2.grid(row=5, column=0, padx=10, pady=10)
                button_exit_2.grid(row=5, column=1, padx=10, pady=10)

                def options_ok(id):
                    try:
                        core.teachersArray[id].name = entry_1_2.get()
                        core.teachersArray[id].surname = entry_2_2.get()
                        element_list.delete(id)
                        element_list.insert(id, str(id + 1) + " " + str(core.teachersArray[id]))
                        # print("Zedytowano")
                    except Exception as e:
                        print("Error: " + str(e))
                    element_window.destroy()
                    options_window.grab_set()

                def options_add_T(id):
                    element_window_time = Toplevel(self.root, padx=10, pady=10)
                    element_window_time.grab_set()
                    label_1_time = Label(element_window_time, text="Niedostępna godzina: ", padx=10,
                                         pady=10)
                    list = []
                    i = 0
                    for item in range(core.numbers_of_Day * core.numbers_of_Time):
                        if item not in core.teachersArray[id].unavailable_hours:
                            list.append(
                                "Dzień " + str(int(i / core.numbers_of_Time) + 1) + " Godzina " + str(
                                    (i % core.numbers_of_Time) + 1))
                        i += 1

                    entry_1_2_time = ttk.Combobox(element_window_time, values=list, width=40)

                    button_ok_2_time = Button(element_window_time, text="OK", width=10,
                                              command=lambda: options_ok_T(id))
                    button_exit_2_time = Button(element_window_time, text="Anuluj", width=10,
                                                command=lambda: element_window_time.destroy())

                    label_1_time.grid(row=0, column=0, columnspan=2)
                    entry_1_2_time.grid(row=1, column=0, columnspan=2)

                    button_ok_2_time.grid(row=3, column=0, padx=10, pady=10)
                    button_exit_2_time.grid(row=3, column=1, padx=10, pady=10)

                    def options_ok_T(id):
                        try:
                            time = (int(entry_1_2_time.get().split(" ")[1]) - 1) * core.numbers_of_Time \
                                   + (int(entry_1_2_time.get().split(" ")[3]) - 1)
                            # print(time)
                            core.teachersArray[id].add_unavailable_hours(time)
                            # print(core.teachersArray[id].unavailable_hours)
                            element_list_T.insert(END, entry_1_2_time.get())
                        except Exception as e:
                            print("Error: " + str(e))
                        element_window_time.destroy()
                        element_window.grab_set()

                def options_delete_T(id):
                    try:
                        splits = str(element_list_T.get(ANCHOR)).split(" ")
                        time = (int(splits[1]) - 1) * core.numbers_of_Time + (int(splits[3]) - 1)
                        core.teachersArray[id].del_unavailable_hours(time)
                        element_list_T.delete(ANCHOR)
                    except Exception as e:
                        print("Error: " + str(e))

            except Exception as e:
                print("Error: " + str(e))

        def options_delete():
            global deleted_count
            if not element_list.get(ANCHOR):
                information_Text.config(text="Wybierz\nelement\nz listy.")
                return
            information_Text.config(text="")
            try:
                # del core.teachersArray[]
                core.remove_teacher(int(element_list.get(ANCHOR).split(" ")[0]) - 1)
                element_list.delete(0, 'end')
                i = 0
                for item in core.teachersArray:
                    item = str(i + 1) + " ) " + str(item)
                    element_list.insert(END, str(item))
                    i += 1
                deleted_count += 1
            except Exception as e:
                print("Error: " + str(e))

    def add_room(self):
        global deleted_count
        deleted_count = 0
        options_window = Toplevel(self.root, padx=10, pady=10)
        options_window.grab_set()
        label = Label(options_window, text="Sale zajęciowe", padx=10, pady=10)
        element_list = Listbox(options_window, width=40, height=20)

        core.roomsArray = sorted(core.roomsArray, key=attrgetter('number'))

        i = 0
        for item in core.roomsArray:
            item = str(i + 1) + " ) " + str(item)
            element_list.insert(END, str(item))
            i += 1

        frame = Frame(options_window)
        button_edit = Button(frame, text="Edytuj", width=10, command=lambda: options_edit())
        button_delete = Button(frame, text="Usuń", width=10, command=lambda: options_delete())
        information_Text = Label(options_window)

        button_add = Button(options_window, text="Dodaj", width=10, command=lambda: options_add())
        button_exit = Button(options_window, text="Zamknij", width=10,
                             command=lambda: options_window.destroy())

        label.grid(row=0, column=0, columnspan=2)
        element_list.grid(row=1, column=0, rowspan=2)
        frame.grid(row=1, column=1)
        button_edit.pack(pady=5)
        button_delete.pack(pady=5)
        information_Text.grid(row=2, column=1)

        button_add.grid(row=3, column=0, padx=10, pady=10)
        button_exit.grid(row=3, column=1, padx=10, pady=10)

        def options_add():
            element_window = Toplevel(self.root, padx=10, pady=10)
            element_window.grab_set()
            label_2 = Label(element_window, text="Dodawanie sali zajęciowej", padx=10, pady=10)

            label_1_2 = Label(element_window, text="Numer sali: ", padx=10, pady=10)
            entry_1_2 = Entry(element_window)

            label_2_2 = Label(element_window, text="Maksymalna liczba uczniów: ", padx=10, pady=10)
            entry_2_2 = Spinbox(element_window, from_=1, to=1000)

            button_ok_2 = Button(element_window, text="OK", width=10, command=lambda: options_ok())
            button_exit_2 = Button(element_window, text="Anuluj", width=10,
                                   command=lambda: element_window.destroy())

            label_2.grid(row=0, column=0, columnspan=2)

            label_1_2.grid(row=1, column=0)
            entry_1_2.grid(row=1, column=1)

            label_2_2.grid(row=2, column=0)
            entry_2_2.grid(row=2, column=1)

            button_ok_2.grid(row=3, column=0, padx=10, pady=10)
            button_exit_2.grid(row=3, column=1, padx=10, pady=10)

            def options_ok():
                try:
                    core.roomsArray.append(core.Room(entry_1_2.get(), entry_2_2.get()))
                    element_list.insert(END, str(len(core.roomsArray)) + "\t " + str(core.roomsArray[-1]))
                    if self.T.winfo_exists() == 1:
                        self.T.insert(END, "\nSALA: " + str(core.roomsArray[-1]))
                    # print("Dodano")
                except Exception as e:
                    print("Error: " + str(e))
                element_window.destroy()

        def options_edit():
            if not element_list.get(ANCHOR):
                information_Text.config(text="Wybierz\nelement\nz listy.")
                return
            information_Text.config(text="")
            try:
                # print(element_list.get(ANCHOR))
                id = int(str(element_list.get(ANCHOR).split(" ")[0])) - 1
                element_window = Toplevel(self.root, padx=10, pady=10)
                element_window.grab_set()
                label_2 = Label(element_window, text="Edycja sali zajęciowej", padx=10, pady=10)

                label_1_2 = Label(element_window, text="Numer sali: ", padx=10, pady=10)
                v1 = StringVar(element_window, value=core.roomsArray[id].name)
                entry_1_2 = Entry(element_window, textvariable=v1)

                label_2_2 = Label(element_window, text="Maksymalna liczba uczniów: ", padx=10, pady=10)
                v2 = StringVar(options_window)
                v2.set(core.roomsArray[id].size)
                entry_2_2 = Spinbox(element_window, from_=1, to=1000, textvariable=v2)

                button_ok_2 = Button(element_window, text="OK", width=10, command=lambda: options_ok(id))
                button_exit_2 = Button(element_window, text="Anuluj", width=10,
                                       command=lambda: element_window.destroy())

                label_2.grid(row=0, column=0, columnspan=2)

                label_1_2.grid(row=1, column=0)
                entry_1_2.grid(row=1, column=1)

                label_2_2.grid(row=2, column=0)
                entry_2_2.grid(row=2, column=1)

                button_ok_2.grid(row=3, column=0, padx=10, pady=10)
                button_exit_2.grid(row=3, column=1, padx=10, pady=10)

                def options_ok(id):
                    try:
                        core.roomsArray[id].name = entry_1_2.get()
                        core.roomsArray[id].size = entry_2_2.get()
                        element_list.delete(id)
                        element_list.insert(id, str(id + 1) + " " + str(core.curriculumsArray[id]))
                        # print("Zedytowano")
                    except Exception as e:
                        print("Error: " + str(e))
                    element_window.destroy()
                    options_window.grab_set()
            except Exception as e:
                print("Error: " + str(e))

        def options_delete():
            global deleted_count
            if not element_list.get(ANCHOR):
                information_Text.config(text="Wybierz\nelement\nz listy.")
                return
            information_Text.config(text="")
            try:
                # core.curriculumsArray.remove(core.find_teacher_by_name(int(element_list.get(ANCHOR).split(" ")[0])))
                # del core.roomsArray[int(element_list.get(ANCHOR).split(" ")[0]) - 1]
                core.remove_room(int(element_list.get(ANCHOR).split(" ")[0]) - 1)
                element_list.delete(0, 'end')
                i = 0
                for item in core.roomsArray:
                    item = str(i + 1) + " ) " + str(item)
                    element_list.insert(END, str(item))
                    i += 1
                deleted_count += 1
            except Exception as e:
                print("Error: " + str(e))

    def add_course(self):
        global deleted_count
        deleted_count = 0
        options_window = Toplevel(self.root, padx=10, pady=10)
        options_window.grab_set()
        label = Label(options_window, text="Lekcje (Aktywności)", padx=10, pady=10)
        element_list = Listbox(options_window, width=110, height=40)

        core.coursesArray = sorted(core.coursesArray, key=attrgetter('name'))

        i = 0
        for item in core.coursesArray:
            item = str(i + 1) + " ) " + str(item)
            element_list.insert(END, str(item))
            i += 1

        # frame = Frame(options_window)
        button_edit = Button(options_window, text="Edytuj", width=10,
                             command=lambda: options_edit(int(str(element_list.get(ANCHOR).split(" ")[0])) - 1))
        button_delete = Button(options_window, text="Usuń", width=10, command=lambda: options_delete())
        information_Text = Label(options_window)

        button_add = Button(options_window, text="Dodaj", width=10, command=lambda: options_add())
        button_exit = Button(options_window, text="Powrót", width=10,
                             command=lambda: options_window.destroy())

        label.grid(row=0, column=0, columnspan=4)
        element_list.grid(row=1, column=0, columnspan=4)
        information_Text.grid(row=2, column=0, columnspan=4)

        button_add.grid(row=3, column=0, padx=10, pady=10)
        button_edit.grid(row=3, column=1, padx=10, pady=10)
        button_delete.grid(row=3, column=2, padx=10, pady=10)
        button_exit.grid(row=3, column=3, padx=10, pady=10)

        def options_add():
            element_window = Toplevel(self.root, padx=10, pady=10)
            element_window.grab_set()
            label_2 = Label(element_window, text="Dodawanie lekcji (aktywności)", padx=10, pady=10)

            label_1_2 = Label(element_window, text="Nazwa: ", padx=10, pady=10)
            entry_1_2 = Entry(element_window, width=44)

            label_2_2 = Label(element_window, text="Klasa: ", padx=10, pady=10)
            list = []
            i = 0
            for item in core.curriculumsArray:
                item = str(i + 1) + " " + str(item)
                list.append(str(item))
                i += 1
            entry_2_2 = ttk.Combobox(element_window, values=list, width=40)

            label_2_2_2 = Label(element_window, text="Dodatkowa klasa: ", padx=10, pady=10)
            list = []
            i = 0
            list.append("BRAK")
            for item in core.curriculumsArray:
                item = str(i + 1) + " " + str(item)
                list.append(str(item))
                i += 1
            entry_2_2_2 = ttk.Combobox(element_window, values=list, width=40)
            entry_2_2_2.current(0)

            label_2_2_3 = Label(element_window, text="Dodatkowa klasa: ", padx=10, pady=10)
            list = []
            i = 0
            list.append("BRAK")
            for item in core.curriculumsArray:
                item = str(i + 1) + " " + str(item)
                list.append(str(item))
                i += 1
            entry_2_2_3 = ttk.Combobox(element_window, values=list, width=40)
            entry_2_2_3.current(0)

            label_2_2_4 = Label(element_window, text="Dodatkowa klasa: ", padx=10, pady=10)
            list = []
            i = 0
            list.append("BRAK")
            for item in core.curriculumsArray:
                item = str(i + 1) + " " + str(item)
                list.append(str(item))
                i += 1
            entry_2_2_4 = ttk.Combobox(element_window, values=list, width=40)
            entry_2_2_4.current(0)

            label_3_2 = Label(element_window, text="Nauczyciel: ", padx=10, pady=10)
            list = []
            i = 0
            for item in core.teachersArray:
                item = str(i + 1) + " " + str(item)
                list.append(str(item))
                i += 1
            entry_3_2 = ttk.Combobox(element_window, values=list, width=40)

            label_4_2 = Label(element_window, text="Konkretna sala: ", padx=10, pady=10)
            list = []
            i = 0
            list.append("BRAK")
            for item in core.roomsArray:
                item = str(i + 1) + " " + str(item)
                list.append(str(item))
                i += 1
            entry_4_2 = ttk.Combobox(element_window, values=list, width=40)
            entry_4_2.current(0)

            label_5_2 = Label(element_window, text="Liczba godzin lekcyjnych: ", padx=10, pady=10)
            entry_5_2 = Spinbox(element_window, from_=1, to=core.numbers_of_Time, width=41)

            label_5_3 = Label(element_window, text="LICZBA KURSÓW W OKRESIE: ", padx=10, pady=10)
            entry_5_3 = Spinbox(element_window, from_=1, to=core.numbers_of_Time, width=41)

            button_ok_2 = Button(element_window, text="OK", width=10, command=lambda: options_ok())
            button_exit_2 = Button(element_window, text="Anuluj", width=10,
                                   command=lambda: element_window.destroy())

            label_2.grid(row=0, column=0, columnspan=2)

            label_1_2.grid(row=1, column=0)
            entry_1_2.grid(row=1, column=1)

            label_2_2.grid(row=2, column=0)
            entry_2_2.grid(row=2, column=1)

            label_2_2_2.grid(row=3, column=0)
            entry_2_2_2.grid(row=3, column=1)

            label_2_2_3.grid(row=4, column=0)
            entry_2_2_3.grid(row=4, column=1)

            label_2_2_4.grid(row=5, column=0)
            entry_2_2_4.grid(row=5, column=1)

            label_3_2.grid(row=6, column=0)
            entry_3_2.grid(row=6, column=1)

            label_4_2.grid(row=7, column=0)
            entry_4_2.grid(row=7, column=1)

            # label_5_2.grid(row=8, column=0)
            # entry_5_2.grid(row=8, column=1)

            label_5_3.grid(row=8, column=0)
            entry_5_3.grid(row=8, column=1)

            button_ok_2.grid(row=9, column=0, padx=10, pady=10)
            button_exit_2.grid(row=9, column=1, padx=10, pady=10)

            def options_ok():
                try:
                    if entry_1_2.get() != "" and entry_2_2.get() != "" and entry_3_2.get() != "" and entry_4_2.get() != "" and entry_5_2.get() != "":
                        curriculum_id = int(entry_2_2.get().split(" ")[0]) - 1
                        teacher_id = int(entry_3_2.get().split(" ")[0]) - 1
                        curriculum2 = None
                        curriculum3 = None
                        curriculum4 = None
                        room = None
                        if entry_2_2_2.get() != "BRAK":
                            curriculum2 = core.curriculumsArray[int(entry_2_2_2.get().split(" ")[0]) - 1]
                        if entry_2_2_3.get() != "BRAK":
                            curriculum3 = core.curriculumsArray[int(entry_2_2_3.get().split(" ")[0]) - 1]
                        if entry_2_2_4.get() != "BRAK":
                            curriculum4 = core.curriculumsArray[int(entry_2_2_4.get().split(" ")[0]) - 1]
                        if entry_4_2.get() != "BRAK":
                            room = core.roomsArray[int(entry_4_2.get().split(" ")[0]) - 1]
                        for n in range(int(entry_5_3.get())):
                            core.coursesArray.append(
                                core.Course(entry_1_2.get(), core.curriculumsArray[curriculum_id], curriculum2,
                                            curriculum3,
                                            curriculum4, core.teachersArray[teacher_id],
                                            room, int(entry_5_2.get())))
                            element_list.insert(END, str(len(core.coursesArray)) + " ) " + str(core.coursesArray[-1]))
                        if self.T.winfo_exists() == 1:
                            self.T.insert(END, "\nKURS: " + str(entry_5_3.get()) + "x " + str(core.coursesArray[-1]))
                        element_window.destroy()
                        options_window.grab_set()
                        information_Text.config(text="")
                    else:
                        information_Text.config(text="Dodawany element musi mieć poprawnie podane wszystkie pola.")
                    # print("Dodano")
                except Exception as e:
                    print("Error: " + str(e))

        def options_edit(id):
            if not element_list.get(ANCHOR):
                information_Text.config(text="Wybierz element z listy.")
                return
            information_Text.config(text="")
            try:
                # print(element_list.get(ANCHOR))
                element_window = Toplevel(self.root, padx=10, pady=10)
                element_window.grab_set()
                label_2 = Label(element_window, text="Edycja lekcji (aktywnośći)", padx=10, pady=10)

                label_1_2 = Label(element_window, text="Nazwa: ", padx=10, pady=10)
                v1 = StringVar(element_window, value=core.coursesArray[id].name)
                entry_1_2 = Entry(element_window, textvariable=v1, width=44)

                label_2_2 = Label(element_window, text="Klasa: ", padx=10, pady=10)
                list = []
                i = 0
                for item in core.curriculumsArray:
                    item = str(i + 1) + " " + str(item)
                    list.append(str(item))
                    i += 1
                entry_2_2 = ttk.Combobox(element_window, values=list, width=40)
                entry_2_2.current(core.curriculumsArray.index(core.coursesArray[id].curriculum))

                label_2_2_2 = Label(element_window, text="Dodatkowa klasa: ", padx=10, pady=10)
                list = []
                i = 0
                list.append("BRAK")
                for item in core.curriculumsArray:
                    item = str(i + 1) + " " + str(item)
                    list.append(str(item))
                    i += 1
                entry_2_2_2 = ttk.Combobox(element_window, values=list, width=40)
                if core.coursesArray[id].curriculum2 is not None:
                    entry_2_2_2.current(core.curriculumsArray.index(core.coursesArray[id].curriculum2) + 1)
                else:
                    entry_2_2_2.current(0)

                label_2_2_3 = Label(element_window, text="Dodatkowa klasa: ", padx=10, pady=10)
                list = []
                i = 0
                list.append("BRAK")
                for item in core.curriculumsArray:
                    item = str(i + 1) + " " + str(item)
                    list.append(str(item))
                    i += 1
                entry_2_2_3 = ttk.Combobox(element_window, values=list, width=40)
                if core.coursesArray[id].curriculum3 is not None:
                    entry_2_2_3.current(core.curriculumsArray.index(core.coursesArray[id].curriculum3) + 1)
                else:
                    entry_2_2_3.current(0)

                label_2_2_4 = Label(element_window, text="Dodatkowa klasa: ", padx=10, pady=10)
                list = []
                i = 0
                list.append("BRAK")
                for item in core.curriculumsArray:
                    item = str(i + 1) + " " + str(item)
                    list.append(str(item))
                    i += 1
                entry_2_2_4 = ttk.Combobox(element_window, values=list, width=40)
                if core.coursesArray[id].curriculum3 is not None:
                    entry_2_2_4.current(core.curriculumsArray.index(core.coursesArray[id].curriculum4) + 1)
                else:
                    entry_2_2_4.current(0)

                label_3_2 = Label(element_window, text="Nauczyciel: ", padx=10, pady=10)
                list = []
                i = 0
                for item in core.teachersArray:
                    item = str(i + 1) + " " + str(item)
                    list.append(str(item))
                    i += 1
                entry_3_2 = ttk.Combobox(element_window, values=list, width=40)
                entry_3_2.current(core.teachersArray.index(core.coursesArray[id].teacher))

                label_4_2 = Label(element_window, text="Konkretna sala: ", padx=10, pady=10)
                list = []
                i = 0
                list.append("BRAK")
                for item in core.roomsArray:
                    item = str(i + 1) + " " + str(item)
                    list.append(str(item))
                    i += 1
                entry_4_2 = ttk.Combobox(element_window, values=list, width=40)
                if core.coursesArray[id].room is not None:
                    entry_4_2.current(core.roomsArray.index(core.coursesArray[id].room) + 1)
                else:
                    entry_4_2.current(0)

                label_5_2 = Label(element_window, text="Liczba godzin lekcyjnych: ", padx=10, pady=10)
                v5 = StringVar(options_window)
                v5.set(core.coursesArray[id].lenght)
                entry_5_2 = Spinbox(element_window, from_=1, to=core.numbers_of_Time, textvariable=v5, width=41)

                button_ok_2 = Button(element_window, text="OK", width=10, command=lambda: options_ok(id))
                button_exit_2 = Button(element_window, text="Anuluj", width=10,
                                       command=lambda: element_window.destroy())

                label_2.grid(row=0, column=0, columnspan=2)

                label_1_2.grid(row=1, column=0)
                entry_1_2.grid(row=1, column=1)

                label_2_2.grid(row=2, column=0)
                entry_2_2.grid(row=2, column=1)

                label_2_2_2.grid(row=3, column=0)
                entry_2_2_2.grid(row=3, column=1)

                label_2_2_3.grid(row=4, column=0)
                entry_2_2_3.grid(row=4, column=1)

                label_2_2_4.grid(row=5, column=0)
                entry_2_2_4.grid(row=5, column=1)

                label_3_2.grid(row=6, column=0)
                entry_3_2.grid(row=6, column=1)

                label_4_2.grid(row=7, column=0)
                entry_4_2.grid(row=7, column=1)

                # label_5_2.grid(row=7, column=0)
                # entry_5_2.grid(row=7, column=1)

                button_ok_2.grid(row=8, column=0, padx=10, pady=10)
                button_exit_2.grid(row=8, column=1, padx=10, pady=10)

                def options_ok(id):
                    try:
                        if entry_1_2.get() != "" and entry_2_2.get() != "" and entry_3_2.get() != "" and entry_4_2.get() != "" and entry_5_2.get() != "":
                            curriculum_id = int(entry_2_2.get().split(" ")[0]) - 1
                            teacher_id = int(entry_3_2.get().split(" ")[0]) - 1
                            curriculum2 = None
                            curriculum3 = None
                            curriculum4 = None
                            room = None
                            if entry_2_2_2.get() != "BRAK":
                                curriculum2 = core.curriculumsArray[int(entry_2_2_2.get().split(" ")[0]) - 1]
                            if entry_2_2_3.get() != "BRAK":
                                curriculum3 = core.curriculumsArray[int(entry_2_2_3.get().split(" ")[0]) - 1]
                            if entry_2_2_4.get() != "BRAK":
                                curriculum4 = core.curriculumsArray[int(entry_2_2_4.get().split(" ")[0]) - 1]
                            if entry_4_2.get() != "BRAK":
                                room = core.roomsArray[int(entry_4_2.get().split(" ")[0]) - 1]
                            core.coursesArray[id].name = entry_1_2.get()
                            core.coursesArray[id].curriculum = core.curriculumsArray[curriculum_id]
                            core.coursesArray[id].curriculum2 = curriculum2
                            core.coursesArray[id].curriculum3 = curriculum3
                            core.coursesArray[id].curriculum4 = curriculum4
                            core.coursesArray[id].teacher = core.teachersArray[teacher_id]
                            core.coursesArray[id].room = room
                            core.coursesArray[id].lenght = int(entry_5_2.get())
                            element_list.delete(id)
                            element_list.insert(id, str(id + 1) + " " + str(core.coursesArray[id]))
                        else:
                            information_Text.config(text="Edytowany element musi mieć poprawnie podane wszystkie pola.")
                    except Exception as e:
                        print("Error: " + str(e))
                    element_window.destroy()
            except Exception as e:
                print("Error2: " + str(e))

        def options_delete():
            global deleted_count
            if not element_list.get(ANCHOR):
                information_Text.config(text="Wybierz element z listy.")
                return
            information_Text.config(text="")
            try:
                del core.coursesArray[int(element_list.get(ANCHOR).split(" ")[0]) - 1]
                element_list.delete(0, 'end')
                i = 0
                for item in core.coursesArray:
                    item = str(i + 1) + " ) " + str(item)
                    element_list.insert(END, str(item))
                    i += 1
                deleted_count += 1
            except Exception as e:
                print("Error: " + str(e))

    def generate_button(self):

        export_window = Toplevel(self.root, padx=10, pady=10)
        export_window.grab_set()
        label_example = Label(export_window, text="GENEROWANIE PLANU.\nProces ten może potrwać.", padx=10, pady=10)
        button_yes = Button(export_window, text="GENERUJ", width=10, command=lambda: options_ok())
        button_no = Button(export_window, text="Anuluj", width=10, command=lambda: export_window.destroy())

        label_example.grid(row=0, column=0, columnspan=2)
        button_yes.grid(row=1, column=0, padx=10, pady=10)
        button_no.grid(row=1, column=1, padx=10, pady=10)

        def options_ok():
            w = Label(export_window, text="GENEROWANIE...")
            button_yes.destroy()
            button_no.destroy()
            w.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
            try:
                success, result = core.generate()
                if not success:
                    self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Z aktualnych aktywności nie da się ułożyć bezkolizijnego planu.")
                else:
                    self.generate_elements()
                    self.status.config(text=time.strftime("%H:%M",
                                                          time.localtime()) + " Wygenerowano plan.")
            except Exception as e:
                 self.status.config(text=time.strftime("%H:%M", time.localtime()) + " Przy generowaniu planu napotkano na problem.")
            export_window.destroy()

    def options(self):
        options_window = Toplevel(self.root, padx=10, pady=10)
        options_window.grab_set()
        label = Label(options_window, text="Ustawienia planu", padx=10, pady=10)

        label_day = Label(options_window, text="Ilość dni: ", padx=10, pady=10)
        var_day = StringVar(options_window)
        var_day.set(core.numbers_of_Day)
        spinbox_day = Spinbox(options_window, from_=1, to=21, textvariable=var_day)

        label_time = Label(options_window, text="Ilość godzin w dniu: ", padx=10, pady=10)
        var_time = StringVar(options_window)
        var_time.set(core.numbers_of_Time)
        spinbox_time = Spinbox(options_window, from_=1, to=48, textvariable=var_time)

        label_break = Label(options_window, text="Zezwolenie na okienka w planie: ", padx=10, pady=10)
        var_brake = BooleanVar()
        var_brake.set(core.breaks_in_plan)
        checkbox_break = Checkbutton(options_window, text="", variable=var_brake)

        button_ok = Button(options_window, text="OK", width=10, command=lambda: options_ok())
        button_exit = Button(options_window, text="Anuluj", width=10,
                             command=lambda: options_window.destroy())

        label.grid(row=0, column=0, columnspan=2)

        label_day.grid(row=1, column=0)
        spinbox_day.grid(row=1, column=1)

        label_time.grid(row=2, column=0)
        spinbox_time.grid(row=2, column=1)

        label_break.grid(row=3, column=0)
        checkbox_break.grid(row=3, column=1)

        button_ok.grid(row=4, column=0, padx=10, pady=10)
        button_exit.grid(row=4, column=1, padx=10, pady=10)

        def options_ok():
            try:
                value1 = int(spinbox_day.get())
                value2 = int(spinbox_time.get())

                core.numbers_of_Day = value1
                core.numbers_of_Time = value2
                core.breaks_in_plan = var_brake.get()
                # print(core.breaks_in_plan)

                options_window.destroy()
            except Exception as e:
                print("Error: " + str(e))

    def generate_elements(self):
        for widget in self.content1.winfo_children():
            widget.destroy()

        content = Canvas(self.content1, height=500, scrollregion=(0, 0, 500, 500), background="white")

        scrollbar = Scrollbar(self.content1, orient="vertical", command=content.yview)
        scrollbar2 = Scrollbar(self.content1, orient="horizontal", command=content.xview)
        scrollbar.pack(fill='y', side='right')
        scrollbar2.pack(fill='x', side='bottom')
        # self.body.config(scrollregion=self.body.bbox('all'), yscrollcommand=self.scrollbar_y.set)

        body = Canvas(content)
        body.config(bg="#ffffff")
        color_map = {}

        for i in range(core.numbers_of_Day):
            d = Label(body, text=("Dzień\n" + str(i + 1)), bg="#ababab",
                      height=(int(3 * core.numbers_of_Time)))
            d.grid(row=(i * core.numbers_of_Time + 1), column=0, rowspan=core.numbers_of_Time)

        for i in range(core.numbers_of_Day * core.numbers_of_Time):
            if i % 2 == 0:
                color = "#fafafa"
            else:
                color = "#eaeaea"
            t = Label(body, text=(str((i % core.numbers_of_Time) + 1)), bg=color, height=3, width=2)
            t.grid(row=i + 1, column=1)

        cur = 0
        for i in range(len(core.curriculumsArray)):
            k = Label(body, text=(str(core.curriculumsArray[i].name)), bg="#ababab",
                      height=2, width=17)
            k.grid(row=0, column=2 + i)
            muz = 1
            # print(result[cur])
            count = 0
            for j in core.time_array[cur]:
                if count % 2 == 0:
                    color = "#ffffff"
                else:
                    color = "#efefef"
                count += 1
                l = Label(body, bg=color, height=3, width=17)
                l.pack_propagate(False)
                if j is not None:
                    # if (j.name, j.teacher) not in color_map.keys():
                    #     color_map[(j.name, j.teacher)] = random_color()
                    # color = color_map[(j.name, j.teacher)]
                    if j.name not in color_map.keys():
                        color_map[j.name] = random_color()
                    color = color_map[j.name]
                    l.config(bg=color)
                    rooms = ""
                    if j.room:
                        rooms = j.room.number
                    b = Button(l, text=str(j.name + "\n" + j.teacher.name + " " +
                                           j.teacher.surname + "\n" + rooms), borderwidth=0, bg=color,
                               command=lambda j=j, cur=cur: options_edit_time(j, cur))
                    b.pack()
                l.grid(row=muz, column=2 + i)
                muz += 1
            cur += 1
        content.create_window(0, 0, anchor='nw', window=body)
        content.update_idletasks()
        content.configure(scrollregion=content.bbox('all'), yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set)
        content.pack(fill='both', expand=True, side='left')

        def options_edit_time(course, time_array_index):
            element_window = Toplevel(self.root, padx=10, pady=10)
            element_window.grab_set()
            label_2 = Label(element_window, text=str(course), padx=10, pady=10)
            label_1_2 = Label(element_window, text="(Możesz zmienić godzinę na inną niekolidujący) ", padx=10, pady=10)
            list = []
            i = 0
            starti = -1
            for item in core.time_array[time_array_index]:
                if item is None:
                    for x in core.time_array:
                        if x[i] is not None and (x[i].teacher == course.teacher or x[i].room == course.room):
                            break
                    else:
                        if core.time_array[core.curriculumsArray.index(course.curriculum)][i] is not None:
                            pass
                        elif(course.curriculum2 is not None and
                                 core.time_array[core.curriculumsArray.index(course.curriculum2)][i] is not None):
                            pass
                        elif(course.curriculum3 is not None and
                                 core.time_array[core.curriculumsArray.index(course.curriculum3)][i] is not None):
                            pass
                        elif(course.curriculum4 is not None and
                                 core.time_array[core.curriculumsArray.index(course.curriculum4)][i] is not None):
                            pass
                        else:
                            list.append(
                                "Dzień " + str(int(i / core.numbers_of_Time) + 1) + " Godzina " + str(
                                    (i % core.numbers_of_Time) + 1))
                elif item is course:
                    list.append(
                        "Dzień " + str(int(i / core.numbers_of_Time) + 1) + " Godzina " + str(
                            (i % core.numbers_of_Time) + 1))
                    starti = len(list) - 1
                i += 1
            entry_1_2 = ttk.Combobox(element_window, values=list, width=40)
            entry_1_2.current(starti)

            button_ok_2 = Button(element_window, text="OK", width=10,
                                 command=lambda course=course, time_array_index=time_array_index:
                                 options_ok(course, time_array_index))
            button_exit_2 = Button(element_window, text="Anuluj", width=10,
                                   command=lambda: element_window.destroy())

            label_2.grid(row=0, column=0, columnspan=2)

            label_1_2.grid(row=2, column=0, columnspan=2)
            entry_1_2.grid(row=1, column=0, columnspan=2)

            button_ok_2.grid(row=3, column=0, padx=10, pady=10)
            button_exit_2.grid(row=3, column=1, padx=10, pady=10)

            def options_ok(c, i):
                try:
                    time = (int(entry_1_2.get().split(" ")[1]) - 1) * core.numbers_of_Time \
                           + (int(entry_1_2.get().split(" ")[3]) - 1)
                    old = core.time_array[i].index(c)
                    #core.time_array[i][time] = c
                    #core.time_array[i][old] = None

                    i1 = core.curriculumsArray.index(c.curriculum)
                    core.time_array[i1][time] = c
                    core.time_array[i1][old] = None

                    if c.curriculum2 is not None:
                        i2 = core.curriculumsArray.index(c.curriculum2)
                        core.time_array[i2][time] = c
                        core.time_array[i2][old] = None

                    if c.curriculum3 is not None:
                        i3 = core.curriculumsArray.index(c.curriculum3)
                        core.time_array[i3][time] = c
                        core.time_array[i3][old] = None

                    if c.curriculum4 is not None:
                        i4 = core.curriculumsArray.index(c.curriculum4)
                        core.time_array[i4][time] = c
                        core.time_array[i4][old] = None
                    self.generate_elements()
                except Exception as e:
                    pass
                    # print("Error: " + str(e))
                element_window.destroy()


GUI()
