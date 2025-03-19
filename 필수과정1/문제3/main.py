# main.py

list_file_path = '필수과정1/문제3/Mars_Base_Inventory_List.csv'
lines = []

try:
    with open(list_file_path, 'r', encoding='utf-8') as file:
        header = file.readline().strip()
        while True:
            line = file.readline().strip()
            if not line:
                break
            lines.append(line)
except FileNotFoundError:
    print(f'파일 {list_file_path} 찾을 수 없습니다.')
    raise SystemExit
except Exception as e:
    print(f'기타 오류 발생: {e}')
    raise SystemExit

lines.sort(key=lambda x: float(x.split(',')[4]), reverse=True)

output_list = []
for a in lines:
    f = float(a.split(',')[4])
    if f >= 0.7:
        output_list.append(a)
        print(a)
output_danger_file_path = '필수과정1/문제3/Mars_Base_Inventory_danger.csv'
try:
    with open(output_danger_file_path, 'w', encoding='utf-8') as file:
        file.write(f'{header}\n')
        for a in output_list:
            file.write(f'{a}\n')
    print(f'{output_danger_file_path} 파일이 성공적으로 생성되었습니다.')
except Exception as e:
    print(f'파일 {output_danger_file_path}생성 중 오류 발생: {e}')
    raise SystemExit


output_file_path = '필수과정1/문제3/Mars_Base_Inventory_List.bin'
try:
    with open(output_file_path, 'wb') as bin_file:
        bin_file.write(header.encode() + b'\n')
        for b in lines:
            bin_file.write(b.encode() + b'\n')
    print(f'{output_file_path} 파일이 성공적으로 생성되었습니다.')
except Exception as e:
    print(f'파일 {output_file_path}생성 중 오류 발생: {e}')
    raise SystemExit

try:
    with open(output_file_path, 'rb') as bin_file:
        content = bin_file.read()
        decoded_content = content.decode('utf-8')
        print('이진 파일 내용:')
        print(decoded_content)
except FileNotFoundError:
    print(f'파일 {output_file_path} 찾을 수 없습니다.')
    raise SystemExit
except Exception as e:
    print(f'기타 오류 발생: {e}')
    raise SystemExit
