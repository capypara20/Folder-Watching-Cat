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

    def __init__(self, patterns):
        self.patterns = patterns

    def check_pattern_match(self, filename):
        """ファイル名がパターンに一致するかチェック"""
        matches = []

        # 完全一致
        if filename in self.patterns.get("filenames", []):
            matches.append(f"ファイル名一致: {filename}")

        # 拡張子
        for ext in self.patterns.get("extensions", []):
            if filename.endswith(ext):
                matches.append(f"拡張子一致: {ext}")

        # 接頭辞
        for prefix in self.patterns.get("prefixes", []):
            if filename.startswith(prefix):
                matches.append(f"接頭辞一致: {prefix}")

        # 接尾辞（拡張子を除いた部分）
        name_without_ext = os.path.splitext(filename)[0]
        for suffix in self.patterns.get("suffixes", []):
            if name_without_ext.endswith(suffix):
                matches.append(f"接尾辞一致: {suffix}")

        return matches

    def on_created(self, event):
        """新しいファイル/フォルダが作成されたとき"""
        item_type = "フォルダ" if event.is_directory else "ファイル"
        print(f"🐱 ﾆｬｰﾝ！新しい{item_type}を見つけたﾆｬｰ！")
        print(f"   → {event.src_path}")

        # ファイルの場合、パターンマッチをチェック
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            matches = self.check_pattern_match(filename)
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
            print(f"🐱 ファイルが変更されたよ！")
            print(f"   → {event.src_path}")


def main():
    # 設定を読み込む
    config = load_config()
    watch_path = config.get("watch_path", "./watch_target")
    patterns = config.get("patterns", {})

    # 監視を開始
    event_handler = CatWatcher(patterns)
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()

    print("=" * 50)
    print("🐱 にゃー Folder-Watching-Cat 起動しましたニャー！")
    print(f"   監視中: {watch_path}")
    print("   検知パターン:")
    if patterns.get("filenames"):
        print(f"     ファイル名: {patterns['filenames']}")
    if patterns.get("extensions"):
        print(f"     拡張子: {patterns['extensions']}")
    if patterns.get("prefixes"):
        print(f"     接頭辞: {patterns['prefixes']}")
    if patterns.get("suffixes"):
        print(f"     接尾辞: {patterns['suffixes']}")
    print("   終了するには Ctrl+C を押してニャー!")
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
