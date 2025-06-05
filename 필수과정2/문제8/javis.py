import os
import wave
import pyaudio
import speech_recognition as sr
import csv
import time

records_folder = "forCodyssey/필수과정2/문제8/records"
if not os.path.exists(records_folder):
    os.makedirs(records_folder)

def get_current_time():
    return time.strftime("%Y%m%d-%H%M%S", time.localtime())

def check_microphone():
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:
            return True
    return False

def record_audio():
    if not check_microphone():
        return None, None

    chunk = 1024
    format = pyaudio.paInt16
    channels = 1  
    rate = 44100
    duration = 5 
    p = pyaudio.PyAudio()

    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    
    frames = []
    start_time = time.time()
    for _ in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

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

    return filename, start_time

def convert_audio_to_text(audio_file, start_time):
    audio_path = os.path.join(records_folder, audio_file)
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)  
    
    try:
        text = recognizer.recognize_google(audio, language="ko-KR")
        transcription = process_transcription_with_time(text, start_time)
        return transcription
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return None

def process_transcription_with_time(text, start_time):
    current_time = time.time() - start_time
    time_str = str(round(current_time, 2))
    return time_str, text.strip()

def save_transcription_to_csv(audio_file, transcription, full_text):
    csv_file = os.path.splitext(audio_file)[0] + ".csv"
    csv_path = os.path.join(records_folder, csv_file)

    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([full_text])
        writer.writerow(['시간', '인식된 텍스트'])
        writer.writerows([transcription])

def search_in_text(keyword, text):
    if keyword.lower() in text.lower():
        return True
    return False

def main():
    audio_file, start_time = record_audio()
    if audio_file:
        transcription = convert_audio_to_text(audio_file, start_time)

        if transcription:
            full_text = transcription[1]
            print(f"녹음한 텍스트: {full_text}")

        save_transcription_to_csv(audio_file, [transcription], full_text)

        while True:
            search_keyword = input("검색할 키워드를 입력하세요: ")
            if search_in_text(search_keyword, full_text):
                print(f"키워드 '{search_keyword}'이/가 텍스트에 포함되어있습니다.\n")
            else:
                print(f"키워드 '{search_keyword}'은/는 텍스트에 포함되어있지 않습니다.\n")
            
            again = input("다시 검색하시겠습니까? (예/아니오): ")
            if again == "아니오":
                print("프로그램을 종료합니다.")
                break
            elif again != "예":
                print("잘못된 입력입니다. '예' 또는 '아니오'를 입력해 주세요.")

if __name__ == "__main__":
    main()
