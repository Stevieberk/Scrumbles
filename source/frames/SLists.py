import tkinter as tk

from styling import styling as style
from tkinter import ttk

class ColorSchemes:
    incompleteAssignmentColorScheme = {'bg': 'firebrick4', 'fg': 'VioletRed1'}
    assignedScheme = {'bg': style.scrumbles_blue, 'fg': 'navy'}
    inProgressColorScheme = {'bg': 'khaki', 'fg': 'dark green'}
    submittedColorScheme = {'bg': style.scrumbles_orange, 'fg': 'black'}
    epicItemColorScheme = {'bg': 'MediumPurple1', 'fg': 'black'}
    completedItemColorScheme = {'bg': style.scrumbles_green_bg, 'fg': style.scrumbles_green_fg}


class BaseList(tk.Frame, tk.Listbox):
    def __init__(self, controller):
        self.fullList = []
        self.controller = controller

    def showPartialList(self, list):
        self.clearList()
        for item in list:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def showFullList(self):
        self.clearList()
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def importList(self, list):
        self.deleteList()
        self.fullList = list
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def importItemList(self, items):
        self.deleteList()
        listOfNames = []
        for item in items:
            listOfNames.append(item.itemTitle)
        self.fullList = listOfNames
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def importProjectList(self, projects):
        self.deleteList()
        listOfNames = []
        for project in projects:
            listOfNames.append(project.projectName)
        self.fullList = listOfNames
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def importSprintsList(self, sprints):
        self.deleteList()
        listOfNames = []
        for sprint in sprints:
            listOfNames.append(sprint.sprintName)
        self.fullList = listOfNames
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def importListSorted(self, list):
        self.deleteList()
        self.fullList = list
        for item in self.fullList:
            self.listbox.insert(tk.END, item)

    def appendList(self, list):
        for item in list:
            self.fullList.append(item)
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def addItem(self, item):
        self.fullList.append(item)
        self.listbox.insert(tk.END, item)
        self.enforceSort()

    def sortForward(self):
        self.fullList = sorted(self.fullList, key=lambda s: self.processSort(s))
        self.importListSorted(self.fullList)

    def sortReverse(self):
        self.fullList = sorted(self.fullList, key=lambda s: self.processSort(s), reverse=True)
        self.importListSorted(self.fullList)

    def processSort(self, string):
        string = string.lower()
        string = "".join(string.split())
        return string

    def clearList(self):
        self.listbox.delete(0, tk.END)

    def deleteList(self):
        self.listbox.delete(0, tk.END)
        self.fullList = []

    def deleteSelectedItem(self):

        selection = self.listbox.curselection()
        self.listbox.delete(selection[0])
        val = self.listbox.get(selection[0])
        index = self.fullList.index(val)
        del(self.fullList[index])

        self.enforceSort()

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

    def search(self, str):
        def fulfillsCondition(item, str):
            return item[:len(str)].lower() == str.lower()

        matches = [x for x in self.fullList if fulfillsCondition(x, str)]
        self.showPartialList(matches)


class SComboList(BaseList):
    def __init__(self, controller, title, products):
        BaseList.__init__(self, controller)
        tk.Frame.__init__(self, controller)

        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self, textvariable = self.box_value, cursor = "hand2")
        self.box['values'] = (products)
        self.box.current(0)
        self.box.pack(fill = tk.X)

        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL, cursor = "hand2")
        self.listbox = tk.Listbox(self.listFrame,
                                  selectmode = tk.BROWSE,
                                  yscrollcommand=self.listScrollbar.set,
                                  cursor = "hand2")
        self.listScrollbar.config(command = self.listbox.yview)

        self.typeSort = "none"
        self.listbox.pack(side = tk.LEFT, fill = tk.BOTH)
        self.listScrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.listFrame.pack(fill = tk.BOTH, expand = True)

