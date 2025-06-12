import csv
import os
import mysql.connector

class MySQLHelper:
    def __init__(self, host, user, password, database, sql_init_file=None):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print(f'MySQL 연결 오류: {e}')
            if sql_init_file and os.path.exists(sql_init_file):
                print(f'{sql_init_file} 파일을 실행하여 DB 및 테이블을 만듭니다.')
                self.init_db(host, user, password, sql_init_file)
                self.conn = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
                self.cursor = self.conn.cursor()
            else:
                raise

    def init_db(self, host, user, password, sql_file):
        with open(sql_file, encoding='utf-8') as f:
            sql_script = f.read()
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        for stmt in sql_script.split(';'):
            stmt = stmt.strip()
            if stmt:
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    print(f'쿼리 실행 중 오류: {e}\n문장: {stmt}')
        conn.commit()
        cursor.close()
        conn.close()

    def executemany(self, query, param_list):
        try:
            self.cursor.executemany(query, param_list)
            self.conn.commit()
        except Exception as e:
            print(f'쿼리 실행 중 오류: {e}')
            self.conn.rollback()
            raise

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(f'연결 종료 오류: {e}')

csv_file = '과정3/mars_weathers_data.csv'
sql_init_file = '과정3/mars_maker.sql'

if not os.path.exists(csv_file):
    print(f'오류: 파일 "{csv_file}"을(를) 찾을 수 없습니다.')
else:
    try:
        print('CSV 파일 내용:')
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            print(header)
            for row in reader:
                print(row)

        print('\n\n')
        data_to_insert = []
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                try:
                    mars_date = row['mars_date']
                    temp = float(row['temp'])
                    storm = int(row['storm'])
                    data_to_insert.append((mars_date, temp, storm))
                except Exception as e:
                    print(f'{idx+2}번째 줄 데이터 오류: {e}')

        if data_to_insert:
            db = MySQLHelper(
                host='localhost',
                user='root',
                password='password',  # 실제 비밀번호로 변경
                database='mars_db',
                sql_init_file=sql_init_file
            )
            insert_query = '''
                INSERT INTO mars_weather (mars_date, temp, storm)
                VALUES (%s, %s, %s)
            '''
            print('INSERT중')
            db.executemany(insert_query, data_to_insert)
            db.close()
            print('DB 입력 완료')
        else:
            print('입력할 데이터가 없습니다.')

    except Exception as e:
        print(f'전체 처리 중 오류 발생: {e}')
