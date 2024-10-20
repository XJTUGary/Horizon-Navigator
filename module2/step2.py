from djitellopy import Tello
import yaml
def process_movements(tello,param):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    step2_config = config.get(param, {})
    for direction, distance in step2_config.items():
        if direction == "rotate":
            tello.rotate_clockwise(distance)
        else:
            tello.move(direction, distance)
        print("the height is :" + tello.get_height())

def flyStep2(tello):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        # keep live
        tello.send_keepalive()

        # tello.go_xyz_speed_mid(**config['x']x, y, z, speed, mid)
        #x	int	-500-500	必填
        # y	int	-500-500	必填
        # z	int	-500-500	必填
        # speed	int	10-100	必填
        tello.go_xyz_speed(**config['go_xyz_speed_mid'])

        # param1:up, down, left, right, forward or back / param2 :20-500 cm
        process_movements(tello,"step2")
        # x
        # int
        # 1 - 360
        # 必填
        # tello.rotate_clockwise(x)

        print("distance :" + tello.get_distance_tof())




