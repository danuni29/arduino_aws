from datetime import time
import psycopg2
import serial
import re
import os

# RDS 인스턴스 정보
DB_HOST = os.environ['database-1.crhwxgwlg3at.us-east-1.rds.amazonaws.com']
DB_PORT = os.environ['5432']
DB_NAME = os.environ['postgres']
DB_USER = os.environ['danuni']
DB_PASSWORD = os.environ['gkekdms0429']
SSL_ROOT_CERT = './global-bundle.pem'  # Lambda에서 필요한 경우 경로 설정

# PostgreSQL에 데이터 삽입 함수
def insert_data(temp, hum, soil_moisture):
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        insert_query = """INSERT INTO sensor_data (temperature, humidity, soil_moisture) VALUES (%s, %s, %s)"""
        record_to_insert = (temp, hum, soil_moisture)
        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        cursor.close()
        connection.close()
        print("데이터가 성공적으로 삽입되었습니다.")
    except (Exception, psycopg2.Error) as error:
        print("데이터베이스 연결 오류:", error)

# Lambda 핸들러 함수
def lambda_handler(event, context):
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # 시리얼 포트 경로 설정
    interval_seconds = 180  # 데이터 수집 주기 설정

    while True:
        start_time = time.time()

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received: {line}")
            # 정규식을 사용하여 데이터 파싱
            match = re.match(r"temp: (\d+\.\d+) °C, hum: (\d+\.\d+) %, Soil moisture: (\d+)", line)
            if match:
                temp = float(match.group(1))
                hum = float(match.group(2))
                soil_moisture = int(match.group(3))
                insert_data(temp, hum, soil_moisture)

        elapsed_time = time.time() - start_time
        if elapsed_time < interval_seconds:
            time.sleep(interval_seconds - elapsed_time)
