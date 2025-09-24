from get_classes import get_classes
from delete_class import cancel_class
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import sys

def round_up_to_next_hundred(n: int) -> int:
    return ((n // 100) + 1) * 100 if n % 100 != 0 else n + 100

def fetch_page(page_num, lock):
    try:
        items = get_classes(page_num)
        if not items:
            with lock:
                print(f"No items found on page {page_num + 1}.")
            return []
        return items
    except Exception as e:
        with lock:
            print(f"Error fetching classes for page {page_num + 1}: {e}")
        return []

def cancel_class_threadsafe(class_id, status, lock):
    if status == "CANCELLED":
        with lock:
            print(f"Class ID {class_id} is already cancelled.")
        return
    if class_id:
        try:
            response_code = cancel_class(class_id)
            with lock:
                if response_code == 200:
                    print(f"Successfully cancelled class ID {class_id}.")
                else:
                    print(f"Failed to cancel class ID {class_id}. Response code: {response_code}")
        except Exception as e:
            with lock:
                print(f"Error cancelling class ID {class_id}: {e}")

def main():
    try:
        user_pages = int(input("Enter the number of pages to fetch (each page contains up to 100 classes): "))
        if user_pages <= 0:
            print("Number of pages must be positive.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return

    total_page = int(round_up_to_next_hundred(user_pages) / 100)
    print(f"Fetching {total_page} pages in parallel...")

    lock = threading.Lock()
    all_items = []
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_page = {executor.submit(fetch_page, i, lock): i for i in range(total_page)}
            for future in as_completed(future_to_page):
                items = future.result()
                if items:
                    all_items.extend(items)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Stopping fetch operations...")
        executor.shutdown(wait=False, cancel_futures=True)
        sys.exit(1)

    print(f"Fetched {len(all_items)} classes. Cancelling in parallel...")

    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for item in all_items:
                try:
                    class_id = item.get('classId')
                    status = item.get('status')
                except (KeyError, TypeError) as e:
                    with lock:
                        print(f"Malformed item data: {e}")
                    continue
                futures.append(executor.submit(cancel_class_threadsafe, class_id, status, lock))
            for _ in as_completed(futures):
                pass  # All output is handled in the thread-safe function
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Stopping cancel operations...")
        executor.shutdown(wait=False, cancel_futures=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
