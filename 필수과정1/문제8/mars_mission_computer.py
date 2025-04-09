import time
import os
import platform
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
        self.history = []  # 5분 평균 저장용
        self.setting = self.load_setting()

    def load_setting(self):
        setting = {
            'os_name': 1,
            'os_version': 1,
            'cpu_type': 1,
            'core_count': 1,
            'memory_mb': 1,
            'cpu_load_percent': 1,
            'memory_load_percent': 1
        }
        try:
            with open('필수과정1/문제8/setting.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(':')
                    if len(parts) == 2 and parts[1].strip() in ['0', '1']:
                        setting[parts[0].strip()] = int(parts[1].strip())
        except:
            pass
        return setting

    def get_sensor_data(self, sensor):
        sensor.set_env()
        self.env_values = sensor.get_env()
        self.history.append(self.env_values.copy())  # 값 저장

        json_str = '{'
        json_str += '"mars_base_internal_temperature":' + str(self.env_values['mars_base_internal_temperature']) + ','
        json_str += '"mars_base_external_temperature":' + str(self.env_values['mars_base_external_temperature']) + ','
        json_str += '"mars_base_internal_humidity":' + str(self.env_values['mars_base_internal_humidity']) + ','
        json_str += '"mars_base_external_illuminance":' + str(self.env_values['mars_base_external_illuminance']) + ','
        json_str += '"mars_base_internal_co2":' + str(self.env_values['mars_base_internal_co2']) + ','
        json_str += '"mars_base_internal_oxygen":' + str(self.env_values['mars_base_internal_oxygen'])
        json_str += '}'
        print(json_str)

    def calculate_five_minute_avg(self):
        if len(self.history) == 60:
            avg_values = {key: sum(d[key] for d in self.history) / len(self.history) for key in self.env_values}

            json_avg_str = '{'
            json_avg_str += '"mars_base_internal_temperature":' + str(avg_values['mars_base_internal_temperature']) + ','
            json_avg_str += '"mars_base_external_temperature":' + str(avg_values['mars_base_external_temperature']) + ','
            json_avg_str += '"mars_base_internal_humidity":' + str(avg_values['mars_base_internal_humidity']) + ','
            json_avg_str += '"mars_base_external_illuminance":' + str(avg_values['mars_base_external_illuminance']) + ','
            json_avg_str += '"mars_base_internal_co2":' + str(avg_values['mars_base_internal_co2']) + ','
            json_avg_str += '"mars_base_internal_oxygen":' + str(avg_values['mars_base_internal_oxygen'])
            json_avg_str += '}'

            print('5분 평균:', json_avg_str)
            self.history.clear()

    def get_mission_computer_info(self):
        try:
            os_name = platform.system()
            os_version = platform.version()
            cpu_type = platform.processor()
            core_count = os.cpu_count()
            mem_size = 0

            if os_name == 'Windows':
                mem_info = os.popen('wmic ComputerSystem get TotalPhysicalMemory').read().strip().split('\n')
                if len(mem_info) > 1 and mem_info[1].strip().isdigit():
                    mem_size = int(mem_info[1].strip()) // (1024 * 1024)
            elif os_name in ['Linux', 'Darwin']:
                mem_info = os.popen('grep MemTotal /proc/meminfo').read().strip()
                if mem_info:
                    mem_size = int(mem_info.split()[1]) // 1024

            info = {}
            if self.setting.get('os_name'): info['os_name'] = os_name
            if self.setting.get('os_version'): info['os_version'] = os_version
            if self.setting.get('cpu_type'): info['cpu_type'] = cpu_type
            if self.setting.get('core_count'): info['core_count'] = core_count
            if self.setting.get('memory_mb'): info['memory_mb'] = mem_size

            print(str(info).replace("'", '"'))
        except:
            print('{"error": "시스템 정보를 가져올 수 없습니다."}')

    def get_mission_computer_load(self):
        try:
            os_name = platform.system()
            cpu_load = 0
            mem_load = 0

            if os_name == 'Windows':
                cpu_out = os.popen('wmic cpu get loadpercentage /value').read().strip()
                for line in cpu_out.split('\n'):
                    if 'LoadPercentage' in line:
                        _, val = line.split('=')
                        if val.strip().isdigit():
                            cpu_load = int(val.strip())

                mem_data = os.popen('wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value').read().strip().split('\n')
                mem_info = {}
                for line in mem_data:
                    if '=' in line:
                        k, v = line.strip().split('=')
                        mem_info[k] = int(v)
                if 'FreePhysicalMemory' in mem_info and 'TotalVisibleMemorySize' in mem_info:
                    mem_load = 100 - (mem_info['FreePhysicalMemory'] * 100 // mem_info['TotalVisibleMemorySize'])

            elif os_name in ['Linux', 'Darwin']:
                cpu_line = os.popen("top -bn1 | grep 'Cpu(s)'").read().strip()
                if cpu_line:
                    parts = cpu_line.split(',')
                    idle = [p for p in parts if 'id' in p]
                    if idle:
                        idle_val = float(idle[0].strip().split()[0])
                        cpu_load = int(100 - idle_val)
                mem_info = os.popen('free -m').readlines()
                if len(mem_info) > 1:
                    mem_line = mem_info[1].split()
                    if len(mem_line) >= 3:
                        total_mem = int(mem_line[1])
                        used_mem = int(mem_line[2])
                        mem_load = used_mem * 100 // total_mem

            load_info = {}
            if self.setting.get('cpu_load_percent'): load_info['cpu_load_percent'] = int(cpu_load)
            if self.setting.get('memory_load_percent'): load_info['memory_load_percent'] = int(mem_load)

            print(str(load_info).replace("'", '"'))
        except:
            print('{"error": "시스템 부하 정보를 가져올 수 없습니다."}')

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

runComputer = MissionComputer()

runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()
