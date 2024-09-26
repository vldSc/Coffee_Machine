from art import coffee as logo
from data import MENU, resources, action, word
from replit import clear
import sys
import time

total_money_client = 0
total_profit = 0
refill = 0


def clear_sceen_print_logo():
    clear()
    print(logo)


def loading_animation(duration=3):
    animation = "|/-\\"
    idx = 0

    print("Loading", end="")
    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(0.1)
        sys.stdout.write(f'\rLoading {animation[idx % len(animation)]}')
        sys.stdout.flush()
        idx += 1
    sys.stdout.write('\rLoading complete!   \n')


def remove_spaces(respond):
    if " " in respond:
        respond = respond.replace(" ", "")
    return respond


def validate(respond, validate_list):
    if respond in validate_list:
        return True
    else:
        print("\nOpss! You choose an invalid option! Try again!")
        return False


def get_drink(drink):
    drinks = {
        "1": "espresso",
        "2": "latte",
        "3": "cappuccino"
    }
    return drinks.get(drink)


def check_resources(drink):
    little_resources = []
    for ingredient in resources:
        if ingredient not in MENU[drink]["ingredients"]:
            resources[ingredient] = resources[ingredient]
        else:
            if resources[ingredient] < MENU[drink]["ingredients"][ingredient]:
                little_resources.append(ingredient)
    if len(little_resources) > 0:
        print(
            f"\nSorry there is not enough {', '.join(little_resources)}! The Money has been returned.")
        return False
    else:
        return True


def restart_machine():
    global resources
    global refill
    clear_sceen_print_logo()
    resources = {
        "water": 300,
        "milk": 200,
        "coffee": 100,
    }
    loading_animation()

    print("\nResources have been refilled!")
    input("Please press Enter.")
    refill += 1
    clear_sceen_print_logo()


def is_number(n):
    try:
        n = int(n)
        return True, n
    except:
        print("Please, insert an number!")
        return False, None


def get_money():
    global total_money_client
    total_money_client = 0
    coins = {
        "dimes": 0.10,
        "quarters": 0.25,
        "half dollars": 0.50
    }

    print("\nPlease insert coins.")
    for coin in coins:
        is_money = False
        while not is_money:
            total = input(f"How many {coin}: ")
            is_money, total = is_number(total)

        total_money_client += total * coins[coin]
    return total_money_client


def enouth_money(money, drink):
    if money < MENU[drink]["cost"]:
        loading_animation()
        print(f"Insufficient funds. The Money has been returned.")
        while True:
            again_money = input(
                "Do you want to try again? Type 'y' or 'n': ").lower()
            if validate(again_money, ["y", "n"]):
                if again_money == "y":
                    money = get_money()
                    enouth_money(money, drink)
                    return True
                else:
                    return False
    elif money > MENU[drink]["cost"]:
        loading_animation()
        change = "{:.2f}".format(money - MENU[drink]["cost"])
        print(f"Here is your change: ${change} ")
        return True
    else:
        return True


def display_resources():
    for ingredient in resources:
        print(ingredient, resources[ingredient])
    print(f"Money: ${total_profit}")
    print(f"Number of refills: {refill}")
    input("Please press Enter.")


def report():
    while True:
        report = input(
            "\nDo you want to see the report of resources? Type 'y' or 'n': ").lower()
        report = remove_spaces(report)
        if validate(report, ["y", "n"]):
            if report == "y":
                if get_password(3):
                    display_resources()
                    break
            else:
                break
        else:
            break


def make_drink(drink):
    global total_money_client
    global total_profit
    drink = get_drink(drink)
    print(f"Your {drink} costs ${MENU[drink]['cost']}")
    money = get_money()
    if enouth_money(money, drink):
        if check_resources(drink):
            for ingredient in resources:
                if ingredient not in MENU[drink]["ingredients"]:
                    resources[ingredient] = resources[ingredient]
                else:
                    resources[ingredient] = resources[ingredient] - \
                        MENU[drink]["ingredients"][ingredient]
            print("")
            total_profit += MENU[drink]['cost']
            loading_animation()
            print(f"Enjoy your {drink}!")
        else:
            total_money_client = 0
            report()
            while True:
                restart = input(
                    "\nDo you want to refill the resources? Type 'y' or 'n': ").lower()
                restart = remove_spaces(restart)
                if validate(restart, ["y", "n"]):
                    if get_password(2):
                        restart_machine()
                        break


def turn_off():
    while True:
        answer = input(
            "\nWould you like to turn off the machine? Type 'y' for yes or 'n' for no: ").lower()
        answer = remove_spaces(answer)
        if validate(answer, ["y", "n"]):
            return answer == "y"


def get_password(n):
    while True:
        password = input(
            f"Please enter the seret word to {action.get(n)} the machine: ").lower()
        password = remove_spaces(password)
        if validate(password, [word.get(n)]):
            return True
        else:
            while True:
                ch = input(
                    "Do you want to try again? Type 'y' or 'n': ").lower()
                ch = remove_spaces(ch)
                if validate(ch, ["y", "n"]):
                    if ch == "y":
                        get_password(n)
                    else:
                        return False


def coffee_machien():
    while True:
        clear_sceen_print_logo()

        while True:
            drink = input(
                "\nWhat would you like (espresso/latte/cappuccino)?\n Type 1 for espresso, 2 for latte or 3 for cappucino: ").lower()
            drink = remove_spaces(drink)
            if validate(drink, ["1", "2", "3"]):
                break

        make_drink(drink)

        if turn_off():
            report()
            if get_password(1):
                clear_sceen_print_logo()
                loading_animation()
                print("\nMachine is off!\nSee you next time!")
                break


coffee_machien()
