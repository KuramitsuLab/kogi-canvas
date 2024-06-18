import requests
import os
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

uuid0 = -1

def download_image(url, save_dir='images'):
    global uuid0
    # 画像をダウンロード
    response = requests.get(url)
    response.raise_for_status()  # エラーチェック

    # URLからファイル名を抽出
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # ファイル名が存在しない場合は、画像の種類から生成
    if not filename:
        img = Image.open(BytesIO(response.content))
        ext = img.format.lower()
        uuid0 += 1
        filename = f'image{uuid0}.{ext}'
    
    # 保存ディレクトリを作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # ファイルを保存
    save_path = os.path.join(save_dir, filename)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f'Image saved to {save_path}')
    return save_path

def resize_image(image_path, new_width=None, new_height=None):
    # 画像を開く
    if new_width is None and new_height is None:
        return image_path

    with Image.open(image_path) as img:
        # 現在の幅と高さを取得
        width, height = img.size
        print(f"Original width: {width}, Original height: {height}")
        if new_height is None:
            new_height = int(height * new_width / width)
        if new_width is None:
            new_width = int(width * new_height / height)

        # 画像をリサイズ
        resized_img = img.resize((new_width, new_height))

        path, ext = image_path.rpartition('.')
        output_path = f'{path}_{new_width}x{new_height}.{ext}'
        # リサイズされた画像を保存
        resized_img.save(output_path)
        print(f"Resized image saved as: {output_path}")
        return output_path

_CACHE = {}

def load_image(url_or_imagepath, width=None, height=None):
    global _CACHE
    if url_or_imagepath.startswith('http://') or url_or_imagepath.startswith('https://'):
        if url_or_imagepath not in _CACHE:
            _CACHE[url_or_imagepath] = download_image(url_or_imagepath)
        save_path = _CACHE[url_or_imagepath]
    if

