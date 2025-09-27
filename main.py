from utils.get_classes import get_classes
from utils.cancle_class import cancel_class


def account_selection() -> str:
    while True:
        print("Select an account to use:")
        account = input("Enter 1 for Nathan@shellcpr.com | 2 for onthegoCPRtn@outlook.com: ")
        if account == '1':
            return 'acc_1'
        elif account == '2':
            return 'acc_2'
        else:
            print("Invalid selection. Please enter 1 or 2.")

def cancelation_method() -> str:
    while True:
        method = input("Enter 1 for `CSV` | 2 for simple cancelation: ")
        if method == '1':
            return 'csv'
        elif method == '2':
            return 'simple'
        else:
            print("Invalid selection. Please enter 1 or 2.")

def round_up_to_next_hundred(n: int) -> int:
    return ((n // 100) + 1) if n % 100 != 0 else int(n / 100)

def get_token() -> str:
    token = input("Enter your JWT token: ").strip()
    if not token:
        raise ValueError("Token cannot be empty.")
    return token

def read_csv(file_path: str) -> list:
    import csv
    class_ids = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row:  # Ensure the row is not empty
                    try:
                        class_id = int(row[0])
                        class_ids.append(class_id)
                    except ValueError:
                        print(f"Invalid class ID in CSV: {row[0]}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    return class_ids

def main():
    try:
        acc = account_selection()
        method = cancelation_method()
        token = get_token()
        if method == 'csv':
            file_path = input("Enter the path to the CSV file containing class IDs: ")
            class_ids = read_csv(file_path)
            if not class_ids:
                print("No valid class IDs found in the CSV file.")
                return
            for class_id in class_ids:
                try:
                    response_code = cancel_class(acc, class_id, token)
                    if response_code == 200:
                        print(f"Successfully cancelled class ID {class_id}.")
                    else:
                        print(f"Failed to cancel class ID {class_id}. Response code: {response_code}")
                except Exception as e:
                    print(f"Error cancelling class ID {class_id}: {e}")
            print("Process completed.")
            return
        print("https://atlas.heart.org/organisation/class-listing")
        user_pages = int(input("Enter the number of items displaying on the above page of entered account: "))
        if user_pages <= 0:
            print("Number of pages must be positive.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return

    total_page = round_up_to_next_hundred(user_pages)
    print(f"Fetching {total_page} pages...")

    for i in range(total_page):
        print(f"Processing page {i + 1} of {total_page}")
        try:
            items = get_classes(acc, i, token)
            if not items:
                print(f"No items found on page {i + 1}.")
                continue
        except Exception as e:
            print(f"Error fetching classes for page {i + 1}: {e}")
            continue

        for item in items:
            try:
                class_id = item.get('classId')
                status = item.get('status')
            except (KeyError, TypeError) as e:
                print(f"Malformed item data: {e}")
                continue

            if status == "CANCELLED" or status == "COMPLETED":
                # print(f"Class ID {class_id} is already cancelled.")
                continue
            if class_id:
                try:
                    response_code = cancel_class(acc, class_id, token)
                    if response_code == 200:
                        print(f"Successfully cancelled class ID {class_id}.")
                    else:
                        print(f"Failed to cancel class ID {class_id}. Response code: {response_code}")
                except Exception as e:
                    print(f"Error cancelling class ID {class_id}: {e}")
    print("Process completed.")


if __name__ == "__main__":
    main()