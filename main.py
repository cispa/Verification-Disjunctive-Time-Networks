""" The main function simply executes the summary automaton computations as
    provided in the paper.

    By specifying the `--extended` flag, you can execute the MINREACH
    computation for even bigger examples.
"""

import time
import sys

from dtn.dtn_with_inv import DTNWithInv
from dtn.dtn_minus import DTNMinus
from examples.examples_dtns import gcs_3, gcs_4  # type: ignore
from examples.examples_minreach import star_4, star_5, star_6, star_7, star_8  # type: ignore


def main():
    print("Starting to execute benchmarks ...\n")

    print("Starting Summary Automaton benchmark ...")
    print("GCS(3) without invariants:")
    start_time = time.process_time()
    alg = DTNMinus(gcs_3)
    alg.get_summary_automaton()
    print("Computed summary automaton successfully.")
    print(f"Total CPU time: {time.process_time() - start_time}s\n")

    print("GCS(4) without invariants:")
    start_time = time.process_time()
    alg = DTNMinus(gcs_4)
    alg.get_summary_automaton()
    print("Computed summary automaton successfully.")
    print(f"Total CPU time: {time.process_time() - start_time}s\n")

    print("GCS(3) with invariants:")
    start_time = time.process_time()
    alg = DTNWithInv(gcs_3)
    print(f"Summary automaton is floodable: {alg.check_valid_summary_automaton()}")
    print(f"Total CPU time: {time.process_time() - start_time}s\n")

    print("GCS(4) with invariants:")
    start_time = time.process_time()
    alg = DTNWithInv(gcs_4)
    print(f"Summary automaton is floodable: {alg.check_valid_summary_automaton()}")
    print(f"Total CPU time: {time.process_time() - start_time}s\n")

    print("\n\n\n")

    print("Starting MinReach benchmark...")
    print("MinReach for Star(4):")
    start_time = time.process_time()
    alg = DTNMinus(star_4)
    alg.get_summary_automaton()
    alg.print_min_reach_times()
    print("Computed summary automaton successfully.")
    print(f"Total CPU time: {time.process_time() - start_time}s\n")

    print("MinReach for Star(5):")
    start_time = time.process_time()
    alg = DTNMinus(star_5)
    alg.get_summary_automaton()
    alg.print_min_reach_times()
    print("Computed summary automaton successfully.")
    print(f"Total CPU time: {time.process_time() - start_time}s\n")

    print("MinReach for Star(6)")
    start_time = time.process_time()
    alg = DTNMinus(star_6)
    alg.get_summary_automaton()
    alg.print_min_reach_times()
    print("Computed summary automaton successfully.")
    print(f"Total CPU time: {time.process_time() - start_time}s\n")

    if len(sys.argv) > 1 and sys.argv[1] == "--extended":
        print("MinReach for Star(7):")
        start_time = time.process_time()
        alg = DTNMinus(star_7)
        alg.get_summary_automaton()
        print("Computed summary automaton successfully.")
        print(f"Total CPU time: {time.process_time() - start_time}s\n")

        print("MinReach for Star(8):")
        start_time = time.process_time()
        alg = DTNMinus(star_8)
        alg.get_summary_automaton()
        print("Computed summary automaton successfully.")
        print(f"Total CPU time: {time.process_time() - start_time}s\n")


if __name__ == "__main__":
    main()
