# -*- coding: utf-8 -*-

# ライブラリ
import cv2
import numpy as np
import os
import glob
import trim

# ウィンドウ削除
def windowControl():
    # escキーを押すと終了
    k = cv2.waitKey(0)
    if k == 27:
        # ウィンドウ削除
        cv2.destroyAllWindows()

# 古典的ハフ変換
def houghLinesOut(img, edges):
    lines = cv2.HoughLines(edges, 1, np.pi / 180,120)
    for lines in lines[0:5]:

        rho, theta = lines[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        # 直線の角度を求める
        rad = np.arctan2(y2-y1,x2-x1)
        deg = np.degrees(rad)

        # rad = np.arccos(
        #     (x2 - x1) / np.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1))))
        # deg = np.degrees(rad)

        if deg <= 2 and deg >= -2:
            # print("deg", deg)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
    
    # return img


# バイラテラルフィルタの連続適用
def straightBilateral(src, count):
    for _ in range(count):
        # バイラテラルフィルタ(入力画像, 注目画素の領域, 画素値の差による重み, 画素間の距離差による重み)
        src = cv2.bilateralFilter(src, 15, 10, 10)

    return src

# 画像リストの書き出し
def writeList(path, imgNo, img_list):
    for i in range(len(img_list)):
        # 画像の出力ディレクトリを作成
        os.makedirs(path + str(imgNo), exist_ok=True)
        cv2.imwrite(path + str(imgNo) + "/" + str(i) + ".jpg", img_list[i])

def main(src):

    # 画像読み込み
    # img = cv2.imread(src)
    img = src
    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    bi = straightBilateral(gray, 3)

    # 二値化
    # ret, th = cv2.threshold(bi, 0, 255, cv2.THRESH_OTSU)

    # lap = cv2.Laplacian(bi, cv2.CV_8U, ksize=3)

    # Cannyエッジ検出
    edges = cv2.Canny(bi, 50, 100)

    # ハフ変換
    try:
        houghLinesOut(img, edges)
    except TypeError:
        pass

    # img = trim.triming(img,p1, p2)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite("gray.jpg", gray)
    cv2.imwrite("edges.jpg", edges)
    cv2.imwrite("hough.jpg", img)
    # cv2.imwrite("../assets/main/" + str(imgNo) + "/1_gray.jpg", gray)
    # cv2.imwrite("../assets/main/" + str(imgNo) + "/2_bi.jpg", bi)
    # cv2.imwrite("../assets/main/" + str(imgNo) + "/3_lap.jpg", lap)
    # cv2.imwrite("../assets/main/" + str(imgNo) + "/4_th.jpg", th)
    # # cv2.imwrite("../assets/canny/" + str(imgNo) + "/5_canny.jpg", edges)
    # cv2.imwrite("../assets/main/" + str(imgNo) + "/6_result.jpg", img)

    # os.makedirs("../assets/main/result", exist_ok=True)
    # cv2.imwrite("../assets/main/result/" + str(imgNo) + ".jpg", img)


if __name__ == "__main__":
    # src = "../assets/img_in/edges_0.jpg"
    src ="hough.jpg"
    # dogFilter(src)

    # for imgNo in range(1, 3):
    #     src = "../assets/img_in/edges_" + str(imgNo) + ".jpg"
        # src = "/Users/sho/Data/research/assets/img_in/edges_" + str(imgNo) + ".jpg"

    main(src)
