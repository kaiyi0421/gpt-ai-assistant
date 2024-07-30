from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)
root_dir = "/content/gdrive/My Drive/"

# 文件的正確路徑
file_path = '/content/gdrive/My Drive/人工膝關節置換術.pdf'
# 確認文件存在
import os
if os.path.exists(file_path):
    print("File exists")
else:
    print("File does not exist")
try:
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    print(f'The PDF has {number_of_pages} pages.')
except FileNotFoundError:
    print("File not found. Please check the file path.")
