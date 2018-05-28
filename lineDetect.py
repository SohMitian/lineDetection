# ライブラリ
import cv2
import numpy as np

# 画像のエッジ検出関数
def imageEdgeDetect(src):
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
    lines = cv2.HoughLines(opening, 1, np.pi / 180, 200)
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
    # print(lines[0][0][0])
    # ウィンドウ生成＆表示
    cv2.namedWindow("img", cv2.WINDOW_GUI_EXPANDED)
    cv2.namedWindow("lsd", cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow("img", img)
    cv2.imshow("lsd", img)

    # escキーを押すと終了
    k = cv2.waitKey(0)
    if k == 27:
        # ウィンドウ削除
        cv2.destroyAllWindows()

# ビデオキャプチャのエッジ検出関数
def videoEdgeDetect():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        # グレースケール化
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # バイラテラルフィルタでエッジを残して平滑化
        bilateral = cv2.bilateralFilter(gray, 15, 75, 75)
        # LSDでエッジ検出
        lsd = cv2.createLineSegmentDetector()
        lines = lsd.detect(bilateral)[0]
        drawn_img = lsd.drawSegments(bilateral, lines)

        try:
            # ウィンドウ生成＆表示
            cv2.namedWindow("lsd", cv2.WINDOW_GUI_EXPANDED)
            cv2.imshow("lsd", drawn_img)
        except TypeError:
            print("error")

        # escキーを押すと終了
        k = cv2.waitKey(5)
        if k == 27:
            break

    # ウィンドウ削除
    cv2.destroyAllWindows()
    cap.release()


def canny(src):
    # 画像読み込み
    img = cv2.imread(src)
    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # canny
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img, (x1, y1), (x2, y2),(0,0,255),2)

    # ウィンドウ生成＆表示
    cv2.namedWindow("img", cv2.WINDOW_GUI_EXPANDED)
    cv2.namedWindow("lsd", cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow("img", img)
    cv2.imshow("lsd", edges)

    # escキーを押すと終了
    k = cv2.waitKey(0)
    if k == 27:
        # ウィンドウ削除
        cv2.destroyAllWindows()


if __name__ == "__main__":
    src = "img_in/5.jpg"
    imageEdgeDetect(src)

