import yaml

def move(direction, distance):
    print(f"Moving {direction} for {distance} units.")

def process_movements(step2_config):
    # with open('config.yaml', 'r') as file:
    #     config = yaml.safe_load(file)
    #
    # step2_config = config.get('step2', {})
    for direction, distance in step2_config.items():
        move(direction, distance)

if __name__ == '__main__':
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        process_movements(**config['step2'])