# -*- coding: utf-8 -*-

import sys
import os
import tkinter as tk
import cv2
import numpy as np
from tkinter import filedialog as filedialog
from tkinter import messagebox as tkMessageBox

import mouseParam as mp
import trim
import lineDetect as ld


# ファイル選択
def selectFilePath(event):
    # エントリーの中身を削除
    editBox.delete(0, tk.END)
    # ファイル選択
    fTyp = [("", "*.jpg")]
    iDir = "/home/ユーザ名/"

    # askopenfilename 一つのファイルを選択する。
    filePath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)

    editBox.insert(tk.END, filePath)

# 二点クリック
def imgShow(event):
    filePath = editBox.get()
    # 入力画像
    img = cv2.imread(filePath)

    wname = "img"
    cv2.namedWindow(wname)
    npoints = 2
    ptlist = mp.PointList(npoints)
    cv2.setMouseCallback(wname, mp.onMouse, [wname, img, ptlist])
    cv2.imshow(wname, img)
    cv2.waitKey()
    global point
    point = ptlist.ptlist
    cv2.destroyAllWindows()

# トリミング
def triming(event):
    filePath = editBox.get()
    global img
    img = trim.main(filePath, point)
    ld.main(img)
    tkMessageBox.showinfo('LineDetect', '完了')


root = tk.Tk()
root.title(u"ブレイクライン抽出")
root.geometry("700x600")

# 座標のグローバル変数
point = []
img = np.zeros((10, 10, 3), np.uint8)

# 画像パスラベル
inpathLbl = tk.Label(text=u"入力画像のパス：")
inpathLbl.place(x=80, y=55)

# パスエントリー
editBox = tk.Entry(width=50)
editBox.place(x=190, y=50)

# 画像選択ボタン
imgSelectBtn = tk.Button(text=u"画像選択")
imgSelectBtn.bind("<Button-1>", selectFilePath)
imgSelectBtn.place(x=220, y=100)

# 座標選択ボタン
imgShowBtn = tk.Button(text=u"座標選択")
imgShowBtn.bind("<Button-1>", imgShow)
imgShowBtn.place(x=400, y=100)


ShowBtn = tk.Button(text=u"座標表示")
ShowBtn.bind("<Button-1>", triming)
ShowBtn.place(x=400, y=150)



root.mainloop()
