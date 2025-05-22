def caesar_cipher_decode(target_text):
    def shift_char(c, shift):
        if c.isupper():
            return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        elif c.islower():
            return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        else:
            return c

    dictionary = ['asdf']

    print('카이사르 암호 복호화\n')

    found = False
    results = []

    for shift in range(26):
        decrypted = ''.join(shift_char(c, shift) for c in target_text)
        results.append(decrypted)  # 저장
        print(f'{shift}: {decrypted}')
        lower_decrypted = decrypted.lower()

        if any(keyword in lower_decrypted for keyword in dictionary):
            print(f'\n{shift}번째에서 복호화 성공')
            try:
                with open('필수과정2/문제2/result.txt', 'w', encoding='utf-8') as f:
                    f.write(decrypted)
                print('결과를 파일에 저장했습니다.')
            except FileNotFoundError:
                print('경로가 잘못되어 파일을 저장할 수 없습니다.')
            except PermissionError:
                print('파일 저장 권한이 없습니다.')
            except Exception as e:
                print(f'기타 오류 발생: {e}')
            found = True
            break

    if not found:
        print('\n키워드를 포함한 복호화 결과를 찾지 못했습니다.')
        try:
            user_input = input('저장하고 싶은 복호화 결과의 시프트 번호를 입력하세요 (0~25): ')
            shift_num = int(user_input)
            if 0 <= shift_num < 26:
                selected = results[shift_num]
                with open('필수과정2/문제2/result.txt', 'w', encoding='utf-8') as f:
                    f.write(selected)
                print(f'{shift_num}번 결과를 파일에 저장했습니다.')
            else:
                print('0~25 사이의 숫자를 입력해주세요.')
        except ValueError:
            print('유효한 숫자가 아닙니다.')
        except Exception as e:
            print(f'기타 오류 발생: {e}')

if __name__ == '__main__':
    try:
        with open('필수과정2/문제2/password.txt', 'r', encoding='utf-8') as f:
            encrypted_text = f.read().strip()
        caesar_cipher_decode(encrypted_text)
    except FileNotFoundError:
        print('password.txt 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'기타 오류 발생: {e}')
