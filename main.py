from get_classes import get_classes
from delete_class import cancel_class


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

def round_up_to_next_hundred(n: int) -> int:
    return ((n // 100) + 1) if n % 100 != 0 else int(n / 100)


def main():
    try:
        acc = account_selection()
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
            items = get_classes(acc, i)
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

            if status == "CANCELLED":
                # print(f"Class ID {class_id} is already cancelled.")
                continue
            if class_id:
                try:
                    response_code = cancel_class(acc, class_id)
                    if response_code == 200:
                        print(f"Successfully cancelled class ID {class_id}.")
                    else:
                        print(f"Failed to cancel class ID {class_id}. Response code: {response_code}")
                except Exception as e:
                    print(f"Error cancelling class ID {class_id}: {e}")
    print("Process completed.")


if __name__ == "__main__":
    main()