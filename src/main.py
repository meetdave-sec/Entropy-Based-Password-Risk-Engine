from analyzer import analyze_password


def main():
    print("\nPassword Security Analyzer\n")

    password = input("Enter password: ")

    result = analyze_password(password)

    print("\n=== Results ===")
    print(f"Score: {result['score']}/100")
    print(f"Strength: {result['strength']}")
    print(f"Entropy: {result['entropy']} bits")

    print("\n=== Analysis ===")

    if result["issues"]:
        print("Issues detected:")
        for issue in result["issues"]:
            print(f"- {issue}")
    else:
        print("No major issues detected.")


if __name__ == "__main__":
    main()
