import sys
import os
import tkinter
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox


def DeleteEntryValue(event):
    #エントリーの中身を削除
    EditBox.delete(0, tkinter.END)
    #ファイル選択
    fTyp = [('画像ファイル', '*.png')]
    iDir = '/home/ユーザ名/'

    # askopenfilename 一つのファイルを選択する。
    filename = tkFileDialog.askopenfilename(filetypes=fTyp, initialdir=iDir)

    tkMessageBox.showinfo('FILE NAME is ...', filename)

    # askdirectory ディレクトリを選択する。
    # dirname = tkFileDialog.askdirectory(initialdir=iDir)

    # tkMessageBox.showinfo('SELECTED DIRECROTY is ...', dirname)

root = tkinter.Tk()
root.title(u"ブレイクライン抽出")
root.geometry("600x700")

#ラベル
Static1 = tkinter.Label(text=u'入力画像のパス')
Static1.pack()

#エントリー
EditBox = tkinter.Entry()
EditBox.insert(tkinter.END, "")
EditBox.pack()

#ボタン
Button = tkinter.Button(text=u'画像選択')
Button.bind("<Button-1>", DeleteEntryValue)
Button.pack()



root.mainloop()
