"""
Folder-Watching-Cat 🐱
フォルダを監視して、変更を検知したら通知する
"""

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class CatWatcher(FileSystemEventHandler):
    """ファイル/フォルダの変更を監視する猫"""

    def on_created(self, event):
        """新しいファイル/フォルダが作成されたとき"""
        item_type = "フォルダ" if event.is_directory else "ファイル"
        print(f"🐱 にゃ！新しい{item_type}を見つけたよ！")
        print(f"   → {event.src_path}")

    def on_deleted(self, event):
        """ファイル/フォルダが削除されたとき"""
        item_type = "フォルダ" if event.is_directory else "ファイル"
        print(f"🐱 あれ？{item_type}が消えたよ...")
        print(f"   → {event.src_path}")

    def on_modified(self, event):
        """ファイル/フォルダが変更されたとき"""
        if not event.is_directory:
            print(f"🐱 ファイルが変更されたよ！")
            print(f"   → {event.src_path}")


def main():
    # 監視するフォルダ（同じディレクトリの watch_target フォルダ）
    watch_path = "./watch_target"

    # 監視を開始
    event_handler = CatWatcher()
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()

    print("=" * 50)
    print("🐱 Folder-Watching-Cat 起動！")
    print(f"   監視中: {watch_path}")
    print("   終了するには Ctrl+C を押してね")
    print("=" * 50)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🐱 またね！")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
