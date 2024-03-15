# import numpy as np
# import platform
# from PIL import ImageFont, ImageDraw, Image
# from matplotlib import pyplot as plt

import uuid
import json
import time
import requests
import os
import re
import string

start = time.time()


def string_to_int(s):
  try :
    temp = int(eval(str(s)))
    if type(temp) == int:
      return temp
    
  except :
    return

  
def valid(article):
  
  print(article)
  if "약국제출용" in article or "제출용" in article:
    
    print(len(article))
    article =  article[0 : 150]
    print(len(article))
    
    # print(article)
    article2 = []
    for a in article:
      a = a.replace(' ','')
      article2.append(a)
      
      
    # print(article2)
    
  # if "약국제출용" in article:
    # print(article)
    # str길이가 5 or 6인 값 추출
    list5 = list(filter(lambda x: len(x)==5, article2))
    list6 = list(filter(lambda x: len(x)==6, article2))
    # sList = list5.append(list6)
    # print(sList)
    # print(list5)
    # print(list6)
    
    
    iList = [] 
    
    # 그중, int변환 가능한 숫자만 추출 후 배열화
    for l in list5:
      # 구두 점 및 불필요한 텍스트 제거
      
      # l = re.sub(r'[.,"\'-?:!;]', '', l)
      # -가 붙은 코드는 유효하지 않음으로, 여기서 폐기
      
      # l = re.sub(r".", "x", l)
      l = re.sub(r"호", "", l)
      l = re.sub(r"제", "", l)
      
      oriLen = len(l)
      l = l.translate(str.maketrans('','',string.punctuation))
      l = string_to_int(l)
      if l is not None and len(str(l)) == 5:     
        
        iList.append(str(l))
          
        
    for l in list6:
      # 구두 점 및 불필요한 텍스트 제거
      
      # l = re.sub(r'[.,"\'-?:!;]', '', l)
      # -가 붙은 코드는 유효하지 않음으로, 여기서 폐기
      l = re.sub(r"호", "", l)
      l = re.sub(r"제", "", l)
      # l = re.sub(r"[^0-9]", "x", l)
      # l = re.sub(r".", "x", l)
      # l.replace("호","")
      # l.replace("제","")
      # l = re.sub(r"[^0-9]", "", l)
      oriLen = len(l)
      l = l.translate(str.maketrans('','',string.punctuation))
      l = string_to_int(l)
      if l is not None and len(str(l)) == oriLen :
        iList.append(str(l))
      
      # 밑쪽의 전화번호가 추가되는 경우, 뒷쪽에 붙을 수 밖에 없기에, 두개만 남기고
      if len(iList) >= 2:
        del iList[2:]
        
    return(iList) 
  
    
        
  else :
    return("약국 제출용이 아닙니다.")
          
  
   
      
    
  
  
  
# def check_odd_even(arr):
#     odd = [x for x in arr if x % 2 != 0]
#     even = [x for x in arr if x % 2 == 0]

#     if len(set(odd)) == 1:
#         print("모든 홀수열 동일.")
#     else:
#         print("홀수열 동일하지 않음.")

#     if len(set(even)) == 1:
#         print("모든 짝수열 동일.")
#     else:
#         print("짝수열 동일하지 않음.")
  
# CLOVA OCR
api_url = 'https://klvmjhc48z.apigw.ntruss.com/custom/v1/20316/6e00886f7f04697713358f247e904d416eac2e6de60e0ede25abad97676fa360/general'
secret_key = 'S3FUc2tJYXNVY1hTa3RYZ0JKanJHWGl6RVlCaWFsbGs='

imgDir = 'D:/drxDev/ocrCheck/presc1'

imgList = []
possible = ['.jpg']
# allList = []

# 폴더 내 이미지 파일만 읽기
for (root, dirs, files) in os.walk(imgDir):
  if len(files) > 0:
    for file_name in files:
      if os.path.splitext(file_name)[1] in possible:
        img_path = root + '/' + file_name
        img_path = img_path.replace('\\','/')
        imgList.append(img_path)

  
  for i in imgList:
    image_file = i
    # image_file = './img/X102914-1.jpg'
    # image_file = "./img/"+str(i)+".jpg"
    output_file = './testText'+str(i)+'.text'

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
    # print(tList)
    
    for t in tList:
      arti = t['fields']
      
      for a in arti:
        a = a['inferText']
        
        article.append(a)
    
    # print(article)
