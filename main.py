"""
Main script for cancelling class listings on AHA Atlas.
Handles account selection, cancellation method, token input, and batch/single cancellation.
Includes robust error handling and graceful shutdown.
"""

import sys
from utils.get_classes import get_classes
from utils.cancle_class import cancel_class


def account_selection() -> str:
    """Prompt user to select an account."""
    while True:
        print("Select an account to use:")
        account = input("Enter 1 for Nathan@shellcpr.com | 2 for onthegoCPRtn@outlook.com: ").strip()
        if account == '1':
            return 'acc_1'
        elif account == '2':
            return 'acc_2'
        else:
            print("Invalid selection. Please enter 1 or 2.")


def cancelation_method() -> str:
    """Prompt user to select cancellation method."""
    while True:
        method = input("Enter 1 for CSV | 2 for simple cancellation: ").strip()
        if method == '1':
            return 'csv'
        elif method == '2':
            return 'simple'
        else:
            print("Invalid selection. Please enter 1 or 2.")


def round_up_to_next_hundred(n: int) -> int:
    """Round up integer to next hundred."""
    return ((n // 100) + 1) * 100 if n % 100 != 0 else n


def get_token() -> str:
    """Prompt user for JWT token."""
    token = input("Enter your JWT token: ").strip()
    if not token:
        raise ValueError("Token cannot be empty.")
    return token


def read_csv(file_path: str) -> list:
    """Read class IDs from a CSV file."""
    import csv
    class_ids = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row:
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


def process_csv_cancellations(acc: str, token: str):
    """Cancel classes using IDs from a CSV file."""
    try:
        file_path = input("Enter the path to the CSV file containing class IDs: ").strip()
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
    except Exception as e:
        print(f"Error processing CSV cancellations: {e}")


def process_simple_cancellations(acc: str, token: str):
    """Cancel classes by fetching items from pages."""
    try:
        i = 0
        while True:
            try:
                items, is_last_page = get_classes(acc, i, token)
                print(items, is_last_page)
                if not items:
                    print(f"No items found on page {i + 1}.")
                    i += 1
                    continue

            except Exception as e:
                print(f"Error fetching classes for page {i + 1}: {e}")
                continue
            a = f"Processing page {i + 1}"
            print(a + ', Last page reached.' if is_last_page else a)
            for item in items:
                try:
                    class_id = item.get('classId')
                    status = item.get('status')
                except (KeyError, TypeError) as e:
                    print(f"Malformed item data: {e}")
                    continue
                if status in ("CANCELLED", "COMPLETED"):
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
            if is_last_page:
                break
            i += 1
        print("Process completed.")
    except Exception as e:
        print(f"Error processing simple cancellations: {e}")


def main():
    """Main entry point."""
    try:
        acc = account_selection()
        method = cancelation_method()
        token = get_token()
        if method == 'csv':
            process_csv_cancellations(acc, token)
        elif method == 'simple':
            process_simple_cancellations(acc, token)
        else:
            print("Invalid method selected.")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
