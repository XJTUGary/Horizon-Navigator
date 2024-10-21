# pip install opencv-python numpy
import cv2
import numpy as np
from tello import Tello

# 初始化 Tello
drone = Tello()
drone.connect()
drone.streamon()

while True:
    frame = drone.get_frame_read().frame
    # 转换为 HSV 色彩空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定义红色的 HSV 范围（调整范围以适应你的需求） 根据实际颜色调整
    lower_red = np.array([160, 100, 100])
    upper_red = np.array([180, 255, 255])

    # 创建掩膜
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # 进行形态学操作，去除噪声
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # 找到最大的轮廓
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)

        # 在原图上画出轮廓
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)

        # 根据位置控制无人机
        # 计算无人机需要移动的方向
        # 这里的 x 和 y 需要转换为无人机的移动指令
        if radius > 10:  # 检测到圆环
            if x < frame.shape[1] // 3:  # 圆环在左边
                drone.move_left(20)
            elif x > frame.shape[1] * 2 // 3:  # 圆环在右边
                drone.move_right(20)
            else:  # 圆环在中间
                drone.move_forward(20)

            # 向前移动穿过圆环
            drone.move_forward(20)

    # 显示处理后的图像
    cv2.imshow("Frame", frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 着陆
drone.land()
cv2.destroyAllWindows()
