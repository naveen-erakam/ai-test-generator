import json
import argparse
import os
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from groq import Groq

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system_prompt.txt"
OUTPUT_DIR  = Path(__file__).parent.parent / "output"


def load_system_prompt() -> str:
    with open(PROMPT_PATH, "r") as f:
        return f.read()


def generate_test_cases(feature_description: str) -> dict:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    system_prompt = load_system_prompt()
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate test cases for: {feature_description}"}
    ],
    temperature=0.3,
    max_tokens=2048,
    )
    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if Gemini wraps output
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


def display_results(result: dict):
    if not RICH_AVAILABLE:
        print(json.dumps(result, indent=2))
        return

    console = Console()
    console.print(f"\n[bold green]Feature:[/bold green] {result['feature']}")
    console.print(f"[bold]Total Test Cases Generated:[/bold] {result['total_cases']}\n")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID",       width=8)
    table.add_column("Title",    width=45)
    table.add_column("Type",     width=12)
    table.add_column("Priority", width=10)
    table.add_column("Tags",     width=20)

    type_colors = {"positive": "green", "negative": "red", "edge_case": "yellow"}

    for tc in result["test_cases"]:
        color = type_colors.get(tc["type"], "white")
        table.add_row(
            tc["id"],
            tc["title"],
            f"[{color}]{tc['type']}[/{color}]",
            tc["priority"],
            ", ".join(tc.get("tags", []))
        )

    console.print(table)


def save_output(result: dict, feature: str):
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name  = feature[:30].replace(" ", "_").lower()
    filename   = OUTPUT_DIR / f"testcases_{safe_name}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to: {filename}")
    return str(filename) 


def main():
    parser = argparse.ArgumentParser(description="AI Test Case Generator (Powered by Google Gemini)")
    parser.add_argument("--input", type=str, help="Feature description as text")
    parser.add_argument("--file",  type=str, help="Path to text file with feature description")
    parser.add_argument("--save",  action="store_true", help="Save output to JSON file")
    parser.add_argument("--excel", action="store_true", help="Export output to Excel file")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            feature_description = f.read()
    elif args.input:
        feature_description = args.input
    else:
        feature_description = input("Enter feature description: ")

    print(f"\nGenerating test cases for: {feature_description[:80]}...")
    result = generate_test_cases(feature_description)
    display_results(result)

    json_path = save_output(result, feature_description)

    if args.excel:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from export_excel import export_to_excel
        export_to_excel(json_path)


if __name__ == "__main__":
    main()
