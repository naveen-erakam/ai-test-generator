# AI Test Case Generator

An AI-powered test case generation tool that takes a feature description or user story
and outputs structured, ready-to-use test cases using Google Gemini (free).

## How It Works

```
Input: Feature description or user story (plain text)
         |
   Gemini AI analyses requirements
         |
Output: Structured test cases with steps, expected results, priority, and tags
```

## Tech Stack

- **Python** 3.11+
- **Google Gemini API** (free — no credit card required)
- **Rich** (beautiful terminal output)
- **Pytest** (for validating generator logic)

## Project Structure

```
ai-test-generator/
├── generator/
│   ├── test_generator.py     # Core generation logic (Gemini API)
│   └── parser.py             # Converts output to Robot Framework / Pytest format
├── prompts/
│   └── system_prompt.txt     # Prompt template sent to Gemini
├── output/                   # Generated test cases saved here (gitignored)
├── examples/
│   └── sample_story.txt      # Sample user story input
├── .env.example              # Template for your API key
└── requirements.txt
```

## Getting Started

### Step 1 - Get your FREE Gemini API key
1. Go to **https://aistudio.google.com**
2. Sign in with your Google account
3. Click **"Get API Key"** -> **"Create API key"**
4. Copy the key

### Step 2 - Set up the project
```bash
# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Open .env and paste your Gemini API key
```

### Step 3 - Run the generator
```bash
# From a feature description
python generator/test_generator.py --input "User can log in with email and password"

# From a file
python generator/test_generator.py --file examples/sample_story.txt

# Save output to JSON
python generator/test_generator.py --input "Search functionality" --save
```

## Example Output

**Input:**
> "User can search for products by name and filter by category and price range"

**Generated Output:**
```
TC001 - Search with valid product name returns results       [positive]  [high]
TC002 - Search with partial name returns matching results    [positive]  [medium]
TC003 - Search with no results shows empty state message     [negative]  [high]
TC004 - Filter by category narrows results correctly         [positive]  [high]
TC005 - Price range filter excludes out-of-range items       [positive]  [medium]
TC006 - Combined name + category + price filter works        [edge_case] [high]
TC007 - Search with special characters handled gracefully    [edge_case] [medium]
TC008 - Empty search field shows validation message          [negative]  [high]
```

## Use Cases

- **Sprint planning** — generate test cases from user stories before dev starts
- **Edge case discovery** — find scenarios you might have missed
- **Regression expansion** — quickly create tests for new features

## Security Note

Never commit your `.env` file. It is already listed in `.gitignore`.

---
*Built and maintained by [Naveen Erakam](https://github.com/naveen-erakam)*
