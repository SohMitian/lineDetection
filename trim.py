import cv2
import numpy as np
import lineDetect as ld

# class trimmer:

# 中点Mを求める
def calPointM(startPoint, endPoint):
    midPoint = []
    x = (startPoint[0] + endPoint[0]) / 2
    y = (startPoint[1] + endPoint[1]) / 2
    midPoint += [int(x), int(y)]

    return midPoint

# Mを原点とした角度を計算
def calAngle(midPoint, endPoint):
    # 角度（単位：ラジアン）
    rad = np.arctan2(endPoint[1] - midPoint[1], endPoint[0] - midPoint[0])

    return rad

# Mを原点とした回転
def rotationImg(img, midPoint, rad):

    # 画像サイズ
    size = (img.shape[1],img.shape[0])
    # 回転行列の算出
    rotationMat = cv2.getRotationMatrix2D(tuple(midPoint), np.degrees(rad), 1)
    # アフィン変換
    img_rot = cv2.warpAffine(img, rotationMat,
                             size, flags=cv2.INTER_CUBIC)

    return img_rot

# エッジの回転後座標
def rotationPoint(originPoint, rad, point):
    rotedPoint = []

    # 原点を中点に移動
    x = point[0] - originPoint[0]
    y = point[1] - originPoint[1]

    rad = 45
    # 回転
    x = x * np.cos(np.radians(rad)) - y * np.sin(np.radians(rad))
    y = x * np.sin(np.radians(rad)) + y * np.cos(np.radians(rad))

    # 原点をもとに戻す
    x = x + originPoint[0]
    y = y + originPoint[1]

    rotedPoint += [int(np.round(x)), int(np.round(y))]

    return rotedPoint

# トリミング
def triming(img, p1, p2):
    x = (p1[0], p1[1])
    y = (p2[0], p2[1])
    # 原点
    x, y = p1[0], p1[1]-50
    # 高さ、幅
    w, h = abs(p1[0] - p2[0]), abs(p1[1] - p2[1]) + 100

    # 入力画像から窓画像を切り取り
    dst = img[y:y + h, x:x + w]

    return dst

def main(srcPath, point):
    img = cv2.imread(srcPath)
    # エッジ座標をlistに変換
    startPoint = []
    endPoint = []
    startPoint += [point[0][0], point[0][1]]
    endPoint += [point[1][0], point[1][1]]

    cv2.line(img, point[0], point[1], (0, 0, 255), 5)

    # 中点を計算
    midPoint = calPointM(startPoint, endPoint)
    # 角度を計算
    rad = calAngle(midPoint, endPoint)
    # 回転した画像を生成
    img_rot = rotationImg(img, midPoint, rad)

    #回転後のエッジ座標を計算（タプル）
    startPoint = tuple(rotationPoint(midPoint, rad, startPoint))
    endPoint = tuple(rotationPoint(midPoint, rad, endPoint))

    cv2.line(img_rot, startPoint, endPoint, (255, 0, 0), 5)

    # エッジに幅をもたせてトリミング
    img_trim = triming(img_rot, startPoint, endPoint)

    cv2.imshow("img", img_rot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img_trim
    # rot_p1 = rotationPoint(midPoint, rad, startPoint)
    # rot_p2 = rotationPoint(midPoint, rad, endPoint)

    # cv2.line(img_rot, startPoint, endPoint, (0, 0, 255), 3)
    # cv2.circle(img_rot, midPoint, 3, (0, 255, 0), 3)
    # cv2.line(img_rot, rot_p1, rot_p2, (255, 0, 0), 3)

    # cv2.imshow("img_rot", img_rot)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    point = (4983, 919),(4833, 2719)
    img = main("2.jpg", point)

