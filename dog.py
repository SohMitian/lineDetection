#ライブラリ
import cv2
import numpy as np
import os
import glob

# function
# gausianのリストを作成
def listOfGaus(ORIGIN, xy=3, sigma=0):
    gaus_list = []
    for i in range(3, 10, 2):
        gaus_list.append(cv2.GaussianBlur(ORIGIN, (xy, xy), sigma+i))
    return gaus_list

# Cannyのリストを作成
def listOfCanny(gaus_list, min, max):
    canny_list = []
    for gaus_img in gaus_list:
        canny_list.append(cv2.Canny(gaus_img, min, max))
    return canny_list

# 差分のリストを作成
def listOfDiff(canny_list):
    diff_list = []
    for i in range(len(canny_list)-1):
        diff_list.append(cv2.absdiff(canny_list[i + 1], canny_list[i]))
    return diff_list

# 画像リストの書き出し
def writeImgOfList(imgName, img_list):
    for i in range(len(img_list)):
        cv2.imwrite("img_out/" + str(dataNo) + "/" + imgName + str(i) + ".jpg", img_list[i])


# main
# img_in内の画像数を取得
files = glob.glob("img_in/*")
# 画像の枚数分処理
for dataNo in range(1, len(files)+1):
    # 元画像
    dataName = str(dataNo) + ".jpg"
    inPath = ("img_in/" + dataName)
    ORIGIN = cv2.imread(inPath, 0)

    # ガウシアンフィルタを掛けた画像リストを作成
    gaus_list = listOfGaus(ORIGIN)

    # Cannyを掛けた画像リストを作成
    canny_list = listOfCanny(gaus_list, 10, 50)

    # Cannyの差分を取った画像リストを作成
    diff_list = listOfDiff(canny_list)

    # 画像の出力ディレクトリを作成
    os.makedirs("img_out/" + str(dataNo), exist_ok = True)

    # 各画像の出力
    writeImgOfList("gaus", gaus_list)
    writeImgOfList("canny", canny_list)
    writeImgOfList("diff", diff_list)
