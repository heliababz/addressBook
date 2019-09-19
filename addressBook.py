#File Name: addressbook.py
#Programmer: Helia Aghababazadeh
#Description: searchable address book, reads data from a csv file 

from tkinter import *
from tkinter import ttk
import csv

class AddressbookGUI:

    fileName = 'addressBook.csv'
       
    def __init__(self, master):
        
        master.title('Adress book')
 #       master.resizable(False, False)
        master.configure(background = '#0ea4b2')

        self.style = ttk.Style()
        self.style.configure('TFrame')
        self.style.configure('TButton', font = ('Tahoma', 10,))
        self.style.configure('TLabel', font = ('Tahoma', 11,))
        self.style.configure('Header.TLabel', font = ('Tahoma', 18, 'bold'))

        self.frame_header = ttk.Frame(master) 
        self.frame_header.pack()
        
        self.big_logo = PhotoImage(file = 'hexcube.gif')
        self.logo = self.big_logo.subsample(10,10)


        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2)
        ttk.Label(self.frame_header, text = 'Address book search bar', style = 'Header.TLabel').grid(row = 0, column = 1)


        self.searchFrame = ttk.Frame(master)
        self.searchFrame.pack()

        ttk.Label(self.searchFrame, text = 'Search Name, Number, or Email'). grid (row = 0, column = 0, padx = 5)
        ttk.Label(self.searchFrame, text = 'Search Address'). grid (row = 0, column = 1, padx = 5)
        ttk.Label(self.searchFrame, text = 'Search Area: zipdoce, state, etc.'). grid (row = 0, column = 2, padx = 5)
        
        self.search_Entry1 = ttk.Entry(self.searchFrame)
        self.search_Entry2 = ttk.Entry(self.searchFrame)
        self.search_Entry3 = ttk.Entry(self.searchFrame)
        ttk.Button(self.searchFrame, text = 'Search', command = self.search).grid(row = 1, column = 4, padx = 5)

        self.search_Entry3.grid( row = 1, column = 2, padx = 5)
        self.search_Entry2.grid(row = 1, column = 1, padx = 5)
        self.search_Entry1.grid(row = 1, column = 0, padx = 5)
        
        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()
        

# Determines which field was used and what to look for when it does it calles findinRow(strr)
# function and if there is a match adds it to the list of matching rows

    def search(self):
        infoList = self.search_Entry1.get().split()
        addressList = self.search_Entry2.get()
        areaList = self.search_Entry3.get().split()

        matchRowList = []
        if len(infoList) != 0:
            
            for strr in infoList:
                if self.isNum(strr):
                    temp  = self.findinRow(strr, 7)
                    for row in self.findinRow(strr, 8):
                        temp.append(row)

                    if not temp:
                        temp = self.findinRow(strr, 6)

                    for row in temp:
                        matchRowList.append(row)
                                                
                elif self.isEmail(strr):
                    temp  = self.findinRow(strr, 9)
                    for row in temp:
                        matchRowList.append(row)
                else:
                    temp = self.findinRow(strr, 0)
                    for row in self.findinRow(strr, 1):
                        temp.append(row)                      
                    if not temp:
                        temp = self.findinRow(strr, 3)
                    if not temp:
                        temp = self.findinRow(strr, 4)
                    if not temp:
                        temp = self.findinRow(strr, 5)

                    for i in temp:
                        matchRowList.append(i)                      
                
        if len(addressList) != 0:
            temp = self.findinRow(addressList, 2)
            for i in temp:
                matchRowList.append(i)
                
        if len(areaList) != 0:
            for strr in areaList:
                if self.isNum(strr):
                    temp = self.findinRow(strr, 6)

                elif len(strr) == 2:
                    temp = self.findinRow(strr, 5)

                else:
                    temp = self.findinRow(strr, 4)
                    for i in self.findinRow(strr, 3):
                        temp.append(i)

                for i in temp:
                    matchRowList.append(i)
        self.display(matchRowList)

 #       matchRowList = list(dict.fromkeys(matchRowList))
        self.clear()

        return matchRowList
    

    def clear(self):
        self.search_Entry1.delete(0, 'end')
        self.search_Entry2.delete(0, 'end')
        self.search_Entry3.delete(0, 'end')

 # calls reducePhone() function to remove '-()' characters that might be part of a
 # telephone number the checks if the remaining characters are digits
 
    def isNum(self, strr): #can be Phone number or zipcode
        condition = True
        strr = self.reducePhone(strr)
        for i in strr:
            if i.isdigit() == False:
                condition = False                
        return condition

    def isEmail(self,strr):
        condition = False
        for char in strr:
            if char in "@":
                condition = True
        return condition

#reads file and looks for the passed in parameter in the passed in column index
#makes sure extra characters are removed from phone numbers and all characters are
# lowercase to make it easier to compare strings
    def findinRow(self, strr, index):
        indexColumn = []
        answerList = []
        count = 0
        with open ('addressBook.csv') as csvfile:
            file = csv.reader(csvfile, delimiter  =',')
            for row in file:
                indexColumn.append(row[index])
            count = 0
            for word in indexColumn:
                if index == 7 or index == 8:
                    temp1 = self.reducePhone(strr)
                    temp2 = self.reducePhone(word)

                    if temp1 in temp2:
                        answerList.append(count)
                    count+=1
                else:
                    strr = strr.lower()
                    word = word.lower()
                    if strr in word:
                        answerList.append(count)
                    count += 1
        return answerList
                
#removes '-()' characters that might be part of a telephone number       
    def reducePhone(self, strr):
        for char in strr:
            if char in "-()":
                strr = strr.replace(char,'')
        return strr


    def display (self, answerList):

        
        with open ('addressBook.csv') as csvfile:
            list = self.frame_content.grid_slaves()
            for l in list:
                l.destroy()
                
            file = csv.reader(csvfile, delimiter  =',')
            i = 0
            x = 0
            for row in file:
                if i in answerList:
                    ttk.Label(self.frame_content, text = '').grid(row = x, column = 0)
                    ttk.Label(self.frame_content, text = row).grid(row = x+1, column = 0)
                    x += 2
                i += 1;
         
def main():
                
    root = Tk()
    adressBook = AddressbookGUI(root)
    root.mainloop()
    
if __name__ == "__main__": main()

