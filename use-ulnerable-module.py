from PIL import Image
import os

# このファイル自体はただのプレースホルダです。
# 実際に脆弱性をトリガーするには、特別に細工された画像ファイルが必要です。
malicious_file = "potentially_harmful_image.png"

print(f"Pillowのバージョン: {Image.__version__}")
print(f"'{malicious_file}' を開こうとしています...")

try:
    # 悪意のあるファイルを読み込むと、ここで大量のメモリが消費され
    # プロセスがクラッシュする可能性があります。
    with Image.open(malicious_file) as img:
        print("画像を開きました（これは実際にはトリガーされません）。")
        img.load()

except FileNotFoundError:
    print(f"エラー: '{malicious_file}' が見つかりません。")
    print("これはデモです。もし悪意のある画像ファイルがあれば、ここでDoSが発生する可能性があります。")
except Exception as e:
    print(f"画像の処理中にエラーが発生しました: {e}")
