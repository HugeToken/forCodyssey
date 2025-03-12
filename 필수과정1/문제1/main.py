# main.py

print('hello Mars')
log_file_path = '필수과정1/문제1/mission_computer_main.log'

try:
    with open(log_file_path, 'r', encoding='utf-8') as file:
        log = file.readlines()
        print(''.join(log))
except FileNotFoundError:
    print(f'파일 {log_file_path}을(를) 찾을 수 없습니다.')
    raise SystemExit
except Exception as e:
    print(f'기타 오류 발생: {e}')
    raise SystemExit

output_file_path = '필수과정1/문제1/log_analysis.md'

try:
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write('# 사고 원인 분석\n\n') 
        output_file.write('## 산소 탱크 불안정 후 폭발로 인한 시스템 다운\n\n') 
        output_file.write('### 사고 발생 시간\n\n')
        output_file.write('2023-08-27 11:35:00,INFO,Oxygen tank unstable.   \n')
        output_file.write('2023-08-27 11:40:00,INFO,Oxygen tank explosion.   \n')
        output_file.write('2023-08-27 12:00:00,INFO,Center and mission control systems powered down.   \n')

    print(f'{output_file_path} 파일이 성공적으로 생성되었습니다.')
except Exception as e:
    print(f'파일 {output_file_path}을(를) 생성하는 데 오류 발생: {e}')
    raise SystemExit

#보너스 과제
reversed_log = log[1:][::-1]
reversed_log = log[0] + ''.join(reversed_log)
print('시간의 역순으로 정렬된 로그: ')
print(reversed_log)

output_file_path2 = '필수과정1/문제1/problematic_part.txt'

try:
    with open(output_file_path2, 'w', encoding='utf-8') as output_file:
        output_file.write('2023-08-27 11:35:00,INFO,Oxygen tank unstable.\n')
        output_file.write('2023-08-27 11:40:00,INFO,Oxygen tank explosion.')
    print(f'{output_file_path2} 파일이 성공적으로 생성되었습니다.')
except Exception as e:
    print(f'파일 {output_file_path2}을(를) 생성하는 데 오류 발생: {e}')
    raise SystemExit
