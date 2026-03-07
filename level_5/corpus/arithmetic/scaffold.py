#!/usr/bin/env python3
"""
Builds the arithmetic corpus:

  tables/        — generated directly (no LLM needed)
    addition/      addition_table.corpus     (0+0 to 20+20)
    multiplication/ multiplication_table.corpus (1×1 to 12×12)
    division/      division_table.corpus     (all exact integer divisions up to 144)

  word_problems/ — prompts.txt files for generate.py
    addition_subtraction/
    multiplication_division/
    mixed_operations/
    fractions_basic/
    percentages/
    money/
    time_distance/
    area_perimeter/
"""

import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corpus")

# ---------------------------------------------------------------------------
# Format instructions embedded in every word-problem prompt
# ---------------------------------------------------------------------------

PROBLEM_FORMAT = (
    "Format each problem as exactly two lines, with a blank line between problems:\n"
    "Line 1: A natural language word problem with a JSON format instruction (style varies — see below)\n"
    "Line 2: { \"result\": <number> }\n\n"
    "Distribute these instruction styles across the 15 problems:\n\n"
    "Style A (~4 problems) — instruction at the END:\n"
    "<word problem>? Output in json, format { \"result\": number }\n"
    "Example: A baker makes 24 muffins and sells 9. How many muffins are left? Output in json, format { \"result\": number }\n"
    "{ \"result\": 15 }\n\n"
    "Style B (~4 problems) — instruction at the BEGINNING:\n"
    "Output in json, format { \"result\": number } — <word problem>?\n"
    "Example: Output in json, format { \"result\": number } — A store has 50 apples and receives 20 more. How many apples are there now?\n"
    "{ \"result\": 70 }\n\n"
    "Style C (~3 problems) — instruction in the MIDDLE (after the setup, before the question):\n"
    "<setup sentence>. Output in json, format { \"result\": number } <question>?\n"
    "Example: A train travels at 60 km/h for 3 hours. Output in json, format { \"result\": number } How many km did it travel?\n"
    "{ \"result\": 180 }\n\n"
    "Style D (~3 problems) — use an example value instead of the type name:\n"
    "<word problem>? Output in json, format { \"result\": 0 }\n"
    "Example: Maria has 30 stickers and gives 12 away. How many does she have left? Output in json, format { \"result\": 0 }\n"
    "{ \"result\": 18 }\n\n"
    "Style E (~1 problem) — only \"output in json\", no format hint:\n"
    "<word problem>? Output in json.\n"
    "Example: There are 8 rows of 6 chairs. How many chairs are there in total? Output in json.\n"
    "{ \"result\": 48 }\n\n"
    "Use varied real-world contexts (school, sports, cooking, shopping, travel, etc). "
    "Keep numbers realistic and small enough to be solved mentally (no calculators needed). "
    "Output only the problems — no titles, no commentary, no extra explanation."
)

# ---------------------------------------------------------------------------
# Word problem domains
# ---------------------------------------------------------------------------

WORD_PROBLEMS = {
    "addition_subtraction": [
        ("simple_sums.corpus",
         "Generate 15 arithmetic word problems using only addition and subtraction of whole numbers 1–100. "
         "Each problem has 1–2 steps. "
         "Example contexts: counting objects, combining groups, finding a difference. "
         + PROBLEM_FORMAT),
        ("multi_step_add_sub.corpus",
         "Generate 15 multi-step word problems that chain 3 or more addition and subtraction operations. "
         "Numbers stay in the range 1–500. "
         "Example contexts: budgets, inventories, scores across multiple rounds. "
         + PROBLEM_FORMAT),
    ],
    "multiplication_division": [
        ("simple_products.corpus",
         "Generate 15 word problems that each require one multiplication or one division of whole numbers. "
         "Multipliers and divisors in range 2–12. Products up to 144. "
         "Example contexts: rows of seats, packs of items, equal sharing, price per unit. "
         + PROBLEM_FORMAT),
        ("sharing_grouping.corpus",
         "Generate 15 word problems about equal sharing and grouping (division focus). "
         "All divisions are exact (no remainders). Dividends up to 200. "
         "Example contexts: distributing items, splitting costs, filling containers. "
         + PROBLEM_FORMAT),
    ],
    "mixed_operations": [
        ("two_operations.corpus",
         "Generate 15 word problems that each require exactly two different arithmetic operations "
         "(e.g. multiply then add, divide then subtract). "
         "Numbers in range 1–100. "
         "Example contexts: shopping totals with discounts, distance then remainder, combined groups. "
         + PROBLEM_FORMAT),
        ("three_operations.corpus",
         "Generate 15 word problems that each require three arithmetic operations. "
         "Keep intermediate values under 500. "
         "Example contexts: trip planning, multi-item purchases, event scheduling. "
         + PROBLEM_FORMAT),
    ],
    "fractions_basic": [
        ("half_quarters.corpus",
         "Generate 15 word problems involving halves and quarters only (1/2, 1/4, 3/4). "
         "All answers are whole numbers or simple decimals. "
         "Example contexts: cutting food, sharing equally, measuring ingredients. "
         + PROBLEM_FORMAT),
        ("simple_fractions.corpus",
         "Generate 15 word problems with simple fractions (1/3, 2/3, 1/5, 2/5, 3/5, 1/8). "
         "Answers are whole numbers or one-decimal numbers. "
         "Example contexts: portions, distances, time fractions. "
         + PROBLEM_FORMAT),
    ],
    "percentages": [
        ("percent_of.corpus",
         "Generate 15 word problems asking for a percentage of a whole number. "
         "Percentages: 10%, 20%, 25%, 50%, 75%. Numbers in range 10–200. "
         "Example contexts: discounts, tips, survey results, test scores. "
         + PROBLEM_FORMAT),
        ("percent_change.corpus",
         "Generate 15 word problems about percentage increase or decrease. "
         "Original values 10–200, changes of 10–50%. "
         "Example contexts: price changes, population growth, salary raises, temperature change. "
         + PROBLEM_FORMAT),
    ],
    "money": [
        ("prices_change.corpus",
         "Generate 15 word problems about paying for items and receiving change. "
         "Prices in dollars and cents (up to $50). Payment always sufficient. "
         "Example contexts: buying food, paying bus fare, purchasing school supplies. "
         + PROBLEM_FORMAT),
        ("totals_discounts.corpus",
         "Generate 15 word problems about shopping totals with discounts or taxes. "
         "Use whole-dollar discounts or round-percentage off. Totals under $200. "
         "Example contexts: grocery bills, sale prices, splitting a restaurant bill. "
         + PROBLEM_FORMAT),
    ],
    "time_distance": [
        ("speed_time.corpus",
         "Generate 15 word problems using distance = speed × time. "
         "Speeds 5–100 (km/h or mph), times 1–5 hours or 10–60 minutes. "
         "Example contexts: car trips, cycling, running races, train journeys. "
         + PROBLEM_FORMAT),
        ("duration_schedule.corpus",
         "Generate 15 word problems about elapsed time and schedules. "
         "Times expressed as hours and minutes (12-hour clock). "
         "Example contexts: school timetables, cooking durations, travel arrival times. "
         + PROBLEM_FORMAT),
    ],
    "area_perimeter": [
        ("rectangle_square.corpus",
         "Generate 15 word problems calculating area or perimeter of rectangles and squares. "
         "Side lengths 1–30. Some ask for area, some for perimeter, some for a missing side. "
         "Example contexts: garden beds, floor tiles, fencing, picture frames. "
         + PROBLEM_FORMAT),
        ("combined_shapes.corpus",
         "Generate 15 word problems involving two simple shapes combined or subtracted. "
         "Example: an L-shaped room, a path around a garden, two adjacent rectangles. "
         "Keep all dimensions as whole numbers under 20. "
         + PROBLEM_FORMAT),
    ],
}

