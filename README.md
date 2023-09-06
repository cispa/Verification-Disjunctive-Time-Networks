# Verification for Disjunctive Networks of Timed Automata

This project checks reachability of locations in networks of
timed automata guarded with disjunctive location guards. For that purpose, a
**Summary Automaton** will be computed. The main ideas are described in the
corresponding [paper](http://arxiv.org/abs/2305.07295).

This repository contains an implementation which for a $DTN$ given in the form
of a single guarded Timed Automaton (gTA) with a single clock will compute a
**Summary Automaton**. This summary automaton is then proven in the paper to be
language equivalent to the $DTN$ it represents (under certain conditions).
Hence, it can be used to verify properties of the $DTN$ instead of the product
system.

The program can check for the existence of **flooding paths** for automata
with a single clock and invariants on states appearing as location guards. If
such a path exists for every state that appears in a location and has location
invariants, the computed summary automaton is valid and can be used to verify
the system properties.

As of now, the project is in an **experimental state**, i.e. it currently does
not support

- Parsing an input file of any kind. Instead, a user will have to manually
  encode the automaton into the project's Python representation (see
  [input format](#input-format)).

- Checking arbitrary properties, only reachability is supported directly. If a
  user wants to verify other properties of the system, she can do so by
  encoding the summary automaton into a different tool supporting verification
  timed automata, e.g. [UPAAL](https://uppaal.org/).

- Output of a summary automaton in a comprehensible format. Currently, summary
  automata are represented in the internal Python format. A user needs to
  manually encode them into, for example, the [UPAAL](https://uppaal.org/)
  format if she wants to check advanced properties of a system.

## Usage

### Requirements

#### Executing Locally

This project only requires Python `>=3.9`, all other modules are included or
part of the Python standard library. To execute the program use

```bash
python3 main.py
```

#### Docker

Alternatively, you can also use the provided Dockerfile. To execute the image
use:

```bash
docker run ghcr.io/cispa/verification-disjunctive-time-networks:latest
```

By default, it will execute the benchmarks described in the paper and output
the runtime statistics. If you would like to use the program
interactively, use:

```bash
docker run --entrypoint python -it ghcr.io/cispa/verification-disjunctive-time-networks:latest
```

to start an interactive Python shell running in the container. To execute the
main function use:

```python
exec(open("main.py").read())
```

# TODO: --extended flag

### Input Format

Currently, the gTA definition must be manually encoded into a
`Dict`-based representation. Some examples can be found in
[`./examples/example_tas.py`](./examples/example_tas.py). We will explain the
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
    transitions = {
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
        }
  ```

- A list of clocks appearing in the gTA (the name `"0"` is reserved for the
  constantly zero clock). By default, the gTA will assume a single clock
  named `"x"`.

  ```python
  clocks = ["x", "y"]
  ```

Then a gTA object can be constructed using
`TA(locations, init_states, transitions, invariants, clocks)`.

### Constructing a Summary Automaton

To construct a summary automaton from a gTA, you can construct an object of
either `DTNMinus` or `DTNWithInv`. `DTNMinus` should be used with gTAs that
belong to the $DTN^-$ class, so gTAs that do not have invariants on locations
appearing in location guards.

`DTNWithInv` should be used only with gTAs with a single clock, but allows for
invariants in states appearing in location guards.

Both classes take an object of type `TA` as input and provide you with the
methods `get_min_reach_time()` and `get_summary_automaton()`. Where
`get_min_reach_time()` will return a Dict providing you with the minimal global
reach time for each location and `get_summary_automaton()` will return a tuple
with the summary automaton (a `TA` without location guards) and a `Dict`` mapping
locations to the DBM describing the zone with the minimal global clock valuation
for that location.

### Output Format

An output format has not been implemented yet. You will have to use the encoding
of the summary automaton and translate it manually to the desired output format.

We have already translated the systems used in the presented benchmarks to
[UPAAL](https://uppaal.org/), more details can be found in thehe 
["Benchmarks" section](#benchmarks).

## Benchmarks

The paper presents a small benchmark suite, comparing the time it took to check
reachability in the cutoff system against the time it took to construct the
summary automaton and check properties on the automaton.

For the benchmarks presented in the paper [UPAAL](https://uppaal.org/) version
`4.1.26-1` has been used. We also provide the manual translations to the
UPAAL specific input format. They can be found in the folder
[`benchmarks`](./benchmarks/).

### Structure

The paper presents two classes of benchmarks:

- Comparison of MinReach algorithm: The program computes the minimal global time
  to reach all locations. Here the execution time of the UPAAL queries
  can be directly compared with the execution times by the program. The relevant
  files can be found in
  [`./benchmarks/minreach-vs-upaal`](./benchmarks/minreach-vs-uppaal/).

- Computation of the Summary Automaton & checking properties: The program is
  used to compute the summary automaton, the properties can then be checked withhe 
  UPAAL. The relevant files can be found in
  [`./benchmarks/gossip-clock-sync/`](./benchmarks/gossip-clock-sync/). The files
  ending with `summaryTA` indicate that they use the summary automaton
  construction and the `cutoff` suffix indicates that it contains a cutoff
  system construction.

### Executing the UPAAL files

If you have [UPAAL](https://uppaal.org/) along with the provided CLI interface installed,
checking the properties explained in the paper can be performed by executing:

```bash
verifyta -u -s <path-to-uppaal-xml-file>
```