# article = ['□의료보호', '□산재보험', '자동차보험', '*****', '이비인후과', '52381', '정80mg', '보관하시기', '바랍니다.', 'NYCON', '복약지도를', '가톨릭대학', '우선하여야', '원외처방전은', '국민건강보험', '요양기관번호', '제13305', '가톨릭대학교', '58-255', '주민등록번호', '아니합니다.', '매운건수력약', '(사유등록된', '본인보관용은', '조제 연월일', '받으십시오.', '조제할 처방']

# 여기서 부터 후처리
    art = valid(article)

    art.sort()

    print("sort값",art)
    
    allList = []
    
    if len(art) == 2:
      if len(allList) == 0:
        pass
      
      if len(allList) == 2 and set(art) == set(allList):
        allList.clear()
        allList.append(art)
        print("동일 처방전으로 확인되었습니다.")
      
      else :
        pass
      
      print(i+"처방전이 정상처리 되었습니다.")
        
    elif len(art) == 1:    
      print("추출한 ocr 코드가 1개입니다.")
      break
      
    elif len(art) < 1:    
      print("추출한 ocr 코드가 없습니다.")
      break

    else :
      print("보다 많은 코드가 추출 되었습니다.")
      break
  
    
    
    # allList = allList.append(art[0])
    # allList = allList.append(art[1])
    # print(type(allList))
   
      
      
      
    
        # if c == 1:
        #   img1 = valid(article)
        #   print(img1)
        #   # img1 = set(img1)
          
        # elif c == 2:
        #   img2 = valid(article)
        #   print(img2)
        #   # img2 = set(img2)
        #   # true = [i for i, j in zip(img1,img2) if i == j]
        #   # if len(true) == 2:
        #   #   print("1,2번은 동일 처방전 입니다.")
        #   #   pass
          
        #   # else:
        #   #   print("동일 처방전이 아닙니다.")
        #   #   break
          
        # elif c == 3:
        #   img3 = valid(article)
        #   print(img3)
        #   # img3 = set(img3)
        #   # true = [i for i, j in zip(img1,img2,img3) if i == j]
        #   # if len(true) == 2:
        #   #   print("1,2,3,4번은 동일 처방전 입니다.")
        #   #   pass
          
        #   # else:
        #   #   print("동일 처방전이 아닙니다.")
        #   #   break
          
        # elif c == 4:
        #   img4 = valid(article)
        #   print(img4)
        #   # img4 = set(img4)
        #   # true = [i for i, j in zip(img1,img2,img3,img4) if i == j]
        #   # if len(true) == 2:
        #   #   print("1,2,3,4번은 동일 처방전 입니다.")
        #   #   pass
          
        #   # else:
        #   #   print("동일 처방전이 아닙니다.")
        #   #   break
          
        # elif c == 5:
        #   img5 = valid(article)
        #   print(img5)
        #   # img5 = set(img5)
        #   # true = [i for i, j in zip(img1,img2,img3,img4,img5) if i == j]
        #   # if len(true) == 2:
        #   #   print("번은 동일 처방전 입니다.")
        #   #   pass
          
        #   # else:
        #   #   print("동일 처방전이 아닙니다.")
        #   #   break
          
        # else :
        #   pass
        
        # img1 = set(img1)
        # img2 = set(img2)
        # img3 = set(img3)
        # img4 = set(img4)
        # img5 = set(img5)
        
        # # finalList = img1 & img2 & img3 & img4 & img5
        
        # finalList = img1.intersection(img2,img3,img4,img5)
        
        # print(finalList)
        # print(len(finalList))
        
        # if len(finalList) == 2:
        #   print("동일 처방전 입니다.")
          
        # else :
        #   print("동일 처방전이 아닙니다.")
       


  # with open(output_file, 'w', encoding='utf-8') as outfile:
  #     json.dump(article, outfile, indent=4, ensure_ascii=False)

end = time.time()
print(end-start)