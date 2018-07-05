# ライブラリ
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

# ウィンドウ削除


def windowControl():
    # escキーを押すと終了
    k = cv2.waitKey(0)
    if k == 27:
        # ウィンドウ削除
        cv2.destroyAllWindows()

# 古典的ハフ変換


def houghLinesOut(img, edges):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 50)
    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# 確率的ハフ変換


def houghLinesPOut(img, edges):
    minLineLength = 10
    maxLineGap = 20
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100,
                            minLineLength, maxLineGap)
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)


# 精鋭化
def sharpnening(src):
    # カーネルサイズ
    #kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float)
    # 畳み込み
    conv = cv2.filter2D(src, -1, kernel)

    return conv

# lsd


def lsd(src):
    lsd = cv2.createLineSegmentDetector()
    lines = lsd.detect(src)[0]
    draw_line = lsd.drawSegments(src, lines)

    return draw_line

# バイラテラルフィルタの連続適用


def straightBilateral(src, count):
    for i in range(count):
        # バイラテラルフィルタ(入力画像, 注目画素の領域, 画素値の差による重み, 画素間の距離差による重み)
        src = cv2.bilateralFilter(src, 15, 10, 10)

    return src

# gausianのリストを作成


def listOfGaus(count, gray, xy=3, sigma=1):
    gaus_list = []
    for i in range(count):
        gaus_list.append(cv2.GaussianBlur(gray, (xy, xy), sigma + i))
    return gaus_list

# 差分のリストを作成


def listOfDiff(gaus_list):
    diff_list = []
    for i in range(len(gaus_list)):
        if i + 1 >= len(gaus_list):
            print("終了")
        else:
            diff_list.append(gaus_list[i] - gaus_list[i + 1])
    return diff_list

# ハフ変換画像の作成


def listOfHough(img, diff_list):
    for i in range(len(diff_list)):
        try:
            houghLinesOut(img, diff_list[i])
        except TypeError:
            break

    return img

# 画像リストの書き出し


def writeList(path, imgNo, img_list):
    for i in range(len(img_list)):
        # 画像の出力ディレクトリを作成
        os.makedirs(path + str(imgNo), exist_ok=True)
        cv2.imwrite(path + str(imgNo) + "/" + str(i) + ".jpg", img_list[i])

# 画像のエッジ検出関数(LSD+収縮)


def lsdConst(src):
    # 画像読み込み
    img = cv2.imread(src)
    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # バイラテラルフィルタ(入力画像, 注目画素の領域, 画素値の差による重み, 画素間の距離差による重み)
    bilateral = cv2.bilateralFilter(gray, 5, 50, 50)

    # LSDでエッジ検出
    lsd = cv2.createLineSegmentDetector()
    lines = lsd.detect(bilateral)[0]
    drawn_img = lsd.drawSegments(bilateral, lines)

    # 収縮
    kernel = np.ones((8, 8), np.uint8)
    opening = cv2.morphologyEx(bilateral, cv2.MORPH_ERODE, kernel)
    # gray = cv2.cvtColor(drawn_img, cv2.COLOR_RGB2GRAY)

    # 二値化
    ret, thresh = cv2.threshold(opening, 0, 255, cv2.THRESH_OTSU)

    # 収縮
    kernel = np.ones((20, 20), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel)

    # ハフ変換
    houghLinesOut(img, opening)

    # ウィンドウ生成＆表示
    cv2.imshow("img", img)
    cv2.imshow("lsd", img)

    # ウィンドウ操作
    windowControl()


def otsuOnly(src, imgNo):
    # 画像読み込み
    img = cv2.imread(src)

    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # otsuThresh
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ハフ変換
    houghLinesOut(img, th)

    cv2.imwrite("../assets/otsuOnly/otsu/" + str(imgNo) + ".jpg", th)
    cv2.imwrite("../assets/otsuOnly/line/" + str(imgNo) + ".jpg", img)


def dog(src, imgNo):
    houghList = []
    # 画像読み込み
    img = cv2.imread(src)

    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 各リストの作成
    gausList = listOfGaus(10, gray)
    diffList = listOfDiff(gausList)
    houghList.append(listOfHough(img, diffList))

    # 書き出し
    writeList("../assets/dog/gaus/", imgNo, gausList)
    writeList("../assets/dog/diff/", imgNo, diffList)
    writeList("../assets/dog/hough/", imgNo, houghList)


def canny(src, imgNo):
    # 画像読み込み
    img = cv2.imread(src)

    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    bi = straightBilateral(gray, 2)

    # Cannyエッジ検出
    edges = cv2.Canny(bi, 50, 100)

    # ハフ変換
    try:
        houghLinesOut(img, edges)
    except TypeError:
        pass

    cv2.imwrite("../assets/canny/canny/" + str(imgNo) + ".jpg", edges)
    cv2.imwrite("../assets/canny/img/" + str(imgNo) + ".jpg", img)


if __name__ == "__main__":
    # src = "../assets/img_in/17.jpg"
    # dogFilter(src)

    for imgNo in range(11, 20):
        src = "../assets/img_in/" + str(imgNo) + ".jpg"
        canny(src, imgNo)
