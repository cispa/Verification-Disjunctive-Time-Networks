from tn.dtn_with_inv import *
from tn.dtn_minus import *
from examples.example_tns import *
from examples.minreach_examples import *
import time
import sys


def main():
    print("Starting to execute benchmarks ...\n")

    print("Starting Summary Automaton benchmark ...")
    print("GCS(3) without invariants:")
    start_time = time.process_time()
    alg = DTNMinus(gcs_3)
    alg.get_summary_automaton()
    print("Computed summary automaton successfully.")
    print("Total CPU time: {}s\n".format(time.process_time() - start_time))

    print("GCS(4) without invariants:")
    start_time = time.process_time()
    alg = DTNMinus(gcs_4)
    alg.get_summary_automaton()
    print("Computed summary automaton successfully.")
    print("Total CPU time: {}s\n".format(time.process_time() - start_time))

    print("GCS(3) with invariants:")
    start_time = time.process_time()
    alg = DTNWithInv(gcs_3)
    print("Summary automaton is floodable: {}".format(
        alg.check_valid_summary_automaton()))
    print("Total CPU time: {}s\n".format(time.process_time() - start_time))

    print("GCS(4) with invariants:")
    start_time = time.process_time()
    alg = DTNWithInv(gcs_4)
    print("Summary automaton is floodable: {}".format(
        alg.check_valid_summary_automaton()))
    print("Total CPU time: {}s\n".format(time.process_time() - start_time))

    print("\n\n\n")

    print("Starting MinReach benchmark...")
    print("MinReach for Star(4):")
    start_time = time.process_time()
    alg = DTNMinus(star_4)
    alg.get_summary_automaton()
    print("Computed summary automaton successfully.")
    print("Total CPU time: {}s\n".format(time.process_time() - start_time))

    print("MinReach for Star(5):")
    start_time = time.process_time()
    alg = DTNMinus(star_5)
    alg.get_summary_automaton()
    print("Computed summary automaton successfully.")
    print("Total CPU time: {}s\n".format(time.process_time() - start_time))

    print("MinReach for Star(6)")
    start_time = time.process_time()
    alg = DTNMinus(star_6)
    alg.get_summary_automaton()
    print("Computed summary automaton successfully.")
    print("Total CPU time: {}s\n".format(time.process_time() - start_time))

    if len(sys.argv) > 1 and sys.argv[1] == "--extended":
        print("MinReach for Star(7):")
        start_time = time.process_time()
        alg = DTNMinus(star_7)
        alg.get_summary_automaton()
        print("Computed summary automaton successfully.")
        print("Total CPU time: {}s\n".format(time.process_time() - start_time))

        print("MinReach for Star(8):")
        start_time = time.process_time()
        alg = DTNMinus(star_8)
        alg.get_summary_automaton()
        print("Computed summary automaton successfully.")
        print("Total CPU time: {}s\n".format(time.process_time() - start_time))


if __name__ == "__main__":

    main()
