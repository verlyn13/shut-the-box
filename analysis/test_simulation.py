#!/usr/bin/env python3
"""
Simple test to verify simulation works and generate basic output
"""

import sys
import os

# Add the stbsim source to Python path
project_root = "/home/verlyn13/Projects/shut-the-box/shut_the_box_sim"
sys.path.insert(0, os.path.join(project_root, "src"))

# Test import and basic functionality
try:
    from stbsim.simulation import Simulation
    from stbsim.strategies import STRATEGY_MAP

    print("✓ stbsim imports successful")

    # Test basic simulation
    sim = Simulation()
    results = sim.run(
        n_games=10, p1_strategy="greedy_max", p2_strategy="min_tiles", seed_start=42
    )

    print(f"✓ Simulation completed: {len(results)} games")
    print(f"✓ Available strategies: {list(STRATEGY_MAP.keys())}")

    # Basic analysis
    p1_wins = sum(1 for r in results if r["winner"] == "P1")
    p2_wins = sum(1 for r in results if r["winner"] == "P2")
    shut_boxes = sum(1 for r in results if r["shut_box"])

    avg_p1_score = sum(r["p1_score"] for r in results) / len(results)
    avg_p2_score = sum(r["p2_score"] for r in results) / len(results)

    print("\nBasic Results (10 games):")
    print(f"  P1 (greedy_max) wins: {p1_wins}")
    print(f"  P2 (min_tiles) wins: {p2_wins}")
    print(f"  Shut boxes: {shut_boxes}")
    print(f"  Avg P1 score: {avg_p1_score:.2f}")
    print(f"  Avg P2 score: {avg_p2_score:.2f}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback

    traceback.print_exc()
