# Benchmarks for the Blocksense Plonky2 Noir / Nargo backend

The Blocksense fork of Nargo v0.35 uses Plonky2 as the backend for generating
proofs. This repository contains a Python script that generates circuits of
various sizes (2^10 to 2^14) and measures the witness and proof generation
times.

## Usage

First, clone and compile the Blocksense fork of Noir / Nargo:

```bash
git clone https://github.com/blocksense/noir.git
cd noir
cargo build --release
```

Note that the `circuits` directory **will be deleted** when the script is run.

Run `benchmark.py` and specify the path to the compiled Nargo binary:

```bash
python benchmark.py --nargo ~/noir/target/release/nargo
```

## Results

On an Intel 13th Gen Intel(R) Core(TM) i7-13700HX running Ubuntu Linux:

```
Fibonacci size: 2^10
Witness generation time: 1878.1745433807373 ms
Proof generation time:   1667.2353744506836 ms
Fibonacci size: 2^11
Witness generation time: 1771.8946933746338 ms
Proof generation time:   2388.833522796631 ms
Fibonacci size: 2^12
Witness generation time: 3527.2696018218994 ms
Proof generation time:   5291.45622253418 ms
Fibonacci size: 2^13
Witness generation time: 9142.807006835938 ms
Proof generation time:   16868.115663528442 ms
```
