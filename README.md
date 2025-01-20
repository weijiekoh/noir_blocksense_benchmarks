# Benchmarks for the Blocksense Plonky2 Noir / Nargo backend

The Blocksense fork of Nargo v0.35 uses Plonky2 as the backend for generating
proofs. This repository contains a Python script that generates circuits of
various sizes (2^10 to 2^14) and measures the witness and proof generation
times.

## Usage

Note that the `circuits` directory **will be deleted** when the script is run.

```bash
python benchmark.py
```
