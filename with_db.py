import psycopg2
import serial
import time
import re

# RDS 인스턴스 정보
DB_HOST = 'database-1.crhwxgwlg3at.us-east-1.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'danuni'
DB_PASSWORD = 'gkekdms0429'
SSL_ROOT_CERT = './global-bundle.pem'

# 아두이노에서 들어온 값을 postgresql에 저장할거야앗
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





def main():
    ser = serial.Serial('COM3', 9600)
    time.sleep(2)
    interval_seconds = 180
    # while True:
    #     if ser.in_waiting != 0:
    #         data = ser.readline()
    #         print(data.decode()[:-2])
    #         time.sleep(1)
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


if __name__ == '__main__':
    main()