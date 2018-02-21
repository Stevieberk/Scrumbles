import tkinter as tk

import matplotlib
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import csv
import tkcalendar
import datetime

from styling import styling as style

class SList(tk.Frame):
    def __init__(self, controller, title):
        tk.Frame.__init__(self, controller)

        self.titleFrame = tk.Frame(self, bg=style.scrumbles_blue, relief=tk.SOLID, borderwidth=1)
        self.titleLabel = tk.Label(self.titleFrame, text=title, bg=style.scrumbles_blue, relief=tk.FLAT)
        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listFrame, selectmode=tk.BROWSE, yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.config(command=self.listbox.yview)

        self.typeSort = "none"

        self.sortButton = tk.Button(self.titleFrame, text=style.updown_arrow, bg=style.scrumbles_blue, command=lambda: self.decideSort(), relief=tk.FLAT)
        self.titleLabel.pack(side=tk.LEFT)
        self.sortButton.pack(side=tk.RIGHT)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.titleFrame.pack(fill=tk.X, expand=False)
        self.listFrame.pack(fill=tk.BOTH, expand=True)

    def importList(self, list):
        self.clearList()
        for item in list:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def importListSorted(self, list):
        self.clearList()
        for item in list:
            self.listbox.insert(tk.END, item)

    def appendList(self, list):
        for item in list:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def addItem(self, item):
        self.listbox.insert(tk.END, item)
        self.enforceSort()

    def sortForward(self):
        items = self.listbox.get(0, tk.END)
        items = sorted(items)
        self.importListSorted(items)

    def sortReverse(self):
        items = self.listbox.get(0, tk.END)
        items = sorted(items, reverse=True)
        self.importListSorted(items)

    def clearList(self):
        self.listbox.delete(0, tk.END)

    def deleteSelectedItem(self):
        self.listbox.delete(tk.ANCHOR)
        self.enforceSorting()

    def decideSort(self):
        if self.typeSort == "none":
           self.typeSort = "forward"
           self.sortButton["text"] = style.up_arrow
           self.sortForward()
        elif self.typeSort == "forward":
            self.typeSort = "reverse"
            self.sortButton["text"] = style.down_arrow
            self.sortReverse()
        else:
            self.typeSort = "forward"
            self.sortButton["text"] = style.up_arrow
            self.sortForward()

    def enforceSort(self):
        if self.typeSort == "none":
            return
        elif self.typeSort == "forward":
            self.sortForward()
        else:
            self.sortReverse()

class SLineGraph(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)

        self.x = [1,2,3,4,5,6,7,8,9,10]
        self.y = [1,4,2,5,1,4,2,5,1,4]
        self.label = None

        self.figure = Figure(figsize=(4, 4), dpi=100)
        self.graph = self.figure.add_subplot(1,1,1)


    def setTitle(self, title):
        self.label = tk.Label(self, text=title)

    def setAxes(self, xAxis, yAxis):
        self.graph.set_xlabel(xAxis)
        self.graph.set_ylabel(yAxis)
        self.figure.subplots_adjust(left=.15)
        self.figure.subplots_adjust(bottom=.15)

    def importDataFromCSV(self, fileName, delimeter):
        with open(fileName, 'r') as file:
            plots = csv.reader(file, delimeter)
            for row in plots:
                self.x.append(int(row[0]))
                self.y.append(int(row[1]))

    def displayGraph(self):
        self.graph.plot(self.x, self.y)
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.show()
        if self.label is not None:
            self.label.pack(side=tk.TOP, fill=tk.X)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=1, pady=1)

    def changeBackgroundColor(self, color):
        self.graph.set_facecolor(facecolor=color)

class SCalendar(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)
        now = datetime.datetime.now()
        self.cal = tkcalendar.Calendar(self, font="Arial 14", selectmode='day', year=now.year, month=now.month, day=now.day)
        self.cal.pack(side=tk.TOP, fill=tk.BOTH)