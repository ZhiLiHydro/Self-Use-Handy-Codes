#!/usr/bin/env python3
# coding: utf-8
from string import ascii_lowercase, punctuation
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def generate(fin, fout):
    """
    Search first author last name, year, and first meaningful word in title.
    Assemble Google-Scholar-style keys (lastname+year+titlefirstword).
    Replace original keys ``RN+number" with new keys.

    Also adds letter suffixes to repeated keys 
    (e.g. peter1998researcha, peter1998researchb).
    
    """
    keyList = []
    meaninglesswordList = ['a', 'an', 'the', 'on', 'in', 'upon', 'before', 'after',
                     'with', 'by', 'for', 'at', 'about', 'under', 'of', 'to', 'from',
                     'is', 'are', 'am', 'why', 'what', 'where', 'when', 'who', 'how',
                     'because', 'as', 'since', 'between', 'beyond', 'near', 'off', 'over',
                     'through', 'toward', 'towards', 'per', 'past', 'without'] ## should be enough..
    symbolList = list(punctuation) 

    with open(fin, 'r') as f:
        lastname, title, year = '', '', ''
        done = False
        for line in f:
            if '@' in line:
                lastname, title, year = '', '', ''
                done = False
            if line.replace(' ', '').startswith('author='):
                lastname = line.split('=')[1]
                for symbol in symbolList:
                    lastname = lastname.replace(symbol, ' ')
                lastname = lastname.split()[0].lower()
            if line.replace(' ', '').startswith('title='):
                title = line.split('=')[1].replace('{', '').replace('}', '')
                if title.split()[0] in ['1-D', '2-D', '3-D']:
                    title = title.split()[0].replace('-', '').lower()
                else:
                    for symbol in symbolList:
                        title = title.replace(symbol, ' ')
                    for title in title.split():
                        title = title.lower()
                        if title in meaninglesswordList:
                            continue
                        else:
                            break
            if line.replace(' ', '').startswith('year='):
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
                    if '@' in line: ## assemble keys
                        line = line.replace(line.split('{')[1].split(',')[0], keyList[i])
                        i += 1
                    if line.replace(' ', '').startswith('title=') or line.replace(' ', '').startswith('journal='):
                        line = line.replace('&', '\&') ## make '&' symbol visible in BibTex
                        line = line.replace('{', '{{') ## lock title and journal name to avoid...
                        line = line.replace('}', '}}') ## ...automatic UPPER to lower case change
                    if line.replace(' ', '').startswith('journal='):
                        if 'Ieee' in line:
                            line = line.replace('Ieee', 'IEEE')
                        if 'Asce' in line:
                            line = line.replace('Asce', 'ASCE')
                        if 'Asme' in line:
                            line = line.replace('Asme', 'ASME')
                    if line.replace(' ', '').startswith('university='): ## it seems only 'school' works for...
                        line = line.replace('university', 'school', 1)  ## ...phdthesis type; 'university' not working
                    if line.replace(' ', '').startswith('DOI='): ## fix common issues in DOI
                        for useless in ['Artn','ARTN','Unsp','UNSP', 'Pii', 'PII']:
                            if useless in line:
                                line = line.split(useless)[0]
                        if line.replace(' ', '').startswith('DOI={Doi'):
                            line = line.replace('Doi ','')
                        if line.replace(' ', '').startswith('DOI={DOI'):
                            line = line[::-1].replace(' IOD','',1)[::-1]
                        if line.replace(' ', '').startswith('DOI={Book_Doi'):
                            line = line.replace('Book_Doi ','')
                    if line.split(' ')[0] in ['Artn','ARTN','Unsp','UNSP', 'Pii', 'PII']:
                        continue
                    if line.startswith('Doi 10'):
                        line = line.replace('Doi ','')
                    if line.startswith('DOI 10'):
                        line = line.replace('DOI ','')
                    if line.replace(' ', '').startswith('url=') or line.replace(' ', '').startswith('http'):
                        continue ## remove long url if [Find Full Text]ed in EndNote
                    fo.write(line)
    return keyList, len(keyList), count


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
            keyList, processedkeys, allkeys = generate(finvar.get(), foutvar.get())
            if processedkeys != allkeys:
                message = '\''+foutvar.get()+'\' CANNOT be generated\nError: '\
                          +str(processedkeys)+' out of '+str(allkeys)+' OK\n'\
                          +'Check if each BibTex entry contains AUTHOR, TITLE and YEAR'\
                          +'\n\nTip: Check entries with \'Reference Type = Conference Paper '\
                          +'or Conference Proceedings\', as they are always troublemakers'\
                          +'\n\nPrint result in command line?\n'
            else:
                message = '\''+foutvar.get()+'\' has been generated\n'\
                          +str(processedkeys)+' BibTex entries in total\n\nPrint result in command line?\n'
            if messagebox.askyesno(
                message=message,
                icon='info'):
                print('\\cite{'+str(keyList)[2:-2].replace('\', \'','}\n\\cite{')+'}')
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

