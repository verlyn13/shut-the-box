import subprocess
from pathlib import Path

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "cli_golden_run_output.txt"
CLI_ARGS = [
    "python",
    "-m",
    "stbsim.cli",
    "--n-games",
    "100",
    "--p1-strategy",
    "greedy_max",
    "--p2-strategy",
    "min_tiles",
    "--seed",
    "42",
]


def extract_summary_block(output):
    """
    Extract the summary stats block from CLI output (from '==== Summary Stats ====' to the end of stats).
    """
    lines = output.splitlines()
    # Find the summary header
    try:
        start_idx = lines.index("==== Summary Stats ====")
    except ValueError as err:
        raise AssertionError(
            "Could not find the '==== Summary Stats ====' header in CLI output"
        ) from err
    # Collect lines until hitting an empty line or end
    summary = []
    for line in lines[start_idx:]:
        if line.strip() == "":
            break
        summary.append(line)
    return "\n".join(summary)


def test_cli_golden_run():
    """Checks just the summary block of stbsim CLI output for regressions."""
    result = subprocess.run(
        ["rye", "run"] + CLI_ARGS, capture_output=True, text=True, check=True
    )
    summary_out = extract_summary_block(result.stdout)
    expected = FIXTURE_PATH.read_text().strip()
    assert summary_out.strip() == expected, (
        "CLI summary block did not match golden fixture.\n"
        f"If this change is intentional, bless the new output by updating {FIXTURE_PATH}.\n"
        "Otherwise, review changes for regressions!"
    )
