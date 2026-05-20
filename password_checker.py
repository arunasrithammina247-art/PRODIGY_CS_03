import re
import math
import hashlib
import secrets
import string
import time
import json
from getpass import getpass
from datetime import datetime


# =========================================================
# ULTRA ADVANCED PASSWORD SECURITY ANALYZER
# PRODIGY CS TASK-03
# =========================================================


class PasswordSecurityAnalyzer:

    def __init__(self):

        self.common_passwords = {
            "password", "123456", "123456789", "qwerty",
            "abc123", "password123", "admin", "welcome",
            "letmein", "dragon", "football", "monkey",
            "shadow", "master", "superman"
        }

        self.keyboard_patterns = [
            "qwerty", "asdfgh", "zxcvbn",
            "123456", "987654", "abcdef"
        ]

    # =====================================================
    # PASSWORD ENTROPY
    # =====================================================

    def calculate_entropy(self, password):

        charset = 0

        if re.search(r'[a-z]', password):
            charset += 26

        if re.search(r'[A-Z]', password):
            charset += 26

        if re.search(r'[0-9]', password):
            charset += 10

        if re.search(r'[^A-Za-z0-9]', password):
            charset += 32

        if charset == 0:
            return 0

        entropy = len(password) * math.log2(charset)

        return round(entropy, 2)

    # =====================================================
    # CRACK TIME ESTIMATION
    # =====================================================

    def estimate_crack_time(self, entropy):

        guesses_per_second = 1e12

        seconds = (2 ** entropy) / guesses_per_second

        units = [
            ("seconds", 60),
            ("minutes", 60),
            ("hours", 24),
            ("days", 365),
            ("years", 1000)
        ]

        value = seconds

        for unit, limit in units:

            if value < limit:
                return f"{value:.2f} {unit}"

            value /= limit

        return f"{value:.2f} millennia"

    # =====================================================
    # PATTERN DETECTION
    # =====================================================

    def detect_patterns(self, password):

        warnings = []

        # Sequential Pattern
        sequences = [
            "abcdefghijklmnopqrstuvwxyz",
            "0123456789"
        ]

        password_lower = password.lower()

        for seq in sequences:
            for i in range(len(seq) - 2):

                if seq[i:i+3] in password_lower:
                    warnings.append(
                        "Sequential characters detected"
                    )
                    break

        # Keyboard Pattern
        for pattern in self.keyboard_patterns:

            if pattern in password_lower:
                warnings.append(
                    "Keyboard pattern detected"
                )

        # Repeated Characters
        if re.search(r'(.)\1{2,}', password):
            warnings.append(
                "Repeated characters detected"
            )

        return warnings

    # =====================================================
    # PASSWORD SCORING
    # =====================================================

    def score_password(self, password):

        score = 0
        feedback = []

        # Length Analysis
        if len(password) >= 20:
            score += 4

        elif len(password) >= 16:
            score += 3

        elif len(password) >= 12:
            score += 2

        elif len(password) >= 8:
            score += 1

        else:
            feedback.append(
                "Password should be at least 12 characters"
            )

        # Character Variety
        checks = {
            "uppercase": r'[A-Z]',
            "lowercase": r'[a-z]',
            "numbers": r'[0-9]',
            "special": r'[^A-Za-z0-9]'
        }

        for name, pattern in checks.items():

            if re.search(pattern, password):
                score += 1

            else:
                feedback.append(
                    f"Add {name} characters"
                )

        # Common Password
        if password.lower() in self.common_passwords:
            feedback.append(
                "Common password detected"
            )
            score = 0

        # Pattern Detection
        patterns = self.detect_patterns(password)

        if patterns:
            score -= len(patterns)
            feedback.extend(patterns)

        # Bonus Entropy Score
        entropy = self.calculate_entropy(password)

        if entropy > 80:
            score += 3

        elif entropy > 60:
            score += 2

        elif entropy > 40:
            score += 1

        # Final Strength
        if score >= 10:
            strength = "MILITARY GRADE"

        elif score >= 8:
            strength = "VERY STRONG"

        elif score >= 6:
            strength = "STRONG"

        elif score >= 4:
            strength = "MEDIUM"

        else:
            strength = "WEAK"

        return strength, score, feedback, entropy

    # =====================================================
    # PASSWORD HASHING
    # =====================================================

    def generate_hashes(self, password):

        hashes = {
            "MD5":
                hashlib.md5(
                    password.encode()
                ).hexdigest(),

            "SHA1":
                hashlib.sha1(
                    password.encode()
                ).hexdigest(),

            "SHA256":
                hashlib.sha256(
                    password.encode()
                ).hexdigest(),

            "SHA512":
                hashlib.sha512(
                    password.encode()
                ).hexdigest()
        }

        return hashes

    # =====================================================
    # PASSWORD GENERATOR
    # =====================================================

    def generate_secure_password(self, length=20):

        chars = (
            string.ascii_letters +
            string.digits +
            string.punctuation
        )

        password = ''.join(
            secrets.choice(chars)
            for _ in range(length)
        )

        return password

    # =====================================================
    # COMPLETE ANALYSIS
    # =====================================================

    def analyze(self, password):

        strength, score, feedback, entropy = \
            self.score_password(password)

        crack_time = \
            self.estimate_crack_time(entropy)

        hashes = \
            self.generate_hashes(password)

        report = {
            "timestamp":
                str(datetime.now()),

            "password_length":
                len(password),

            "strength":
                strength,

            "security_score":
                score,

            "entropy_bits":
                entropy,

            "estimated_crack_time":
                crack_time,

            "feedback":
                feedback,

            "hashes":
                hashes
        }

        return report

    # =====================================================
    # SAVE REPORT
    # =====================================================

    def save_report(self, report):

        filename = "security_report.json"

        with open(filename, "w") as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return filename


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():

    analyzer = PasswordSecurityAnalyzer()

    print("=" * 70)
    print("      ULTRA ADVANCED PASSWORD SECURITY ANALYZER")
    print("=" * 70)

    print("\n1. Analyze Password")
    print("2. Generate Secure Password")

    choice = input("\nSelect option (1/2): ")

    # =====================================================
    # ANALYZE PASSWORD
    # =====================================================

    if choice == "1":

        password = getpass(
            "\nEnter password for analysis: "
        )

        print("\nAnalyzing Password Security...")
        time.sleep(2)

        report = analyzer.analyze(password)

        print("\n" + "=" * 70)
        print("SECURITY ANALYSIS REPORT")
        print("=" * 70)

        print(f"\nPassword Length     : "
              f"{report['password_length']}")

        print(f"Security Strength   : "
              f"{report['strength']}")

        print(f"Security Score      : "
              f"{report['security_score']}")

        print(f"Entropy             : "
              f"{report['entropy_bits']} bits")

        print(f"Estimated Crack Time: "
              f"{report['estimated_crack_time']}")

        print("\nPASSWORD HASHES")

        for algo, value in report["hashes"].items():

            print(f"\n{algo}:")
            print(value)

        if report["feedback"]:

            print("\nSECURITY WARNINGS")

            for item in report["feedback"]:
                print(f"[-] {item}")

        else:
            print("\n[+] No security issues detected")

        saved_file = analyzer.save_report(report)

        print(f"\n[+] Report saved as: {saved_file}")

    # =====================================================
    # GENERATE PASSWORD
    # =====================================================

    elif choice == "2":

        length = int(
            input("\nEnter password length: ")
        )

        generated = analyzer.generate_secure_password(
            length
        )

        print("\nGenerated Secure Password:")
        print(generated)

    else:
        print("\nInvalid option selected")


# =========================================================
# DRIVER CODE
# =========================================================

if __name__ == "__main__":
    main()