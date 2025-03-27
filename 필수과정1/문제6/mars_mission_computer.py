import requests

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

    def get_random_number(self, min_value, max_value):
        url = 'https://www.random.org/integers/'

        hds = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        params = {'num': 1, 'min': min_value, 'max': max_value, 'col': 1, 'base': 10, 'format': 'plain'}

        max_retries = 20
        retries = 0
        
        while retries < max_retries:
            try:
                response = requests.get(url, params=params, headers=hds)
                response.raise_for_status()
                return int(response.text.strip())
            except requests.exceptions.RequestException as e:
                retries += 1
                if retries == max_retries:
                    return None

    def set_env(self):
        temp_internal = self.get_random_number(18, 30)
        temp_external = self.get_random_number(0, 21)
        humidity = self.get_random_number(50, 60)
        illuminance = self.get_random_number(500, 715)
        co2 = self.get_random_number(2, 10)
        oxygen = self.get_random_number(4, 7)

        self.env_values['mars_base_internal_temperature'] = temp_internal if temp_internal is not None else 20
        self.env_values['mars_base_external_temperature'] = temp_external if temp_external is not None else 10
        self.env_values['mars_base_internal_humidity'] = humidity if humidity is not None else 55
        self.env_values['mars_base_external_illuminance'] = illuminance if illuminance is not None else 600
        self.env_values['mars_base_internal_co2'] = (co2 if co2 is not None else 2) / 100
        self.env_values['mars_base_internal_oxygen'] = oxygen if oxygen is not None else 5

    def get_kst(self):
        url = 'http://timeapi.io/api/Time/current/zone?timeZone=Asia/Seoul'
        hds = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        max_retries = 20
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(url, headers=hds)
                response.raise_for_status()
                data = response.json()
                return data['dateTime']
            except requests.exceptions.RequestException as e:
                retries += 1
                if retries == max_retries:
                    return None

    def get_env(self):
        time_string = self.get_kst()
        env_data = self.env_values
        if time_string:
            log_message = f'{time_string},internal_temperature:{env_data["mars_base_internal_temperature"]},external_temperature:{env_data["mars_base_external_temperature"]},' \
                          f'internal_humidity:{env_data["mars_base_internal_humidity"]},external_illuminance:{env_data["mars_base_external_illuminance"]},' \
                          f'internal_co2:{env_data["mars_base_internal_co2"]},internal_oxygen:{env_data["mars_base_internal_oxygen"]}\n'

            with open('필수과정1/문제6/mars_base_log.txt', 'a') as log_file:
                log_file.write(log_message)
            print('로그 메시지')
            print(log_message)
        return self.env_values


# 테스트
ds = DummySensor()
print('setenv')
print(ds.set_env())
print('getenv')
print(ds.get_env())
