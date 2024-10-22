# coding=utf-8
from djitellopy import Tello
import time
import yaml



def step1(tello, params):
    tello.move_up(params['up'])
    tello.move_forward(params['forward1'])
    tello.rotate_counter_clockwise(90)
    tello.move_forward(params['forward2'])


def step2(tello, params):
    tello.move_forward(params['forward'])
    tello.move_down(params['down'])

    # tello.curve_xyz_speed(params['radius'], 0, 0, 0, params['radius'], 0, params['angle'], params['speed'])
    tello.move_right(params['mid-side'])
    tello.move_forward(params['side'])
    tello.move_left(params['side'])
    tello.move_back(params['side'])
    tello.move_right(params['side'])
    tello.move_forward(params['side'])
    tello.move_left(params['mid-side'])
    tello.move_forward(60)


def step3(tello, params):
    tello.move_forward(params['forward'])
    tello.move_up(params['mid-up'])
    tello.move_forward(params['side'])
    tello.move_down(params['side'])
    tello.move_back(params['side'])
    tello.move_up(params['side'])
    tello.move_forward(params['side'])


def main(config):
    # 初始化无人机
    tello = Tello()
    tello.connect()
    print(f"Battery: {tello.get_battery()}%")
    # 起飞
    tello.takeoff()
    # time.sleep(0.5)
    step1_params = config['step1']
    step1(tello, step1_params)

    step2_params = config['step2']
    step2(tello, step2_params)

    step3_params = config['step3']
    step3(tello, step3_params)



    # 着陆
    tello.land()


if __name__ == "__main__":
    # 读取配置文件
    with open("config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    main(config)
