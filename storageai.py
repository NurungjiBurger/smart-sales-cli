import json
import os

DATA_DIR = "data"


def load_data(filename):
    """data/{filename}.json 파일을 읽어 Python 객체로 반환한다.
    파일이 없거나 JSON 형식이 깨졌으면 빈 리스트를 반환한다.
    """
    filepath = os.path.join(DATA_DIR, f"{filename}.json")
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_data(filename, data):
    """Python 객체를 data/{filename}.json 파일에 저장한다.
    data 디렉터리가 없으면 생성한다.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{filename}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)