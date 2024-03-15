# import numpy as np
# import platform
# from PIL import ImageFont, ImageDraw, Image
# from matplotlib import pyplot as plt

import uuid
import json
import time
import cv2
import requests

start = time.time()

api_url = 'https://klvmjhc48z.apigw.ntruss.com/custom/v1/20316/6e00886f7f04697713358f247e904d416eac2e6de60e0ede25abad97676fa360/general'
secret_key = 'S3FUc2tJYXNVY1hTa3RYZ0JKanJHWGl6RVlCaWFsbGs='

for i in range(1, 2):
  image_file = "./img/"+str(i)+".jpg"
  output_file = './mediText'+str(i)+'.text'

  request_json = {
      'images': [
          {
              'format': 'png',
              'name': 'demo'
          }
      ],
      'requestId': str(uuid.uuid4()),
      'version': 'V2',
      'timestamp': int(round(time.time() * 1000))
  }

  payload = {'message': json.dumps(request_json).encode('UTF-8')}
  files = [
    ('file', open(image_file,'rb'))
  ]
  headers = {
    'X-OCR-SECRET': secret_key
  }

  response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

  res = json.loads(response.text.encode('utf8'))
  # print(res['inferText'])
  
  article = []
  tList = res['images']
  
  # print(type(tList))
  print(tList)
  
  # for t in tList:
  #   arti = t['fields']
    
  #   for a in arti:
  #     a = a['inferText']
      
  #     article.append(a)
  
  # print(article)
  

  with open(output_file, 'w', encoding='utf-8') as outfile:
      json.dump(tList, outfile, indent=4, ensure_ascii=False)

  end = time.time()
  print(end-start)