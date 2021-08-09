import cv2
import numpy as np

img = cv2.imread('1.jpg')
rows, cols, ch = img.shape
# 边缘提取
Ksize = 3
L2g = True
edge = cv2.Canny(img, 50, 100, apertureSize=Ksize, L2gradient=L2g)

# 提取轮廓
'''
findcontour()函数中有三个参数，第一个img是源图像，第二个model是轮廓检索模式，第三个method是轮廓逼近方法。输出等高线contours和层次结构hierarchy。
model:  cv2.RETR_EXTERNAL  仅检索极端的外部轮廓。 为所有轮廓设置了层次hierarchy[i][2] = hierarchy[i][3]=-1
        cv2.RETR_LIST  在不建立任何层次关系的情况下检索所有轮廓。
        cv2.RETR_CCOMP  检索所有轮廓并将其组织为两级层次结构。在顶层，组件具有外部边界；在第二层，有孔的边界。如果所连接零部件的孔内还有其他轮廓，则该轮廓仍将放置在顶层。
        cv2.RETR_TREE  检索所有轮廓，并重建嵌套轮廓的完整层次。
        cv2.RETR_FLOODFILL  输入图像也可以是32位的整型图像(CV_32SC1)
method：cv2.CHAIN_APPROX_NONE  存储所有的轮廓点，任何一个包含一两个点的子序列（不改变顺序索引的连续的）相邻。
        cv2.CHAIN_APPROX_SIMPLE  压缩水平，垂直和对角线段，仅保留其端点。 例如，一个直立的矩形轮廓编码有4个点。
        cv2.CHAIN_APPROX_TC89_L1 和 cv2.CHAIN_APPROX_TC89_KCOS 近似算法
'''
contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 绘制轮廓 第三个参数是轮廓的索引（在绘制单个轮廓时有用。要绘制所有轮廓，请传递-1）
dst = np.ones(img.shape, dtype=np.uint8)
cv2.drawContours(dst, contours, -1, (0, 255, 0), 1)
for i in range(12):
    print(len(contours[i]))
'''
cv2.ellipse(image, centerCoordinates, axesLength, angle, startAngle, endAngle, color [, thickness[, lineType[, shift]]])
image:它是要在其上绘制椭圆的图像。
centerCoordinates:它是椭圆的中心坐标。坐标表示为两个值的元组，即(X坐标值，Y坐标值)。
axesLength:它包含两个变量的元组，分别包含椭圆的长轴和短轴(长轴长度，短轴长度)。
angle:椭圆旋转角度，以度为单位。
startAngle:椭圆弧的起始角度，以度为单位。
endAngle:椭圆弧的终止角度，以度为单位。
color:它是要绘制的形状边界线的颜色。对于BGR，我们通过一个元组。例如：(255，0，0)为蓝色。
thickness:是形状边界线的粗细像素。厚度-1像素将用指定的颜色填充形状。
lineType:这是一个可选参数，它给出了椭圆边界的类型。
shift:这是一个可选参数。它表示中心坐标中的小数位数和轴的值。
'''
cnt = contours[3]
ellipse = cv2.fitEllipse(cnt)
print(ellipse)
cv2.ellipse(dst, ellipse, (0, 0, 255), 2)
cv2.imshow("dst", dst)
cv2.waitKey()

'''
#print(contours)
# 绘制单个轮廓
cnt = contours[3]
cv2.drawContours(dst, [cnt], 0, (0, 0, 255), 1)

# 特征矩
cnt = contours[3]
M = cv2.moments(cnt)
print(M)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
cv2.circle(dst, (cx, cy), 2, (0, 0, 255), -1)   # 绘制圆点

# 轮廓面积
area = cv2.contourArea(cnt)
print(area)

# 轮廓周长：第二个参数指定形状是闭合轮廓(True)还是曲线
perimeter = cv2.arcLength(cnt, True)
print(perimeter)

# 轮廓近似：epsilon是从轮廓到近似轮廓的最大距离--精度参数
epsilon = 0.01 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)
cv2.polylines(dst, [approx], True, (0, 255, 255))   # 绘制多边形
print(approx)

# 轮廓凸包：returnPoints：默认情况下为True。然后返回凸包的坐标。如果为False，则返回与凸包点相对应的轮廓点的索引。
hull = cv2.convexHull(cnt, returnPoints=True)
cv2.polylines(dst, [hull], True, (255, 255, 255), 2)   # 绘制多边形
print(hull)

# 检查凸度：检查曲线是否凸出的功能，返回True还是False。
k = cv2.isContourConvex(cnt)
print(k)

# 边界矩形:最小外接矩形
# 直角矩形
x, y, w, h = cv2.boundingRect(cnt)
cv2.rectangle(dst, (x, y), (x+w, y+h), (255, 255, 0), 2)
# 旋转矩形
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(dst, [box], 0, (0, 0, 255), 2)

# 最小外接圆
(x, y), radius = cv2.minEnclosingCircle(cnt)
center = (int(x), int(y))
radius = int(radius)
cv2.circle(dst, center, radius, (0, 255, 0), 2)

# 拟合椭圆
ellipse = cv2.fitEllipse(cnt)
cv2.ellipse(dst, ellipse, (0, 0, 255), 2)

# 拟合直线
rows, cols = img.shape[:2]
[vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx)+y)
cv2.line(dst, (cols-1, righty), (0, lefty), (255, 255, 255), 2)


cv2.imshow("dst", dst)
cv2.waitKey()'''