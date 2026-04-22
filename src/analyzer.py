import re
import math

COMMON_PATTERNS = [
    "1234", "123456", "1234567890",
    "password", "qwerty", "admin", "letmein"
]

KEYBOARD_PATTERNS = [
    "qwerty", "asdfgh", "zxcvbn"
]


def estimate_entropy(password: str) -> float:
    charset_size = 0

    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"[0-9]", password):
        charset_size += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        charset_size += 32

    if charset_size == 0:
        return 0

    return len(password) * math.log2(charset_size)


def check_common_patterns(password: str):
    findings = []
    lower = password.lower()

    for pattern in COMMON_PATTERNS:
        if pattern in lower:
            findings.append(f"common pattern: {pattern}")

    return findings


def detect_keyboard_patterns(password: str):
    lower = password.lower()
    return any(pattern in lower for pattern in KEYBOARD_PATTERNS)


# ✅ NEW: STRUCTURE DETECTION (THIS WAS MISSING)
def detect_weak_structure(password: str):
    findings = []

    # letters + numbers (Meet123)
    if re.match(r"^[A-Za-z]+[0-9]+$", password):
        findings.append("predictable pattern: letters followed by numbers")

    # word + symbol + numbers (Meet@123)
    if re.match(r"^[A-Za-z]+[^A-Za-z0-9]+[0-9]+$", password):
        findings.append("predictable pattern: word + symbol + numbers")

    # repeated characters (aaa, 111)
    if re.search(r"(.)\1{2,}", password):
        findings.append("repeated characters detected")

    return findings


def classify_strength(score: int) -> str:
    if score <= 30:
        return "Very Weak"
    elif score <= 50:
        return "Weak"
    elif score <= 70:
        return "Moderate"
    elif score <= 85:
        return "Strong"
    else:
        return "Very Strong"
    
    
def detect_sequences(password: str):
    findings = []
    lower = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789"
    ]

    for seq in sequences:
        # check forward sequences
        for i in range(len(seq) - 3):
            pattern = seq[i:i+4]
            if pattern in lower:
                findings.append(f"sequential pattern detected: {pattern}")

        # check reverse sequences
        rev_seq = seq[::-1]
        for i in range(len(rev_seq) - 3):
            pattern = rev_seq[i:i+4]
            if pattern in lower:
                findings.append(f"reverse sequential pattern detected: {pattern}")

    return findings


def analyze_password(password: str):
    entropy = estimate_entropy(password)

    issues = check_common_patterns(password)
   
    if detect_keyboard_patterns(password):
        issues.append("keyboard pattern detected")
   
    structure_issues = detect_weak_structure(password)
    issues.extend(structure_issues)

    sequence_issues = detect_sequences(password)
    issues.extend(sequence_issues)


    score = 0

 
    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    else:
        score += 5


    if entropy > 60:
        score += 30
    elif entropy > 40:
        score += 20
    else:
        score += 10

    
    score -= len(issues) * 15

    
    score = max(0, min(score, 100))

    return {
        "score": score,
        "strength": classify_strength(score),
        "entropy": round(entropy, 2),
        "issues": issues
    }
