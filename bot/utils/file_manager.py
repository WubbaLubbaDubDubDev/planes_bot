import json
import os


def load_from_json(path: str):
    if os.path.isfile(path) and (os.stat(path).st_size > 0):
        with open(path, "r", encoding='utf-8') as file:
            return json.load(file)
    else:
        sessions_list = []
        with open(path, 'w', encoding='utf-8') as file:
            example = {
                 "session_name": "name_example",
                 "proxy": "type://user:pass@ip:port"
            }
            sessions_list.append(example)
            json.dump(sessions_list, file, ensure_ascii=False, indent=2)
        return sessions_list


def save_to_json(path: str, dict_: dict):
    sessions = load_from_json(path=path)
    sessions.append(dict_)
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(sessions, file, ensure_ascii=False, indent=2)


def rewrite_json(path: str, dict_):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(dict_, file, ensure_ascii=False, indent=2)

