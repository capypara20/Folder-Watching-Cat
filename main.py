"""
Folder-Watching-Cat 🐱
フォルダを監視して、変更を検知したら通知する
"""

import json
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def load_config():
    """設定ファイルを読み込む"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


class CatWatcher(FileSystemEventHandler):
    """ファイル/フォルダの変更を監視する猫"""

    def __init__(self, file_patterns, folder_patterns):
        self.file_patterns = file_patterns
        self.folder_patterns = folder_patterns

    def check_pattern_match(self, name, patterns, is_directory=False):
        """名前がパターンに一致するかチェック"""
        matches = []

        # 完全一致
        if name in patterns.get("names", []):
            matches.append(f"ファイル名一致ﾆｬｰ: {name}")

        # 拡張子（ファイルのみ）
        if not is_directory:
            for ext in patterns.get("extensions", []):
                if name.endswith(ext):
                    matches.append(f"拡張子一致: {ext}")

        # 接頭辞
        for prefix in patterns.get("prefixes", []):
            if name.startswith(prefix):
                matches.append(f"接頭辞一致ﾆｬｰ: {prefix}")

        # 接尾辞（拡張子を除いた部分）
        name_without_ext = os.path.splitext(name)[0] if not is_directory else name
        for suffix in patterns.get("suffixes", []):
            if name_without_ext.endswith(suffix):
                matches.append(f"接尾辞一致ﾆｬｰ: {suffix}")

        return matches

    def on_created(self, event):
        """新しいファイル/フォルダが作成されたとき"""
        item_type = "フォルダ" if event.is_directory else "ファイル"
        print(f"🐱 ﾆｬｰﾝ！新しい{item_type}を見つけたﾆｬｰ！")
        print(f"   → {event.src_path}")

        # パターンマッチをチェック
        name = os.path.basename(event.src_path)
        if event.is_directory:
            matches = self.check_pattern_match(name, self.folder_patterns, is_directory=True)
        else:
            matches = self.check_pattern_match(name, self.file_patterns, is_directory=False)

        if matches:
            print(f"   🎯 パターンにマッチ！")
            for match in matches:
                print(f"      - {match}")

    def on_deleted(self, event):
        """ファイル/フォルダが削除されたとき"""
        item_type = "フォルダ" if event.is_directory else "ファイル"
        print(f"🐱 ﾆｬ!!? {item_type}が消えたニャ!!")
        print(f"   → {event.src_path}")

    def on_modified(self, event):
        """ファイル/フォルダが変更されたとき"""
        if not event.is_directory:
            print(f"🐱 ファイル変更されたﾆｬｰﾝ!")
            print(f"   → {event.src_path}")


def main():
    # 設定を読み込む
    config = load_config()
    watch_path = config.get("watch_path", "./watch_target")
    file_patterns = config.get("file_patterns", {})
    folder_patterns = config.get("folder_patterns", {})

    # 監視を開始
    event_handler = CatWatcher(file_patterns, folder_patterns)
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()

    print("=" * 50)
    print("🐱 にゃー Folder-Watching-Cat 起動しましたニャー！")
    print(f"   監視中: {watch_path}")
    print("   📁 ファイル検知パターン:")
    if file_patterns.get("names"):
        print(f"     名前: {file_patterns['names']}")
    if file_patterns.get("extensions"):
        print(f"     拡張子: {file_patterns['extensions']}")
    if file_patterns.get("prefixes"):
        print(f"     接頭辞: {file_patterns['prefixes']}")
    if file_patterns.get("suffixes"):
        print(f"     接尾辞: {file_patterns['suffixes']}")
    print("   📂 フォルダ検知パターン:")
    if folder_patterns.get("names"):
        print(f"     名前: {folder_patterns['names']}")
    if folder_patterns.get("prefixes"):
        print(f"     接頭辞: {folder_patterns['prefixes']}")
    if folder_patterns.get("suffixes"):
        print(f"     接尾辞: {folder_patterns['suffixes']}")
    print("   終了するには Ctrl+C を押してね")
    print("=" * 50)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🐱 またニャ！")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