# ---------------------------------------------------------------------------
# Table generators (pure Python, no LLM)
# ---------------------------------------------------------------------------

def write_addition_table(path: str) -> int:
    lines = []
    for a in range(0, 21):
        for b in range(0, 21):
            lines.append(f"{a} + {b} = {a + b}")
    content = "\n".join(lines) + "\n"
    with open(path, "w") as f:
        f.write(content)
    return len(lines)


def write_multiplication_table(path: str) -> int:
    lines = []
    for a in range(1, 13):
        for b in range(1, 13):
            lines.append(f"{a} × {b} = {a * b}")
    content = "\n".join(lines) + "\n"
    with open(path, "w") as f:
        f.write(content)
    return len(lines)


def write_division_table(path: str) -> int:
    lines = []
    for b in range(1, 13):
        for a in range(b, b * 13, b):
            lines.append(f"{a} ÷ {b} = {a // b}")
    content = "\n".join(lines) + "\n"
    with open(path, "w") as f:
        f.write(content)
    return len(lines)


def build_tables():
    table_specs = [
        ("addition",       "addition_table.corpus",       write_addition_table),
        ("multiplication", "multiplication_table.corpus", write_multiplication_table),
        ("division",       "division_table.corpus",       write_division_table),
    ]
    total_entries = 0
    for subdir, filename, writer in table_specs:
        dirpath = os.path.join(BASE, "tables", subdir)
        os.makedirs(dirpath, exist_ok=True)
        filepath = os.path.join(dirpath, filename)
        if os.path.exists(filepath):
            print(f"  tables/{subdir}/{filename} (already exists, skipping)")
            continue
        n = writer(filepath)
        total_entries += n
        print(f"  tables/{subdir}/{filename} ({n} entries written)")
    return total_entries


# ---------------------------------------------------------------------------
# Word problem prompts
# ---------------------------------------------------------------------------

def build_word_problem_prompts():
    total_dirs = 0
    total_prompts = 0
    for subdomain, angles in WORD_PROBLEMS.items():
        dirpath = os.path.join(BASE, "word_problems", subdomain)
        os.makedirs(dirpath, exist_ok=True)

        lines = []
        for filename, prompt in angles:
            prompt_oneline = prompt.replace("\n", " | ")
            lines.append(f"{filename} {prompt_oneline}")

        prompts_path = os.path.join(dirpath, "prompts.txt")
        with open(prompts_path, "w") as f:
            f.write("\n".join(lines) + "\n")

        total_dirs += 1
        total_prompts += len(lines)
        print(f"  word_problems/{subdomain}/prompts.txt ({len(lines)} prompts)")
    return total_dirs, total_prompts


def main():
    os.makedirs(BASE, exist_ok=True)

    print("Building arithmetic tables (no LLM)...")
    build_tables()

    print("\nBuilding word problem prompts...")
    dirs, prompts = build_word_problem_prompts()

    print(f"\nDone! {dirs} word-problem directories, {prompts} prompts.")
    print("Run generate.py to produce the word-problem corpus files.")


if __name__ == "__main__":
    main()
