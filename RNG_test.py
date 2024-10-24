import json
import random

def test_example():
    assert True

def load_lucky_items():
    with open("Lucky.json", "r") as file:
        return json.load(file)

def load_or_create_yourstuff():
    try:
        with open("Yourstuff.json", "r") as file:
            data = file.read()
            if not data:
                return {}
            return json.loads(data)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error: Yourstuff.json is corrupted. Initializing as empty.")
        return {}

def save_yourstuff(your_stuff):
    with open("Yourstuff.json", "w") as file:
        json.dump(your_stuff, file, indent=4)

def print_item_chances(lucky_items):
    print("Available items and their chances:")
    for item, chance in lucky_items.items():
        print(f"{item}: {chance}%")

def spin_once(lucky_items):
    items = list(lucky_items.keys())
    chances = [lucky_items[item] for item in items]
    result = random.choices(items, weights=chances, k=1)[0]
    return result

def spin_multiple(lucky_items, num_spins):
    items = list(lucky_items.keys())
    chances = [lucky_items[item] for item in items]
    results = random.choices(items, weights=chances, k=num_spins)
    return results

def update_yourstuff(your_stuff, items_spun):
    for item in items_spun:
        if item in your_stuff:
            your_stuff[item] += 1
        else:
            your_stuff[item] = 1
    save_yourstuff(your_stuff)

def display_summary(items_spun):
    summary = {}
    for item in items_spun:
        if item in summary:
            summary[item] += 1
        else:
            summary[item] = 1
    print("\nSummary of your spins:")
    for item, count in summary.items():
        print(f"{item}: {count}")

def display_inventory(your_stuff):
    if not your_stuff:
        print("Your inventory is empty.")
    else:
        print("Your inventory:")
        for item, count in your_stuff.items():
            print(f"{item}: {count}")

def main():
    lucky_items = load_lucky_items()
    your_stuff = load_or_create_yourstuff()

    print_item_chances(lucky_items)

    while True:
        user_input = input("\nPress 'e' to spin once, 'r' to spin 10 times, 'n' to choose number of spins, 'b' to check your items, or 's' to exit: ").lower()

        if user_input == 'e':
            result = spin_once(lucky_items)
            print(f"You got: {result}")
            update_yourstuff(your_stuff, [result])

        elif user_input == 'r':
            results = spin_multiple(lucky_items, 10)
            print("You got the following items:")
            for result in results:
                print(f"- {result}")
            update_yourstuff(your_stuff, results)

        elif user_input == 'n':
            try:
                num_spins = int(input("How many times would you like to spin? "))
                if num_spins <= 0:
                    print("Please enter a positive number.")
                    continue
                results = spin_multiple(lucky_items, num_spins)
                update_yourstuff(your_stuff, results)
                display_summary(results)
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        elif user_input == 'b':
            display_inventory(your_stuff)

        elif user_input == 's':
            print("Exiting the program...")
            break

        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
