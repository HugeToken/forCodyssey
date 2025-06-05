import os
import wave
import pyaudio

records_folder = "forCodyssey/필수과정2/문제7/records"
if not os.path.exists(records_folder):
    os.makedirs(records_folder)

def get_current_time():
    current_time = os.popen('powershell -Command "Get-Date -Format \'yyyyMMdd-HHmmss\'"').read().strip()
    return current_time

def check_microphone():
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:
            print("유효한 마이크가 연결되어 있습니다.")
            p.terminate()
            return True
    print("유효한 마이크가 연결되지 않았습니다.")
    return False

def record_audio():
    if not check_microphone():
        return

    chunk = 1024
    format = pyaudio.paInt16
    channels = 1  # 모노
    rate = 44100
    duration = 5 
    p = pyaudio.PyAudio()

    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    
    print("녹음을 시작합니다.")
    
    frames = []
    for _ in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("녹음이 완료되었습니다.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()

    current_time = get_current_time()
    filename = f"{current_time}.wav"

    filepath = os.path.join(records_folder, filename)

    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    
    print(f"파일이 저장되었습니다: {filepath}")

def list_recordings(start_date, end_date):
    try:
        if start_date > end_date:
            raise ValueError("시작 날짜가 종료 날짜보다 뒤에 올 수 없습니다.")
        
        files = os.listdir(records_folder)
        files = [file for file in files if file.endswith('.wav')]

        filtered_files = []

        for file in files:
            file_date_str = file.split('.')[0]
            date_str, _ = file_date_str.split('-')
            if (date_str >= start_date.replace("-", "")) and (date_str <= end_date.replace("-", "")):
                filtered_files.append(file)

        if filtered_files:
            print(f"특정 날짜 범위: {start_date} ~ {end_date}")
            print("녹음 파일 목록:")
            for file in filtered_files:
                print(file)
        else:
            print(f"해당 범위 ({start_date} ~ {end_date})에 녹음 파일이 없습니다.")
    
    except ValueError as e:
        print(f"입력 오류: {e}")

if __name__ == "__main__":
    record_audio()
    list_recordings("2025-05-01", "2025-05-31")