class SBacklogList(BaseList):
    def __init__(self, controller, title, MasterView=None, canAdd=True):
        BaseList.__init__(self, controller)
        tk.Frame.__init__(self, controller)
        self.MasterView = MasterView
        self.titleFrame = tk.Frame(self, bg = style.scrumbles_blue, relief = tk.SOLID, borderwidth = 1)
        self.searchFrame = tk.Frame(self.titleFrame, relief = tk.SOLID, bg = style.scrumbles_blue)

        self.searchLabel = tk.Label(self.searchFrame, text = "Search:", bg = style.scrumbles_blue)
        self.searchEntry = tk.Entry(self.searchFrame, cursor = "hand2")
        self.searchButton = tk.Button(self.searchFrame,
                                      text = style.right_enter_arrow,
                                      bg = style.scrumbles_blue,
                                      command = lambda: self.search(self.searchEntry.get()),
                                      relief = tk.FLAT,
                                      cursor = "hand2")
        self.undoSearchButton = tk.Button(self.searchFrame,
                                          text = style.cancel_button,
                                          bg = style.scrumbles_blue,
                                          command = lambda: self.clearSearchEntry(),
                                          relief = tk.FLAT,
                                          cursor = "hand2")

        self.searchEntry.bind('<Return>', lambda event: self.search(self.searchEntry.get()))
        self.undoSearchButton.pack(side = tk.RIGHT)
        self.searchButton.pack(side = tk.RIGHT)
        self.searchEntry.pack(side = tk.RIGHT)
        self.searchLabel.pack(side = tk.RIGHT)

        self.titleLabel = tk.Label(self.titleFrame,
                                   text = title,
                                   bg = style.scrumbles_blue,
                                   relief = tk.FLAT)
        self.sortButton = tk.Button(self.titleFrame,
                                    text = style.updown_arrow,
                                    bg = style.scrumbles_blue,
                                    command = lambda: self.decideSort(),
                                    relief = tk.FLAT,
                                    cursor = "hand2")

        self.titleLabel.pack(side = tk.LEFT)
        if MasterView is not None and canAdd is True:
            self.addButton = tk.Button(self.titleFrame, text=style.big_plus, font='Helvetica 14', bg=style.scrumbles_blue,
                                       command=lambda: MasterView.showCreateItemDialog(), relief=tk.FLAT,cursor="hand2")
            self.addButton.pack(side=tk.LEFT, fill=tk.BOTH)
        self.sortButton.pack(side = tk.RIGHT)
        self.searchFrame.pack(side = tk.RIGHT)

        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient = tk.VERTICAL, cursor = "hand2")
        self.listbox = tk.Listbox(self.listFrame,
                                  selectmode = tk.BROWSE,
                                  yscrollcommand = self.listScrollbar.set,
                                  cursor = "hand2")
        self.listScrollbar.config(command = self.listbox.yview)

        self.typeSort = "none"
        self.titleFrame.pack(fill = tk.X, expand = False)
        self.listbox.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.listScrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.listFrame.pack(fill = tk.BOTH, expand = True)

    def clearSearchEntry(self):
        self.showFullList()
        self.searchEntry.delete(0,tk.END)

    def colorCodeListboxes(self):
        i = 0
        itemTitleMap = {}
        if self.MasterView is not None:
            itemList = self.MasterView.activeProject.listOfAssignedItems
        else:
            itemList = self.controller.controller.activeProject.listOfAssignedItems

        for item in itemList:
            itemTitleMap[item.itemTitle] = item

        for title in self.listbox.get(0, tk.END):
            if itemTitleMap[title].itemUserID is None or itemTitleMap[title].itemSprintID is None:
                self.listbox.itemconfig(i, ColorSchemes.incompleteAssignmentColorScheme)
            elif itemTitleMap[title].itemType == 'Epic':
                self.listbox.itemconfig(i, ColorSchemes.epicItemColorScheme)
            elif itemTitleMap[title].itemStatus == 1:
                self.listbox.itemconfig(i, ColorSchemes.assignedScheme)
            elif itemTitleMap[title].itemStatus == 2:
                self.listbox.itemconfig(i, ColorSchemes.inProgressColorScheme)
            elif itemTitleMap[title].itemStatus == 3:
                self.listbox.itemconfig(i, ColorSchemes.submittedColorScheme)
            elif itemTitleMap[title].itemStatus == 4:
                self.listbox.itemconfig(i, ColorSchemes.completedItemColorScheme)
            else:
              self.listbox.itemconfig(i, ColorSchemes.incompleteAssignmentColorScheme)

            if itemTitleMap[title].itemType == 'Epic':
                self.listbox.itemconfig(i, ColorSchemes.epicItemColorScheme)
            i += 1

class SBacklogListColor(SBacklogList):
    def __init__(self, controller, title, MasterView=None, canAdd=True):
        SBacklogList.__init__(self, controller, title, MasterView, canAdd)

    def sortForward(self):
        super().sortForward()
        self.colorCodeListboxes()

    def sortRevers(self):
        super().sortReverse()
        self.colorCodeListboxes()

    def importListSorted(self, list):
        self.deleteList()
        self.fullList = list
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.colorCodeListboxes()

    def clearSearchEntry(self):
        self.showFullList()
        self.searchEntry.delete(0,tk.END)
        self.colorCodeListboxes()

    def search(self, str):
        def fulfillsCondition(item,str):
            return item[:len(str)].lower() == str.lower()

        matches = [x for x in self.fullList if fulfillsCondition(x, str)]

        self.showPartialList(matches)
        self.colorCodeListboxes()

class SList(BaseList):
    def __init__(self, controller, title):
        BaseList.__init__(self, controller)
        tk.Frame.__init__(self, controller)

        self.titleFrame = tk.Frame(self,
                                   bg = style.scrumbles_blue,
                                   relief = tk.SOLID,
                                   borderwidth = 1)
        self.titleLabel = tk.Label(self.titleFrame,
                                   text = title,
                                   bg = style.scrumbles_blue,
                                   relief = tk.FLAT)
        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame,
                                          orient = tk.VERTICAL,
                                          cursor = "hand2")
        self.listbox = tk.Listbox(self.listFrame,
                                  selectmode = tk.BROWSE,
                                  yscrollcommand = self.listScrollbar.set,
                                  cursor = "hand2")
        self.listScrollbar.config(command=self.listbox.yview)

        self.typeSort = "none"

        self.sortButton = tk.Button(self.titleFrame,
                                    text = style.updown_arrow,
                                    bg = style.scrumbles_blue,
                                    command = lambda: self.decideSort(),
                                    relief = tk.FLAT,
                                    cursor = "hand2")

        self.titleLabel.pack(side = tk.LEFT)
        self.sortButton.pack(side = tk.RIGHT)
        self.listbox.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.listScrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.titleFrame.pack(fill = tk.X, expand = False)
        self.listFrame.pack(fill = tk.BOTH, expand = True)
