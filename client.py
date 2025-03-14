import sys
import socket
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f"File created: {event.src_path}")
        print("created")
        notify_folder_update(b"created")


    def on_modified(self, event):
        logging.info(f"File modified: {event.src_path}")
        print("modified")
        notify_folder_update(b"modified")


    def on_deleted(self, event):
        logging.info(f"File deleted: {event.src_path}")
        print("deleted")
        notify_folder_update(b"deleted")


    def on_moved(self, event):
        logging.info(f"File moved: {event.src_path} -> {event.dest_path}")
        print("moved")
        notify_folder_update(b"moved")


def notify_folder_update(message):
    server_ip = "10.149.106.8"
    server_port = 5001
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_socket.sendall(message)
    client_socket.close()


def observe_sync_folder():
    logging.basicConfig(
        filename="sync_folder.log",
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', 
        )

    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = EventHandler()

    observer = Observer()
    observer.schedule(event_handler=event_handler, path=path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    observe_sync_folder()