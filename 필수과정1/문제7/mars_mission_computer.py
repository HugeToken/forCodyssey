#mars_mission_computer.py

import time
import mars_mission_computer2 as mmc2

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.history = []

    def get_sensor_data(self, sensor):
        sensor.set_env()
        self.env_values = sensor.get_env()
        self.history.append(self.env_values.copy())

        json_str = '{' + ','.join(f'"{key}":{value}' for key, value in self.env_values.items()) + '}'
        print(json_str)

    def calculate_five_minute_avg(self):
        if len(self.history) == 60:
            avg_values = {key: sum(d[key] for d in self.history) / len(self.history) for key in self.env_values}
            json_avg_str = '{' + ','.join(f'"{key}":{value}' for key, value in avg_values.items()) + '}'
            print('5분 평균:', json_avg_str)
            self.history.clear()

    def run(self, sensor):
        count = 0
        try:
            while True:
                self.get_sensor_data(sensor)
                count += 1
                if count % 60 == 0:
                    self.calculate_five_minute_avg()
                time.sleep(5)
        except KeyboardInterrupt:
            print('System stopped...')
            raise SystemExit


ds = mmc2.DummySensor()
RunComputer = MissionComputer()
RunComputer.run(ds)
