# coding: utf-8
from string import ascii_lowercase
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def generate(fin, fout):
    keyList = []
    emptywordList = ['a', 'an', 'the', 'on', 'in', 'with', 'by', 'for', 'at', 'about', 'under', 'of', 'to', 'is', 'are']
    symbolList = [',', '-', ':', '?', '!', '/', '\\', '(', ')', '\'', '\"', '{', '}', '[', ']', '%', '*']

    with open(fin, 'r') as f:
        for line in f:
            if '@' in line:
                lastname = ''
                title = ''
                year = ''
                done = False
            if 'author =' in line:
                lastname = line.split('=')[1].replace('\n', '')
                for symbol in symbolList:
                    lastname = lastname.replace(symbol, ' ')
                lastname = lastname.split()[0].lower()
            if 'title =' in line:
                title = line.split('{')[1].split('}')[0].lower()
                if title.split()[0] in ['1-d', '2-d', '3-d']:
                    title = title.split()[0].replace('-','')
                else:
                    for symbol in symbolList:
                        title = title.replace(symbol, ' ')
                    for title in title.split():
                        if title in emptywordList:
                            continue
                        else:
                            break
            if 'year =' in line:
                year = line.split('{')[1].split('}')[0]
            if len(lastname) != 0 and len(title) != 0 and len(year) != 0 and done == False:
                key = lastname + year + title
                keyList.append(key)
                done = True
    
    repeatedkeyList = []
    for key in keyList:
        if keyList.count(key) > 1:
            repeatedkeyList.append(key)
    repeatedkeyList = list(set(repeatedkeyList))

    for key in repeatedkeyList:
        for letter in ascii_lowercase:
            _list2str = ' '.join(keyList)
            _list2str = _list2str.replace(key+' ', key+letter+' ', 1)
            keyList = _list2str.split(' ')

    with open(fin, 'r') as f:
        count = '\n'.join(f.readlines()).count('@')

    if len(keyList) == count:
        with open(fout, 'w') as fo:
            with open(fin, 'r') as fi:
                i = 0
                for line in fi:
                    if '@' in line:
                        line = line.replace(line.split('{')[1].split(',')[0], keyList[i])
                        i += 1
                    fo.write(line)

    return len(keyList), count


def main():
    root = tk.Tk()
    root.title('Endnote2BibTeX')
    root.resizable(0, 0)

    row = tk.Frame(root)
    row.pack(side='top',padx=10,pady=10)

    tk.Label(
        row,
        text='Input File Name',
        width=20,
        font='System 10',
        anchor='c').pack(side='left')

    finvar = tk.StringVar()
    fin = ttk.Combobox(
        row,
        font='System 10',
        width=35,
        textvariable=finvar)
    fin.set('My EndNote Library.txt')
    fin.pack()

    row = tk.Frame(root)
    row.pack(side='top',padx=10,pady=10)

    tk.Label(
        row,
        text='Output File Name',
        width=20,
        font='System 10',
        anchor='c').pack(side='left')

    foutvar = tk.StringVar()
    fout = ttk.Combobox(
        row,
        font='System 10',
        width=35,
        textvariable=foutvar)
    fout.set('MyEndNoteLibrary.bib')
    fout.pack()

    row = tk.Frame(root)
    row.pack(side='top')

    def convert():
        try:
            processedkeys, allkeys = generate(finvar.get(), foutvar.get())
            if processedkeys != allkeys:
                message = '\''+foutvar.get()+'\' CANNOT be generated\nError: '\
                          +str(processedkeys)+' out of '+str(allkeys)+' OK\n'\
                          +'Check if each bib item contains author, title and year'
            else:
                message = '\''+foutvar.get()+'\' has been generated\n'\
                          +str(processedkeys)+' bib items in total'
            messagebox.showinfo(
                message=message,
                icon='info')
        except FileNotFoundError:
            messagebox.showinfo(
                message='The input file \''+finvar.get()+'\' not found',
                icon='info')

    tk.Button(
            row, 
            text='Convert', 
            font='System 11 bold', 
            command=convert,
            padx=50,
            pady=5).pack(side='left',padx=10,pady=10)
    
    root.mainloop()


if __name__ == '__main__':
    main()

