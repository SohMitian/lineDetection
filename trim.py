import cv2
import numpy as np
import lineDetect as ld

# class trimmer:

# 中点Mを求める
def calPointM(startPoint: list, endPoint: list) -> list:
    midPoint = []
    x = (startPoint[0] + endPoint[0]) / 2
    y = (startPoint[1] + endPoint[1]) / 2
    midPoint += [int(x), int(y)]

    return midPoint

# Mを原点とした角度を計算
def calAngle(midPoint: list, endPoint: list) -> float:
    # 角度（単位：ラジアン）
    rad = np.arctan2(endPoint[1] - midPoint[1], endPoint[0] - midPoint[0])

    return rad

# Mを原点とした回転
def rotationImg(img: np.ndarray, midPoint: list, rad: float) -> np.ndarray:

    # 画像サイズ
    size = (img.shape[1],img.shape[0])
    # 回転行列の算出
    rotationMat = cv2.getRotationMatrix2D(tuple(midPoint), np.degrees(rad), 1)
    # アフィン変換
    img_rot = cv2.warpAffine(img, rotationMat,
                             size, flags=cv2.INTER_CUBIC)

    return img_rot

# エッジの回転後座標
def rotationPoint(originPoint: list, rad: float, point: list) -> list:
    rotatedPoint = []

    # 原点を中点に移動
    x = point[0] - originPoint[0]
    y = point[1] - originPoint[1]

    # 引数はラジアン
    cos = np.cos(-rad)
    sin = np.sin(-rad)
    # 回転
    x_dash = (x * cos) - (y * sin)
    y_dash = (x * sin) + (y * cos)


    # 原点をもとに戻す
    x_dash = x_dash + originPoint[0]
    y_dash = y_dash + originPoint[1]

    rotatedPoint += [int(np.round(x_dash)), int(np.round(y_dash))]

    return rotatedPoint

# トリミング
def triming(img: np.ndarray, stP: list, endP: list):

    # ListのtopIndexを省く処理
    startP = [stP[0][0], stP[0][1]]
    endP = [endP[0][0], endP[0][1]]

    # 原点
    # xに始点のX座標を yに始点のY座標
    x, y = startP[0], startP[1]

    # 幅と高さ
    # 幅：始点x - 終点x
    # 高さ：始点y - 終点y
    w, h = abs(startP[0] - endP[0]), abs(startP[1] - endP[1]) +100

    # 入力画像から窓画像を切り取り
    dst = img[y:y + h, x:x + w]

    return dst

def main(srcPath: str, point: list) -> np.ndarray:
    img = cv2.imread(srcPath)

    # 中点を計算
    midPoint = calPointM(point[0], point[1])
    # 角度を計算
    rad = calAngle(midPoint, point[1])
    # 回転した画像を生成
    img_rot = rotationImg(img, midPoint, rad)
    # cv2.line(img_rot, tuple(point[0]),tuple(point[1]), (0, 0, 255), 5)

    #回転後のエッジ座標を計算（list）
    rotatedStartPoint = [rotationPoint(midPoint, rad, point[0])]
    rotatedEndPoint = [rotationPoint(midPoint, rad, point[1])]

# # 線の描画
# cv2.line(img_rot, tuple(rotatedStartPoint[0]),
#          tuple(rotatedEndPoint[0]), (0, 0, 255), 5)
# # 始点
# cv2.circle(img_rot, tuple(rotatedStartPoint[0]), 10, (255, 0, 0), -1)
# # 終点
# cv2.circle(img_rot, tuple(rotatedEndPoint[0]), 10, (0, 255, 0), -1)

    # エッジに幅をもたせてトリミング
    img_trim = triming(img_rot, rotatedStartPoint, rotatedEndPoint)

    return img_trim


if __name__ == "__main__":
    point = (1900, 521),(1804, 2045)
    img = main("1/2.jpg", point)
    cv2.imwrite("result/2.jpg", img)
