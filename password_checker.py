import re
import math


def calculate_entropy(password):
    charset = 0

    if re.search(r'[a-z]', password):
        charset += 26

    if re.search(r'[A-Z]', password):
        charset += 26

    if re.search(r'[0-9]', password):
        charset += 10

    if re.search(r'[^A-Za-z0-9]', password):
        charset += 32

    entropy = len(password) * math.log2(charset) if charset else 0

    return round(entropy, 2)


common_passwords = [
    "password",
    "123456",
    "qwerty",
    "admin",
    "welcome",
    "abc123"
]


def check_password_strength(password):

    score = 0
    feedback = []

    # Length Check
    if len(password) >= 12:
        score += 2

    elif len(password) >= 8:
        score += 1

    else:
        feedback.append("Password should be at least 8 characters long")

    # Uppercase Check
    if re.search(r'[A-Z]', password):
        score += 1

    else:
        feedback.append("Add at least one uppercase letter")

    # Lowercase Check
    if re.search(r'[a-z]', password):
        score += 1

    else:
        feedback.append("Add at least one lowercase letter")

    # Number Check
    if re.search(r'[0-9]', password):
        score += 1

    else:
        feedback.append("Add at least one number")

    # Special Character Check
    if re.search(r'[^A-Za-z0-9]', password):
        score += 2

    else:
        feedback.append("Add at least one special character")

    # Common Password Check
    if password.lower() in common_passwords:
        feedback.append("This password is too common")
        score = 0

    # Calculate Entropy
    entropy = calculate_entropy(password)

    # Strength Levels
    if score >= 7:
        strength = "Very Strong"

    elif score >= 5:
        strength = "Strong"

    elif score >= 3:
        strength = "Medium"

    else:
        strength = "Weak"

    return strength, entropy, feedback


print("=== Advanced Password Complexity Checker ===")

password = input("Enter your password: ")

strength, entropy, feedback = check_password_strength(password)

print("\nPassword Strength:", strength)
print("Password Entropy:", entropy, "bits")

if feedback:
    print("\nSuggestions to Improve Password:")

    for item in feedback:
        print("-", item)

else:
    print("\nExcellent Password!")