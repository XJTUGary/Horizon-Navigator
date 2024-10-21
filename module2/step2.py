from djitellopy import Tello
import yaml
from time import sleep
def process_movements(tello,param):
    with open('module2/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    step2_config = config.get(param, {})
    for distance, direction in step2_config.items():
        if direction == "rotate":
            print("direction is :" + direction + "  distance: " + distance)
            # tello.rotate_clockwise(distance)
        elif direction == "sleep":
            sleep(distance)
        else:
            tello.move(direction, distance)
            print("direction is :" + direction + "  distance: " + distance)

def flyStep2(tello):
    with open('module2/config.yaml', 'r') as file:
        # config = yaml.safe_load(file)
        # keep live
        # tello.send_keepalive()

        # tello.go_xyz_speed_mid(**config['x']x, y, z, speed, mid)
        #x	int	-500-500	必填
        # y	int	-500-500	必填
        # z	int	-500-500	必填
        # speed	int	10-100	必填
        # tello.go_xyz_speed(**config['go_xyz_speed_mid'])

        # param1:up, down, left, right, forward or back / param2 :20-500 cm
        process_movements(tello,"step2")
        # x
        # int
        # 1 - 360
        # 必填
        # tello.rotate_clockwise(x)

        # print("distance :" + tello.get_distance_tof())
        # curve_xyz_speed(x1, y1, z1, x2, y2, z2, speed)
        # 通过
        # x2
        # y2
        # z2
        # 在曲线中飞到
        # x2
        # y2
        # z2。Speed
        # 定义以
        # cm / s
        # 为单位的行进速度。
        #
        # 这两个点都是相对于当前位置的
        # 当前位置和两个点必须形成圆弧。
        # 如果圆弧半径不在
        # 0.5 - 10
        # 米的范围内，则会引发
        # Exception
        # x1 / x2、y1 / y2、z1 / z2
        # 不能同时介于 - 20 - 20
        # 之间，但都可以为
        # 0。




