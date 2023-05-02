# Verification for Disjunctive Networks of Timed Automata

This project is designed to check properties of networks of
timed automata guarded with disjunctive location guards. For that purpose, a
**Summary Automaton** will be computed with a language equivalent to a template
in a network. The main ideas implemented here are described in the
paper [here][paper].

In summary, properties of a network of timed automata can be checked on the
single summary automaton instead of checking them in a cutoff system (which are
substantially larger).

The program can check for a flooding path if the automaton has a single clock
and contains invariants on states appearing as location guards. If this is true
for all such states, the computed summary automaton is valid and can be used to
verify system properties.

As of now the project is in an **experimental state**, i.e. it currently does not
support

- Parsing an input file of any kind, instead, a user will have to manually
  encode the automaton into the projects Python representation (see
  [input format](#input-format)).

- Checking arbitrary properties, only reachability is supported directly. If a
  user wants to verify other properties of the system, she can do so by
  encoding the summary automaton into a different tool supporting verification
  timed automata, e.g. [UPAAL][UPAAL].

- Output of a summary automaton in a comprehensible format. Currently, summary
  automata are represented in the internal Python format. A user needs to
  manually encode them into, for example, the [UPAAL][UPAAL] format if
  she wants to check advanced properties of a system.

## Usage

### Requirements

This project requires Python `>=3.8`.

Alternatively, you can also use the provided Dockerfile. To execute the image
use:

```bash
docker run ghcr.io/splgb/verification-disjunctive-time-networks:latest
```

By default, it will execute the Benchmarks described in the paper and output
the runtime statistics. If you would like to interact with the program
interactively, use:

```bash
docker run --entrypoint python -it ghcr.io/splgb/verification-disjunctive-time-networks:latest
```

to obtain an interactive Python shell running in the container. To execute the
main function use:

```python
exec(open("main.py").read())
```

### Input Format

Currently, the Timed Automata (TA) templates must be manually encoded into a
Dict-based representation. You can find some examples in
[`./examples/example_tas.py`](./examples/example_tas.py).

A TA consist of :

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

  A `Constraint` is a limit on the difference on clocks, e.g. the first
  constraint requires the difference between the clock `x` and the constantly
  zero clock `0` to be $\leq 1$. A `Constraint` with an unbounded `Bound`, i.e.
  $< \infty$, does not limit the clock valuations. This representation has been
  designed with Difference Bound Matrices (DBMs) in mind, as they are used in
  the underlying zone graph exploration. More details can be found in the
  [paper][paper].

- Transitions, encoded as a Dict mapping from transition names to dict with the
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

- A list of clocks appearing in the TA (the name `"0"` is reserved for the
  constantly zero clock). By default the TA will assume a single clock
  named `"x"`.

  ```python
  clocks = ["x", "y"]
  ```

Then a TA object can be constructed using
`TA(locations, init_states, transitions, invariants, clocks)`.

### Constructing a Summary Automaton

To construct a summary automaton from a TA, you can construct an object of
either `DTNMinus` or `DTNWithInv`. `DTNMinus` should be used with TAs that
belong to the $DTN^-$ class, so TAs that do not have invariants on locations
appearing in location guards.

`DTNWithInv` should be used only with TAs with a single clock, but allows for
invariants in states appearing in location guards.

Both Classes take an object of type `TA` as an input and provide you with the
methods `get_min_reach_time()` and `get_summary_automaton()`. Where
`get_min_reach_time()` will return a Dict providing you with the minimal global
reach time for each location and `get_summary_automaton()` will return a tuple
with the summary automaton (a `TA` without location guards) and a Dict mapping
locations to the DBM describing the zone with the minimal global clock valuation
for that location.

### Output Format

An output format has not been implemented yet. You will have to use the encoding
of the summary automaton and translate it manually to the desired output format.

We have already translated the systems used in the presented benchmarks to
[UPAAL][UPAAL], more details will be explained in the ["Benchmarks" section](#benchmarks).

## Benchmarks

The paper presents a small benchmark suite, comparing the time it took to check
reachability in the cutoff system against the time it took to construct the
summary automaton and check properties on the automaton.

For the benchmarks presented in the paper [UPAAL][UPAAL] version `4.1.26-1` has
been used. We also provide the manual translations to the UPAAL specific input
format. They can be found in the folder [`bechmarks`](./benchmarks/).

### Structure

The paper presents two classes of benchmarks:

- Comparison of MinReach algorithm: The program computes the minimal global time
  to reach all locations. Here the execution time of the UPAAL queries
  can be directly compared with the execution times by the program. The relevant
  files can be found in
  [`./benchmarks/minreach-vs-upaal`](./benchmarks/minreach-vs-uppaal/).

- Computation of the Summary Automaton & checking properties: The program is
  used to compute the summary automaton, the properties can then be checked with
  UPAAL. The relevant files can be found in
  [`./benchmarks/gossip-clock-sync/`](./benchmarks/gossip-clock-sync/).The files
  ending with `summaryTA` indicate that they use the summary automaton
  construction and the `cutoff` suffix indicates that it contains the cutoff
  system construction.

### Executing the UPAAL files

If you have [UPAAL][UPAAL] along with the provided CLI interface installed,
checking the properties explained in the paper can performed by executing:

```bash
verifyta -u -s <path-to-uppaal-xml-file>
```

[paper]:[TODO]
[UPAAL]:[https://uppaal.org/]
