from analyzer import analyze_password
from rich import print
from rich.panel import Panel
from rich.text import Text


def generate_recommendations(result):
    recommendations = []

    if result["score"] < 50:
        recommendations.append("Increase password length (at least 8 characters)")
        recommendations.append("Use a mix of uppercase, lowercase, numbers, and symbols")

    for issue in result["issues"]:
        if "common pattern" in issue:
            recommendations.append("Avoid common words and patterns (e.g., 'password', '1234')")

        if "sequential" in issue:
            recommendations.append("Avoid sequential characters (e.g., 'abcd', '1234')")

        if "keyboard" in issue:
            recommendations.append("Avoid keyboard patterns (e.g., 'qwerty')")

        if "predictable pattern" in issue:
            recommendations.append("Avoid predictable structures (e.g., word + numbers)")

        if "repeated" in issue:
            recommendations.append("Avoid repeated characters")

    return list(set(recommendations))


def get_strength_color(strength):
    if strength == "Very Weak":
        return "bold red"
    elif strength == "Weak":
        return "red"
    elif strength == "Moderate":
        return "yellow"
    elif strength == "Strong":
        return "green"
    else:
        return "bold green"


def main():
    print(Panel.fit("[bold cyan]Password Security Analyzer[/bold cyan]"))

    password = input("Enter password: ")

    result = analyze_password(password)
    recommendations = generate_recommendations(result)

    strength_color = get_strength_color(result["strength"])

    print("\n")
    
    score_text = Text()
    score_text.append(f"Score: {result['score']}/100\n", style="bold white")
    score_text.append(f"Strength: {result['strength']}\n", style=strength_color)
    score_text.append(f"Entropy: {result['entropy']} bits", style="cyan")

    print(Panel(score_text, title="Security Summary"))


    if result["issues"]:
        issues_text = "\n".join([f"- {issue}" for issue in result["issues"]])
        print(Panel(issues_text, title="[red]Risk Factors[/red]"))
    else:
        print(Panel("[green]No major issues detected[/green]", title="Risk Factors"))
   

    if recommendations:
        rec_text = "\n".join([f"- {rec}" for rec in recommendations])
        print(Panel(rec_text, title="[yellow]Recommendations[/yellow]"))
    else:
        print(Panel("[green]Strong password. No improvements needed[/green]", title="Recommendations"))


if __name__ == "__main__":
    main()
