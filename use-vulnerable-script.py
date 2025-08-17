import requests

def make_request(url):
    """
    指定されたURLにHTTP GETリクエストを送信します。
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # エラーがあれば例外を発生させる
        print(f"Request to {url} was successful.")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    make_request("https://www.google.com")
