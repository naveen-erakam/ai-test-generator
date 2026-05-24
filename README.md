# AI Test Case Generator

An AI-powered test case generation tool that takes a feature description or user story as input and outputs structured, ready-to-use test cases using the Claude API.

Built to reduce test-authoring time by automating the first-draft generation of test scenarios, including positive, negative, and edge cases.

## How It Works

```
Input: Feature description or user story (plain text)
         ↓
   AI analyses requirements
         ↓
Output: Structured test cases with steps, expected results, and tags
```

## Tech Stack

- **Python** 3.11+
- **Anthropic Claude API** (claude-sonnet)
- **Pytest** (for validating generated test structures)
- **Rich** (terminal output formatting)

## Project Structure

```
ai-test-generator/
├── generator/
│   ├── test_generator.py     # Core generation logic
│   └── parser.py             # Parses and structures AI output
├── prompts/
│   └── system_prompt.txt     # Prompt template for Claude
├── output/                   # Generated test cases saved here
├── examples/                 # Sample inputs and outputs
└── tests/                    # Unit tests for the generator itself
```

## Getting Started

### Prerequisites
```bash
pip install anthropic rich pytest
```

### Set your API key
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

### Run the generator
```bash
# Generate test cases from a feature description
python generator/test_generator.py --input "User can log in with email and password"

# Generate from a file
python generator/test_generator.py --file examples/sample_story.txt

# Save output to file
python generator/test_generator.py --input "Search functionality" --save
```

## Example Output

**Input:**
> "User can search for products by name and filter by category and price range"

**Generated Output:**
```
TC001 - Search with valid product name returns results     [positive]
TC002 - Search with partial name returns matching results  [positive]
TC003 - Search with no results shows empty state message   [negative]
TC004 - Filter by category narrows results correctly       [positive]
TC005 - Price range filter excludes out-of-range items     [positive]
TC006 - Combined name + category + price filter works      [edge case]
TC007 - Search with special characters handled gracefully  [edge case]
TC008 - Empty search field shows validation message        [negative]
```

## Use Cases

- Sprint planning: generate test cases from user stories before dev starts
- Exploratory testing: identify edge cases you might have missed
- Regression expansion: quickly create tests for new features

---
*Built and maintained by [Naveen Erakam](https://github.com/naveen-erakam)*
