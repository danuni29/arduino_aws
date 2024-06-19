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
        query = "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10;"
        cursor.execute(query)
        sensor_data = cursor.fetchall()

        # HTML 템플릿 렌더링
        return render_template('index.html', sensor_data=sensor_data)

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
