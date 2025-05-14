import zipfile
import time
import multiprocessing

zip_file_path = '필수과정2/문제1/emergency_storage_key.zip'
characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
keyword = ''
min_length = 6
max_length = 12
num_workers = multiprocessing.cpu_count()

def unlock_zip(zip_file_path, password):
    try:
        with zipfile.ZipFile(zip_file_path) as zf:
            zf.extractall(pwd=password.encode('utf-8'))
            print(f'비밀번호 찾음: {password}')
            with open('필수과정2/문제1/password.txt', 'w', encoding='utf-8') as f:
                f.write(password)
            return True
    except:
        return False


def generate_permutations(characters, length):
    if length == 0:
        yield ''
    else:
        for c in characters:
            for p in generate_permutations(characters, length - 1):
                yield c + p

def generate_passwords(length, start_index):
    before_len = start_index
    after_len = length - len(keyword) - start_index
    for before in generate_permutations(characters, before_len):
        for after in generate_permutations(characters, after_len):
            yield before + keyword + after

def chunked_generator(generator, num_chunks, chunk_index):
    for i, item in enumerate(generator):
        if i % num_chunks == chunk_index:
            yield item

def worker(length, start_index, chunk_index, num_chunks, queue):
    gen = generate_passwords(length, start_index)
    for password in chunked_generator(gen, num_chunks, chunk_index):
        if unlock_zip(zip_file_path, password):
            queue.put(password)
            return

def run():
    for length in range(min_length, max_length + 1):
        print(f'문자열 길이 {length} 시도중')
        start_time = time.time()
        queue = multiprocessing.Queue()
        processes = []

        max_start_index = length - len(keyword)
        if max_start_index < 0:
            continue

        for start_index in range(max_start_index + 1):
            for chunk_index in range(num_workers):
                p = multiprocessing.Process(
                    target=worker,
                    args=(length, start_index, chunk_index, num_workers, queue)
                )
                p.start()
                processes.append(p)

        found_password = ''
        while True:
            try:
                found_password = queue.get(timeout=0.5)
                break
            except:
                if all(not p.is_alive() for p in processes):
                    break

        for p in processes:
            p.terminate()

        elapsed = time.time() - start_time
        if found_password:
            print(f'비밀번호: {found_password}')
            print(f'길이 {length}에서 찾음')
            print(f'시간: {elapsed:.2f}초')
            return
        else:
            print(f'길이 {length}에서는 실패')
            print(f'걸린 시간: {elapsed:.2f}초\n')

    print(f'\n{min_length} ~ {max_length} 사이 암호 길이에서 비밀번호를 찾지 못했습니다.')

if __name__ == '__main__':
    print(f'{min_length} ~ {max_length} 사이 암호 길이에서 비밀번호를 찾는 중...')
    print(f'키워드: {keyword}\n')
    run()