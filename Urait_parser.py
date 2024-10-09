# импортирование библиотек
import os
import sys
from time import sleep
from datetime import datetime
from PIL import Image
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
# создание пути
res_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
temp_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
try:
    os.mkdir(f'{temp_path}\\temp')
except:
    pass
os.chdir(f'{temp_path}\\temp')
# необходимые функции
def save_image_from_binary(binary_data, filename):
    with open(filename, mode='wb') as file:
        file.write(binary_data)
# получение ссылки на книгу #
url = input("Введите ссылку на книгу, которую хотите скачать: \n")
login = input("Введите логин: \n")
password = input("Введите пароль: \n")
r = requests.get(url)
if 'https://urait.ru/book/' in url and r.status_code==200:
    print("Получаем информацию о книге...")
book_name = BeautifulSoup(r.text, 'html.parser').find(class_="page-content-head__title book_title").text
book_pages = int(BeautifulSoup(r.text, 'html.parser').find(class_="book-about-produce__info").text)
print(f'Название книги: {book_name}',f'Число страниц: {book_pages}',sep='\n')
options = Options()
options.page_load_strategy = 'eager'
options.add_argument("--headless")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.execute_script("document.body.style.zoom='50%'")
driver.get(f'https://urait.ru/viewer/{url.split(r'/')[-1]}#page/{1}')
sleep(3)
button = driver.find_element(By.ID, "viewer__header__auth")
button.click()
sleep(3)
auth_1 = driver.find_element(By.ID, 'email')
auth_1.send_keys(login)
sleep(3)
auth_2 = driver.find_element(By.ID, 'password')
auth_2.send_keys(password)
sleep(3)
button_ = driver.find_element(By.CLASS_NAME, "button-orange")
button_.click()
sleep(3)
flag = True

for i in range(1, book_pages+1):
    driver.get(f'https://urait.ru/viewer/{url.split(r'/')[-1]}#page/{i}')
    if flag:
        sleep(10)
        flag = False
    else:
        sleep(1)
    data = driver.get_screenshot_as_png()
    save_image_from_binary(data, f'Page-{i}.png')
    im = Image.open(f"Page-{i}.png")
    new_im = im.crop((2140, 190, 4020, 2960))
    new_im.save(f"Result-{i}.png", quality=100)
# Собираем все файлы png #
images = []
pages = [i for i in os.listdir(temp_path+r'\\'+'temp') if 'Result' in i]
pages = sorted(pages, key=lambda x:os.path.getmtime(temp_path+'\\'+'temp'+'\\'+x))
for i in pages:
    images.append(Image.open(temp_path+r'\\'+'temp'+r'\\'+str(i)))
images = [img.convert("RGB") for img in images]
# Создаем общий файл pdf #
os.chdir(res_path)
images[0].save(f'{book_name}.pdf', 'PDF', append_images=images[1:len(images):1], save_all=True)
driver.close()
os.chdir()
print("Работа программы завершена!")
sleep(3)
sys.exit(1)
