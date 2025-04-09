import os

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.log_file = '필수과정1/문제6/mars_base_log2.txt'

    def get_random_number(self, min_value, max_value):
        rand_bytes = os.urandom(4)
        rand_int = int.from_bytes(rand_bytes)
        return min_value + (rand_int % (max_value - min_value + 1))

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = self.get_random_number(18, 30)
        self.env_values['mars_base_external_temperature'] = self.get_random_number(0, 21)
        self.env_values['mars_base_internal_humidity'] = self.get_random_number(50, 60)
        self.env_values['mars_base_external_illuminance'] = self.get_random_number(500, 715)
        self.env_values['mars_base_internal_co2'] = self.get_random_number(2, 10) / 100
        self.env_values['mars_base_internal_oxygen'] = self.get_random_number(4, 7)

    def get_kst(self):
        os.system('powershell -Command "Get-Date -Format \'yyyy-MM-dd HH:mm:ss\'" > 필수과정1/문제6/date.txt')
        #os.system('date "+%Y-%m-%d %H:%M:%S" > 필수과정1/문제6/date.txt') ## 리눅스 환경에서 사용
        with open('필수과정1/문제6/date.txt', 'r', encoding='utf-8') as file:
            return file.read().strip()

    def get_env(self):
        time_string = self.get_kst()
        env_data = self.env_values

        log_message = f'{time_string},{env_data["mars_base_internal_temperature"]},{env_data["mars_base_external_temperature"]},' \
                      f'{env_data["mars_base_internal_humidity"]},{env_data["mars_base_external_illuminance"]},' \
                      f'{env_data["mars_base_internal_co2"]},{env_data["mars_base_internal_oxygen"]}\n'

        file_exists = os.path.exists(self.log_file)

        with open(self.log_file, 'a', encoding='utf-8') as log_file:
            if not file_exists:
                log_file.write('timestamp,internal_temperature,external_temperature,internal_humidity,external_illuminance,internal_co2,internal_oxygen\n')
            log_file.write(log_message)

        print('로그 메시지 기록됨:')
        print(log_message.strip())

        return self.env_values

if __name__ == '__main__':
    ds = DummySensor()
    print('set_env 실행')
    ds.set_env()
    print('get_env 실행')
    ds.get_env()