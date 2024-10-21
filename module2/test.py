import yaml

def move(direction, distance):
    print(f"Moving {direction} for {distance} units.")

def process_movements(tello,param):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    step2_config = config.get(param, {})
    for distance, direction in step2_config.items():
        if direction == "rotate":
            print("direction is :" + str(direction) + "  distance: " + str(distance))
            # tello.rotate_clockwise(distance)
        else:
            # tello.move(direction, distance)
            print("direction is :" + str(direction) + "  distance: " + str(distance))

if __name__ == '__main__':
    process_movements("", "step2")
    # with open('config.yaml', 'r') as file:
    #     config = yaml.safe_load(file)
    #     process_movements(**config['step2'])