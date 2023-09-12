# Parameterized Verification of Disjunctive Timed Networks

This project implements new techniques for the parameterized verification of
disjunctive timed networks ($DTN$). A detailed explanation of the main ideas and
formal correctness arguments are provided in the corresponding
[paper](http://arxiv.org/abs/2305.07295).

This repository contains an implementation which, for a $DTN$ given in the form
of a single guarded Timed Automaton (gTA) with a single clock, will compute a
**Summary Automaton**. This summary automaton is proven in the paper to be
language equivalent to the $DTN$ it represents (under certain conditions).
Hence, it can be used to verify properties of the $DTN$ instead of the product
system.

The summary automaton approach is sound and complete for $DTNs$ falling into the
$DTN^-$ class, i.e., locations that appear as a location guard cannot have a
location invariant. If this is not the case, i.e., a location appears as a
location guard with an invariant, the summary automaton will only be sound
if a flooding path exists for all of these locations.

This implementation will also check for the existence of flooding paths if the
check succeeds. The summary automaton can then be used to verify properties of
the $DTN$.

As of now, the project is in a **prototype state**. More specifically it
currently does not support:

- parsing an input file of any kind. Instead, a user will have to manually
  encode the automaton into the project's Python representation (see
  [input format](#input-format)).

- checking arbitrary properties, only reachability is supported directly. If a
  user wants to verify other system properties, she can do so by
  encoding the summary automaton into a different tool supporting verification
  timed automata, e.g., [UPPAAL](https://uppaal.org/).

- output of a summary automaton in a comprehensible format. Currently, summary
  automata are represented in the internal Python format. A user needs to
  manually encode them into, for example, the [UPPAAL](https://uppaal.org/)
  format if she wants to check advanced properties of a system.

## Setup

### Requirements

This project can be run locally on your machine ([see](#local)) or using the provided
Docker image ([see](#docker)).

Note however, that the project currently can only be used to calculate minimal
reachability times and check for the existence of lassos.

To check the properties described in the paper benchmark section, you must
install [UPPAAL](https://uppaal.org/downloads/).
Note that you will have to download and install UPPAAL yourself. We cannot
distribute it nor include it in our Dockerfiles. Please follow the instructions
on the [UPPAAL website](https://uppaal.org/downloads/).

For the benchmarks presented in the paper [UPPAAL](https://uppaal.org/) version
`4.1.26-1` has been used.

We will describe how to reproduce the results from the paper in the
[benchmark section](#benchmarks).

### Local

This project only requires Python `>=3.9`, all other modules are included or
part of the Python standard library. To execute the program, use:

```bash
python3 main.py
```

### Docker

Alternatively, you can also use the provided Dockerfile. To execute the image,
use:

```bash
docker run ghcr.io/cispa/verification-disjunctive-time-networks:latest
```

By default, it will execute the benchmarks described in the paper and output
the runtime statistics along with the minimal reach times for each state. 
If you would like to instead experiment with the program interactively, you can 
also use:

```bash
docker run --entrypoint python -it ghcr.io/cispa/verification-disjunctive-time-networks:latest
```

to start an interactive Python shell running in the container. You can then, for
example, execute the main function using:

```python
exec(open("main.py").read())
```

## Benchmarks

The paper presents a small benchmark suite consisting of two benchmark suits:

- **MINREACH Benchmarks**: The first suite demonstrates the effectiveness of
  our $MINREACH$ algorithm for computing. More details can be found in the
  [$MINREACH$](#minreach) section.

- **Summary Automaton**: This set of benchmarks demonstrates the speedup that
  can be gained by first constructing a summary automaton and then checking
  properties using this automaton instead of constructing the full cutoff
  system. More details can be found in section
  [Summary Automaton](#summary-automaton).

For all benchmarks, we already include the translations to UPPAAL, including the
summary automaton's encoding. Those files can be found in the
[`benchmarks`](./benchmarks/) directory. The next section will outline how to
use those files.

### Using the UPPAAL files

After installing [UPPAAL](https://uppaal.org/), the simplest way to execute any
benchmark is to use:

```bash
verifyta -u -s <path-to-uppaal-xml-file>
```

This will automatically execute the property checks as described for the
individual benchmarks.

### MINREACH

When executing `main.py` it will first print the statistics for checking minimal
reachability times with the algorithm described in the paper for the systems

| System  | UPPAAL Cutoff Encoding                         | Python Encoding                                         |
| ------- | ---------------------------------------------- | ------------------------------------------------------- |
| Star(4) | [star_4.xml](./benchmarks/minreach/star_4.xml) | [examples_minreach.py](./examples/examples_minreach.py) |
| Star(5) | [star_5.xml](./benchmarks/minreach/star_5.xml) | [examples_minreach.py](./examples/examples_minreach.py) |
| Star(6) | [star_6.xml](./benchmarks/minreach/star_6.xml) | [examples_minreach.py](./examples/examples_minreach.py) |

To check the same properties in the cutoff system use UPPAAL with the
accordingly named files provided in
[`./benchmarks/minreach`](./benchmarks/minreach/).

### Summary Automaton

The next part of the output of `main.py` will be statistics for the summary
automaton construction for the systems

| System                    | UPPAAL Cutoff Encoding                                                                                    | UPPAAL Summary Automaton Encoding                                                                               | Python Encoding                                 |
| ------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| GCS(3) without invariants | [gcs_3_without_invariants_cutoff.xml](./benchmarks/summary-automaton/gcs_3_without_invariants_cutoff.xml) | [gcs_3_without_invariants_summaryAT.xml](./benchmarks/summary-automaton/gcs_3_without_invariants_summaryAT.xml) | [examples_dtns.py](./examples/examples_dtns.py) |
| GCS(3) with invariants    | [gcs_3_with_invariants_cutoff.xml](./benchmarks/summary-automaton/gcs_3_with_invariants_cutoff.xml)       | [gcs_3_with_invariants_summaryAT.xml](./benchmarks/summary-automaton/gcs_3_with_invariants_summaryAT.xml)       | [examples_dtns.py](./examples/examples_dtns.py) |
| GCS(4) without invariants | [gcs_4_without_invariants_cutoff.xml](./benchmarks/summary-automaton/gcs_4_without_invariants_cutoff.xml) | [gcs_4_without_invariants_summaryAT.xml](./benchmarks/summary-automaton/gcs_4_without_invariants_summaryAT.xml) | [examples_dtns.py](./examples/examples_dtns.py) |
| GCS(4) with invariants    | [gcs_4_with_invariants_cutoff.xml](./benchmarks/summary-automaton/gcs_4_with_invariants_cutoff.xml)       | [gcs_4_with_invariants_summaryAT.xml](./benchmarks/summary-automaton/gcs_4_with_invariants_summaryAT.xml)       | [examples_dtns.py](./examples/examples_dtns.py) |

To compare the time it takes to check the properties $\phi_1,\phi_2, \phi_3, 
\phi_4, \phi_5$ when constructing the cutoff system and using the summary
automaton check the files as listed in the table above with UPPAAL.

## Code

This section serves as a very brief introduction to the code and the current
input format. This can be useful if you would like to construct summary automata
for your own examples or reuse parts of the program.

### Input Format

Currently, the gTA definition must be manually encoded into a
`Dict`-based representation. Some examples can be found in
[`./examples/example_dtns.py`](./examples/example_dtns.py). We will explain the
input in the following section. A gTA consist of:

- A set of locations, encoded as a list of strings:

  ```python
  locations = ["q1", "q2", "q3", "q4"]
  ```

- A set of initial states, encoded as a list of strings:

  ```python
  init_states = ["q1"]
  ```

- Invariants on states, encoded as a Dict mapping from state names to
  `Constraints`:

  ```python
  invariants = {
                "q1": Constraint("x", "0", Bound.less_equal(1)),
                "q2": Constraint("y", "0", Bound.unbounded()),
                "q3": Constraint("x", "0", Bound.unbounded()),
                "q4": Constraint("x", "0", Bound.unbounded())
            }
  ```

  A `Constraint` is a limit on the difference between clocks, e.g. the first
  constraint requires the difference between the clock `x` and the constantly
  zero clock `0` to be $\leq 1$. A `Constraint` with an unbounded `Bound`, i.e.
  $< \infty$, does not limit the clock valuations. This representation has been
  designed with Difference Bound Matrices (DBMs) in mind, as they are used in
  the underlying zone graph exploration. More details can be found in the
  [paper](http://arxiv.org/abs/2305.07295).

- Transitions, encoded as a `Dict` mapping from transition names to the
  following entries:

  - `source_loc`: the source location of the transition
  - `clock_guard`: The clock guard guarding the transition, which needs to be
    fulfilled to take this transition. Represented as a list of `Constraints`.
  - `reset_clocks`: The clocks reset when taking the transition are represented
    as a list of strings.
  - `loc_guard`: The location guard of the transition, represented as a list
    of strings. Another process must be in this location in order to take
    this transition. If this is a disjunction, it can be represented by creating
    multiple transitions with the different location guards.
  - `target_loc`: The target location of this transition.

  ```python
    transitions = to_gta_transitions({
            "t1": {
                "source_loc": "q1",
                "clock_guard": [Constraint("0", "x", Bound.less_equal(-1))],
                "reset_clocks": ["x"],
                "loc_guard": "empty",
                "target_loc": "q1"
            },
            "t2": {
                "source_loc": "q1",
                "clock_guard": [Constraint("0", "y", Bound.less_equal(-5))],
                "reset_clocks": ["y"],
                "loc_guard": "empty",
                "target_loc": "q2"
            },
            "t3": {
                "source_loc": "q1",
                "clock_guard": [Constraint("y", "0", Bound.unbounded())],
                "reset_clocks": [],
                "loc_guard": "q2",
                "target_loc": "q3"
            }
        })
  ```

  To convert this representation into the internal transition type use the
  function `to_gta_transitions` defined in the `GTA` module.

- A list of clocks appearing in the gTA (the name `"0"` is reserved for the
  constantly zero clock). By default, the gTA will assume a single clock
  named `"x"`.

  ```python
  clocks = ["x", "y"]
  ```

Then a gTA object can be constructed using
`GTA(locations, init_states, transitions, invariants, clocks)`.

### Constructing a Summary Automaton

To construct a summary automaton from a gTA, you can construct an object of
either `DTNMinus` or `DTNWithInv`. `DTNMinus` should be used with gTAs that
belong to the $DTN^-$ class, so gTAs that do not have invariants on locations
appearing in location guards.

`DTNWithInv` should be used only with gTAs with a single clock, but allows for
invariants in states appearing in location guards.

Both classes take an object of type `GTA` as input and provide you with the
methods `get_min_reach_time()` and `get_summary_automaton()`. Where
`get_min_reach_time()` will return a Dict providing you with the minimal global
reach time for each location and `get_summary_automaton()` will return a tuple
with the summary automaton (a `GTA` without location guards) and a `Dict` mapping
locations to the DBM describing the zone with the minimal global clock valuation
for that location.

### Output Format

An output format has not been implemented yet. You will have to use the encoding
of the summary automaton and translate it manually to the desired output format.

You can use the `print_min_reach_times()` to obtain the minimal reachability 
times for each state in the $DTN$.

We have already translated the systems used in the presented benchmarks to
[UPPAAL](https://uppaal.org/), more details can be found in the
["Benchmarks" section](#benchmarks).
