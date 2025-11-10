import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/todos/"

def print_section_header(title):
    """섹션 구분을 위한 헤더를 출력합니다."""
    print("\n" + "="*50)
    print(f"=== {title} ===")
    print("="*50)

def handle_response(response, success_message="성공"):
    """HTTP 응답을 처리하고 출력합니다."""
    status_code = response.status_code
    
    if status_code >= 200 and status_code < 300:
        # 2xx 성공 코드
        try:
            if status_code == 204:
                print(f"상태 코드: {status_code} - {success_message} (내용 없음)")
                return None
            
            data = response.json()
            print(f"상태 코드: {status_code} - {success_message}")
            print(json.dumps(data, indent=4, ensure_ascii=False))
            return data
        except requests.exceptions.JSONDecodeError:
            print(f"상태 코드: {status_code} - {success_message} (응답 본문 없음)")
            return None
            
    else:
        # 4xx, 5xx 오류 코드
        try:
            error_data = response.json()
            print(f"오류 코드: {status_code} - 실패")
            print(json.dumps(error_data, indent=4, ensure_ascii=False))
        except:
            print(f"오류 코드: {status_code} - 서버에서 알 수 없는 오류 발생")
        return None

def create_todo(item_content):
    """POST 요청: 새로운 TODO 항목을 생성합니다."""
    url = BASE_URL
    data = {"item": item_content}
    print(f"-> POST 요청: {url}, 데이터: {data}")
    try:
        response = requests.post(url, json=data)
        return handle_response(response, f"항목 생성 완료: '{item_content}'")
    except requests.exceptions.ConnectionError:
        print("서버 연결 오류: FastAPI 서버가 실행 중인지 확인하세요.")
        return None

def get_all_todos():
    """GET 요청: 전체 TODO 리스트를 조회합니다."""
    url = BASE_URL
    print(f"-> GET 요청: {url}")
    try:
        response = requests.get(url)
        return handle_response(response, "전체 목록 조회 완료")
    except requests.exceptions.ConnectionError:
        print("서버 연결 오류: FastAPI 서버가 실행 중인지 확인하세요.")
        return None

def get_single_todo(item_id):
    """GET 요청: 특정 ID의 TODO 항목을 조회합니다."""
    url = f"{BASE_URL}{item_id}"
    print(f"-> GET 요청: {url}")
    try:
        response = requests.get(url)
        return handle_response(response, f"ID {item_id} 항목 조회 완료")
    except requests.exceptions.ConnectionError:
        print("서버 연결 오류: FastAPI 서버가 실행 중인지 확인하세요.")
        return None

def update_todo(item_id, new_content):
    """PUT 요청: 특정 ID의 TODO 항목을 수정합니다."""
    url = f"{BASE_URL}{item_id}"
    data = {"item": new_content}
    print(f"-> PUT 요청: {url}, 새 데이터: {data}")
    try:
        response = requests.put(url, json=data)
        return handle_response(response, f"ID {item_id} 항목 수정 완료")
    except requests.exceptions.ConnectionError:
        print("서버 연결 오류: FastAPI 서버가 실행 중인지 확인하세요.")
        return None

def delete_todo(item_id):
    """DELETE 요청: 특정 ID의 TODO 항목을 삭제합니다."""
    url = f"{BASE_URL}{item_id}"
    print(f"-> DELETE 요청: {url}")
    try:
        response = requests.delete(url)
        return handle_response(response, f"ID {item_id} 항목 삭제 완료")
    except requests.exceptions.ConnectionError:
        print("서버 연결 오류: FastAPI 서버가 실행 중인지 확인하세요.")
        return None

def display_menu():
    """메뉴를 화면에 출력합니다."""
    print_section_header("TODO 클라이언트 앱 (CRUD 메뉴)")
    print("1. [C] 항목 생성 (POST)")
    print("2. [R] 전체 조회 (GET)")
    print("3. [R] 개별 조회 (GET /{id})")
    print("4. [U] 항목 수정 (PUT /{id})")
    print("5. [D] 항목 삭제 (DELETE /{id})")
    print("0. 프로그램 종료")
    print("="*50)

def main():
    while True:
        display_menu()
        choice = input("기능을 선택하세요 (0-5): ").strip()
        
        if choice == '1':
            print_section_header("1. 항목 생성 (POST)")
            item = input("새로운 TODO 항목 내용을 입력하세요: ").strip()
            if item:
                create_todo(item)
            else:
                print("항목 내용은 비워둘 수 없습니다. (400 에러 유발 가능)")

        elif choice == '2':
            print_section_header("2. 전체 조회 (GET)")
            get_all_todos()

        elif choice == '3':
            print_section_header("3. 개별 조회 (GET)")
            try:
                item_id = int(input("조회할 항목의 ID를 입력하세요: "))
                get_single_todo(item_id)
            except ValueError:
                print("ID는 정수(숫자)만 입력해야 합니다.")

        elif choice == '4':
            print_section_header("4. 항목 수정 (PUT)")
            try:
                item_id = int(input("수정할 항목의 ID를 입력하세요: "))
                new_content = input("새로운 TODO 항목 내용 (생략 가능): ").strip()
                
                if not new_content:
                    print("빈 문자열로 수정 요청합니다. (서버에서 빈 값 허용 여부에 따라 다름)")
                
                update_todo(item_id, new_content)
                
            except ValueError:
                print("ID는 정수(숫자)만 입력해야 합니다.")

        elif choice == '5':
            print_section_header("5. 항목 삭제 (DELETE)")
            try:
                item_id = int(input("삭제할 항목의 ID를 입력하세요: "))
                delete_todo(item_id)
            except ValueError:
                print("ID는 정수(숫자)만 입력해야 합니다.")

        elif choice == '0':
            print("\n프로그램을 종료합니다. 감사합니다.")
            sys.exit(0)

        else:
            print("잘못된 선택입니다. 0부터 5 사이의 숫자를 입력해 주세요.")
        
        input("\n(엔터를 눌러 메뉴로 돌아가세요...)")

if __name__ == "__main__":
    main()