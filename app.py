from datetime import datetime, timedelta

import psycopg2
from flask import Flask, render_template

# PostgreSQL 연결 정보
DB_HOST = 'database-1.crhwxgwlg3at.us-east-1.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'danuni'
DB_PASSWORD = 'gkekdms0429'
SSL_ROOT_CERT = './global-bundle.pem'

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # PostgreSQL 연결
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        # 데이터 조회 쿼리
        query = "SELECT * FROM sensor_data ORDER BY timestamp DESC ;"
        cursor.execute(query)
        sensor_data = cursor.fetchall()
        # timestamp 형식 변경 및 시간 추가
        modified_sensor_data = []
        for data in sensor_data:
            # timestamp를 datetime 객체로 변환
            timestamp = data[4]
            if isinstance(timestamp, datetime):
                # 시간에 9시간 추가
                timestamp += timedelta(hours=9)
                # 필요한 형식으로 포맷팅
                timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M')
                # 변경된 데이터를 리스트에 추가
                modified_sensor_data.append((data[0], data[1], data[2], data[3], timestamp_str))
                print(modified_sensor_data)

        # 가장 최근 데이터만 남기기 ; ID가 가장 큰 데이터
        latest_sensor_data = modified_sensor_data[0]
        print(f'last {latest_sensor_data}')



        return render_template('index.html', sensor_data=modified_sensor_data, latest_sensor_data=latest_sensor_data)

    except (Exception, psycopg2.Error) as error:
        print("데이터베이스 연결 오류:", error)
        return "데이터베이스 연결 오류"

    finally:
        # 연결 종료
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
