from djitellopy import Tello
import time
# pip install pyyaml
import yaml

# 读取配置文件
with open("config.yml", 'r') as file:
    config = yaml.safe_load(file)

# 初始化无人机
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")

# 起飞
tello.takeoff()
time.sleep(2)

# 穿过圆环的函数
def fly_through_rings(rings):
    for ring in rings:
        tello.move_up(ring['height'])  # 上升到指定高度
        tello.rotate_clockwise(ring['rotation'])  # 旋转到指定角度
        tello.move_forward(ring['distance'])  # 向前飞行
        time.sleep(2)

# 从配置中读取圆环参数
fly_through_rings(config['rings'])

# 着陆
tello.land()
