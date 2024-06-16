from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
from datetime import datetime, timedelta
import os
import schedule
import time
from dotenv import load_dotenv

import cv2
import numpy as np
from tensorflow import keras
import tensorflow as tf

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float
from models import Notifications


load_dotenv()
DBUSER = os.getenv("dbuser")
DBUSERPASSWORD = os.getenv("dbpassword")
DBHOST = os.getenv("dbhost")
DBPORT = os.getenv("dbport")
DB = os.getenv("db")
SECRETKEY = os.getenv("secret_key")
FOLDER = os.getenv("upload_folder")
CLIENTIDSENTIETALHUB = os.getenv("client_id")
CLIENTSECRETSENTIETALHUB = os.getenv("client_secret")
model_path = 'model.keras'


def is_image_mostly_black(image, threshold=30, black_ratio=0.8):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    black_pixels = np.sum(gray_image < threshold)
    total_pixels = image.shape[0] * image.shape[1]
    return black_pixels / total_pixels > black_ratio


def inference(image_bytes, m_path):
    test_arr = []
    physical_devices = tf.config.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
        # print(f"Использует GPU: {physical_devices[0].name}")
    else:
        pass
        # print("Не навшел GPU. Использует CPU.")
    nparr = np.frombuffer(image_bytes, np.uint8)
    # test_image = cv2.imread(img_path)
    test_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if is_image_mostly_black(test_image):
        return 1, 0
    test_image = cv2.resize(test_image, (32, 32))
    test_image = np.array(test_image)
    test_image = test_image / 255
    test_image = test_image.reshape(1, 32, 32, 3)
    test_arr.append(test_image)
    model = keras.models.load_model(m_path)
    res = model.predict(test_arr)
    return res[0][0], res[0][1]


def fetch_oauth_token():
    token_url = 'https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token'
    client = BackendApplicationClient(client_id=CLIENTIDSENTIETALHUB)
    oauth = OAuth2Session(client=client)

    def sentinelhub_compliance_hook(response):
        response.raise_for_status()
        return response

    oauth.register_compliance_hook("access_token_response", sentinelhub_compliance_hook)

    token = oauth.fetch_token(token_url=token_url, client_secret=CLIENTSECRETSENTIETALHUB)
    # print(token)
    return token


def fetch_images(token, bbox, start_time, end_time, session):
    start_str = start_time.strftime('%Y-%m-%dT00:00:00Z')
    end_str = end_time.strftime('%Y-%m-%dT00:00:00Z')

    url = "https://services.sentinel-hub.com/api/v1/process"
    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "Content-Type": "application/json",
        "Accept": "image/jpeg"
    }

    request_data = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "bbox": bbox
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": start_str,
                        "to": end_str
                    }
                }
            }]
        },
        "evalscript": """
            //VERSION=3

            function setup() {
              return {
                input: ["B02", "B03", "B04"],
                output: {
                  bands: 3
                }
              };
            }

            function evaluatePixel(
              sample,
              scenes,
              inputMetadata,
              customData,
              outputMetadata
            ) {
              return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
            }
        """
    }

    try:
        response = requests.post(url, headers=headers, json=request_data)
        response.raise_for_status()
        image_data_list = response.content.split(b'\r\n\r\n')
        os.makedirs('satellite_images', exist_ok=True)
        dir_name = f"satellite_images/{start_time.strftime('%Y_%m_%d')}_{end_time.strftime('%Y_%m_%d')}"
        os.makedirs(dir_name, exist_ok=True)
        for index, image_data in enumerate(image_data_list):
            predict = inference(image_data, model_path)
            # print(predict)
            if predict[0] <= 0.5:
                if image_data.startswith(b'\xff\xd8'):
                    filename = f'{dir_name}/image_{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}.jpg'
                    session.add(Notifications(date_time=start_time.strftime('%Y_%m_%d'), text=f'Обнаружена гарь в квадрате с координатам: ({bbox[0]}, {bbox[1]}) ({bbox[2]}, {bbox[3]})', link_res=filename))
                    session.commit()
                    with open(filename, 'wb') as f:
                        f.write(image_data)
                    print(f'Изображение с гарью сохранено как {filename}')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")


def main():
    Base = declarative_base()
    DATABASE_URL = f"postgresql://{DBUSER}:{DBUSERPASSWORD}@{DBHOST}:{DBPORT}/{DB}"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    token = fetch_oauth_token()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=24)

    min_lat, min_lon = 50.0, 156.0
    max_lat, max_lon = 60.0, 165.0

    lat_step = (max_lat - min_lat) / 100
    lon_step = (max_lon - min_lon) / 100

    for i in range(100):
        for j in range(100):
            bbox = [
                min_lon + j * lon_step,
                min_lat + i * lat_step,
                min_lon + (j + 1) * lon_step,
                min_lat + (i + 1) * lat_step
            ]
            fetch_images(token, bbox, start_time, end_time, session)
    session.close()


def run_daily():
    schedule.every().day.at("02:00").do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_daily()