"""ブックマークを整理する."""

import json
from os import path
import sys
from typing import *


def erase_duplication(res: Dict) -> Dict:
    """ブックマークの直列化データ内の重複するURIを消す."""

    def rec(added_uris: Set[str], res: Dict) -> Optional[Dict]:
        if 'uri' in res:
            if res['uri'] in added_uris:
                return None
            else:
                added_uris.add(res['uri'])
        ret = dict()
        for key, value in res.items():
            if key == 'children':
                children = []
                for child in res['children']:
                    unique_child = rec(added_uris, child)
                    if unique_child:
                        children.append(unique_child)
                ret['children'] = children
            else:
                ret[key] = value
        return ret

    return rec(set(), res)


def file_path_w(file_path: str) -> str:
    """読み込むファイルパスを元に, 書き込むファイルパスを存在するパスと重複しないように生成する."""
    (root, ext) = path.splitext(file_path)
    duplicatable_file_path_w = f'{root}_cleaned{ext}'
    ret = duplicatable_file_path_w
    i = 1
    while path.lexists(ret):
        (root, ext) = path.splitext(duplicatable_file_path_w)
        ret = f'{root} ({i}){ext}'
    return ret


def main():
    """コマンドライン引数の一つ目を読み込むファイル名として, ブックマーク内の重複するURIを削除する."""
    path_r = sys.argv[1]
    with open(path_r, encoding='utf-8') as f:
        d = json.load(f)
    unique_d = erase_duplication(d)
    path_w = file_path_w(path_r)
    with open(path_w, 'a', encoding='utf-8') as f:
        json.dump(unique_d, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
