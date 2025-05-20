def caesar_cipher_decode(target_text):
    def shift_char(c, shift):
        if c.isupper():
            return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        elif c.islower():
            return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        else:
            return c

    dictionary = ['mars']

    print('카이사르 암호 복호화\n')

    for shift in range(26):
        decrypted = ''.join(shift_char(c, shift) for c in target_text)
        print(f'{shift}: {decrypted}')
        lower_decrypted = decrypted.lower()

        if any(keyword in lower_decrypted for keyword in dictionary):
            print(f'\n{shift}번째 자리수에서 복호화 성공')
            with open('필수과정2/문제2/result.txt', 'w', encoding='utf-8') as f:
                f.write(decrypted)
            break
    else:
        print('\n키워드를 포함한 복호화 결과를 찾지 못했습니다.')

if __name__ == '__main__':
    try:
        with open('필수과정2/문제2/password.txt', 'r', encoding='utf-8') as f:
            encrypted_text = f.read().strip()
        caesar_cipher_decode(encrypted_text)
    except FileNotFoundError:
        print('password.txt 파일을 찾을 수 없습니다.')
