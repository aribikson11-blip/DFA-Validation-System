
# DFA-Based Real-Time Validation Applications
# Course: Formal Language and Automata
# Assignment: Designing Automata for Real-Time Applications

# ------------------------------------------------
# 1. PASSWORD VERIFICATION USING DFA
# ------------------------------------------------

def password_validator(password):
    state = 0

    if len(password) < 8 or len(password) > 16:
        return False

    for ch in password:
        if ch.isupper():
            state |= 1
        elif ch.islower():
            state |= 2
        elif ch.isdigit():
            state |= 4
        elif ch in "@#$%&*!?":
            state |= 8
        else:
            return False

    # All four conditions must be satisfied
    return state == 15

# ------------------------------------------------
# 2. EMAIL FORMAT VALIDATION USING DFA
# ------------------------------------------------

def email_validator(email):

    if not email or email.count("@") != 1:
        return False

    local, domain = email.split("@")

    # Check local part
    if not local or local.startswith(".") or local.endswith("."):
        return False

    if ".." in local:
        return False

    allowed_local = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789._%+-"
    )

    for ch in local:
        if ch not in allowed_local:
            return False

    # Check domain
    if not domain or "." not in domain:
        return False

    labels = domain.split(".")

    for label in labels:
        if not label:
            return False

        if label.startswith("-") or label.endswith("-"):
            return False

        for ch in label:
            if not (ch.isalnum() or ch == "-"):
                return False

    # Top-level domain must contain at least 2 letters
    tld = labels[-1]

    if len(tld) < 2 or not tld.isalpha():
        return False

    return True

# ------------------------------------------------
# 3. ATM PIN VERIFICATION USING DFA
# ------------------------------------------------

def atm_pin_validator(pin):

    state = 0

    for ch in pin:

        if ch.isdigit():
            state += 1
        else:
            return False

    # ATM PIN must contain exactly 4 or 6 digits
    if state == 4 or state == 6:
        return True

    return False

# ------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------

while True:

    print("\n===================================")
    print("     DFA VALIDATION SYSTEM")
    print("===================================")

    print("1. Password Verification")
    print("2. Email Format Validation")
    print("3. ATM PIN Verification")
    print("4. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        password = input("Enter password: ")

        if password_validator(password):
            print("ACCEPTED: Valid Password")
        else:
            print("REJECTED: Invalid Password")

    elif choice == "2":

        email = input("Enter email address: ")

        if email_validator(email):
            print("ACCEPTED: Valid Email")
        else:
            print("REJECTED: Invalid Email")

    elif choice == "3":

        pin = input("Enter ATM PIN: ")

        if atm_pin_validator(pin):
            print("ACCEPTED: Valid ATM PIN")
        else:
            print("REJECTED: Invalid ATM PIN")

    elif choice == "4":

        print("Exiting Validation System...")
        break

    else:

        print("Invalid choice! Please try again.")
