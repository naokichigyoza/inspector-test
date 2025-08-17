import subprocess
import sqlite3
import pickle
import base64
import os

# --- 脆弱性のあるコードのサンプル ---

# 脆弱性1: ハードコードされたシークレット
# パスワードのような機密情報がコードに直接記述されています。
DB_PASSWORD = "password12345"

def get_user_data(username):
    """
    データベースからユーザー情報を取得する関数。
    """
    # 脆弱性2: SQLインジェクション
    # ユーザーからの入力をサニタイズせずに、直接SQLクエリ文字列に埋め込んでいます。
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # ユーザー入力をそのままクエリに結合しているため危険
        query = "SELECT * FROM users WHERE username = '" + username + "'"
        print(f"実行クエリ: {query}")
        
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"取得結果: {result}")
        
    except sqlite3.Error as e:
        print(f"データベースエラー: {e}")
    finally:
        if conn:
            conn.close()

def list_directory_files(directory):
    """
    指定されたディレクトリのファイル一覧を表示する関数。
    """
    # 脆弱性3: コマンドインジェクション
    # ユーザーからの入力を検証せずに、OSコマンドの一部として実行しています。
    # Linux/macOSでは `ls`, Windowsでは `dir` を想定しています。
    command = f"ls -l {directory}" # Windowsの場合は `dir {directory}`
    print(f"実行コマンド: {command}")
    
    # shell=True はコマンドインジェクションに対して特に危険です。
    subprocess.run(command, shell=True)


def deserialize_user_preference(data):
    """
    Base64エンコードされたデータをデシリアライズして、ユーザー設定を復元する関数。
    """
    # 脆弱性4: 安全でないデシリアライゼーション
    # 信頼できない可能性のあるデータを `pickle.loads()` でデシリアライズしています。
    try:
        decoded_data = base64.b64decode(data)
        user_pref = pickle.loads(decoded_data)
        print(f"ユーザー設定を復元しました: {user_pref}")
        return user_pref
    except Exception as e:
        print(f"デシリアライズ中にエラーが発生しました: {e}")


# --- 実行例 ---
if __name__ == "__main__":
    print("### SQLインジェクションの脆弱性テスト ###")
    # 正常な呼び出し
    get_user_data("alice")
    # 悪意のある呼び出し例
    # 全てのユーザー情報を取得しようと試みるペイロード
    get_user_data("' OR '1'='1")
    
    print("\n" + "-"*30 + "\n")

    print("### コマンドインジェクションの脆弱性テスト ###")
    # 正常な呼び出し
    list_directory_files(".")
    # 悪意のある呼び出し例
    # `id` コマンド（ユーザー情報を表示）を続けて実行しようと試みるペイロード
    list_directory_files(".; id")
    
    print("\n" + "-"*30 + "\n")

    print("### 安全でないデシリアライゼーションの脆弱性テスト ###")
    # 悪意のあるオブジェクトを作成し、エンコードする
    class ArbitraryCodeExecutor:
        def __reduce__(self):
            # デシリアライズ時にOSコマンド `whoami` を実行する
            return (os.system, ('whoami',))

    malicious_object = ArbitraryCodeExecutor()
    malicious_data = pickle.dumps(malicious_object)
    encoded_payload = base64.b64encode(malicious_data)
    
    print(f"悪意のあるペイロード: {encoded_payload.decode()}")
    deserialize_user_preference(encoded_payload)
