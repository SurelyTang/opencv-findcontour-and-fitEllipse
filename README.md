# opencv-findcontour-and-fitEllipse
数学建模数码相机定位 使用opencv完成轮廓提取与椭圆拟合


环境需要：

pip install opencv-python

pip install numpy


fitEllipse.py:主代码 

对1.jpg提取轮廓并椭圆拟合操作 输出椭圆方程三个参数如下：

centerCoordinates:它是椭圆的中心坐标。坐标表示为两个值的元组，即(X坐标值，Y坐标值)。

axesLength:它包含两个变量的元组，分别包含椭圆的长轴和短轴(长轴长度，短轴长度)。

angle:椭圆旋转角度，以度为单位。



1.jpg:fitEllipse.py识别的图片


放缩旋转置换.py:数字图像处理学习矩阵时我实践用的代码，顺便贴的,配套的是 旋转矩阵过程示意.png 

