import os
from PIL import Image
res_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
temp_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
try:
    os.mkdir(f'{temp_path}\\temp')
except:
    pass
os.chdir(f'{temp_path}\\temp')
def save_image_from_binary(binary_data, filename):
    with open(filename, mode='wb') as file:
        file.write(binary_data)
images = []
pages = [i for i in os.listdir(temp_path+r'\\'+'temp') if 'Result' in i]
pages = sorted(pages, key=lambda x:os.path.getmtime(temp_path+'\\'+'temp'+'\\'+x))
for i in pages:
    images.append(Image.open(temp_path+r'\\'+'temp'+r'\\'+str(i)))
images = [img.convert("RGB") for img in images]
# Создаем общий файл pdf #
os.chdir(res_path)
images[0].save(f'{'Result'}.pdf', 'PDF', append_images=images[1:len(images):1], save_all=True)
os.chdir(f"{temp_path}\\temp")
for i in os.listdir(f'{temp_path}\\temp'):
    os.remove(i)
print("Работа программы завершена!")
