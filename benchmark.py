import argparse
import os
import shutil
import time

def prover_toml():
    return """
a = "0"
b = "1"
""".strip()

def circuit_source(n):
    size = 2**n
    source = f"""
global N: u32 = {size};

fn main(a: pub Field, b: pub Field) -> pub Field {{
    let mut seq = [0; N];
    seq[0] = a;
    seq[1] = b;

    for i in 2..N {{
        seq[i] = seq[i-1] + seq[i-2];
    }}
    seq[N-1]
}}
""".strip()
    return source

def generate_circuit(n, nargo_path):
    circuit_dir = f"circuits/{str(n)}"
    os.makedirs(circuit_dir, exist_ok=True)

    # Store current working directory
    original_dir = os.getcwd()
    
    try:
        # Change to the circuit directory
        os.chdir(circuit_dir)
        # Run nargo init silently
        os.system(f"{nargo_path} init > /dev/null 2>&1")
        
        # Create src directory and main.nr file
        os.makedirs("src", exist_ok=True)
        with open("src/main.nr", "w") as f:
            f.write(circuit_source(n))

        # Write Prover.toml
        with open("Prover.toml", "w") as f:
            f.write(prover_toml())
            
    finally:
        # Always return to original directory
        os.chdir(original_dir)

def generate_witness(n, nargo_path):
    # Store current working directory
    original_dir = os.getcwd()
    
    try:
        # cd to circuits/n and run nargo execute
        os.chdir(f"circuits/{str(n)}")
        start_time = time.time()
        os.system(f"{nargo_path} execute > /dev/null 2>&1")
        end_time = time.time()
        # Convert to milliseconds
        time_taken_ms = (end_time - start_time) * 1000
        return time_taken_ms
    finally:
        # Always return to original directory
        os.chdir(original_dir)

def generate_proof(n, nargo_path):
    # Store current working directory
    original_dir = os.getcwd()
    
    try:
        # cd to circuits/n and run nargo prove
        os.chdir(f"circuits/{str(n)}")
        start_time = time.time()
        os.system(f"{nargo_path} prove > /dev/null 2>&1")
        end_time = time.time()
        # Convert to milliseconds
        time_taken_ms = (end_time - start_time) * 1000
        return time_taken_ms
    finally:
        # Always return to original directory
        os.chdir(original_dir)

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Benchmarks for the Blocksense Nargo fork')
    
    # Add nargo path argument
    parser.add_argument('--nargo', type=str, required=True,
                       help='Path to the nargo binary')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if nargo binary exists
    if not os.path.isfile(args.nargo):
        raise FileNotFoundError(f"Nargo binary not found at: {args.nargo}")

    # Delete circuits/ directory
    if os.path.exists("circuits"):
        shutil.rmtree("circuits")
    
    # Create circuits/ directory
    os.makedirs("circuits", exist_ok=True)

    start = 10
    end = 14 # not inclusive
    for i in range(start, end):
        generate_circuit(i, args.nargo)

        print(f"Fibonacci size: 2^{i}")
        witness_time = generate_witness(i, args.nargo)
        print(f"Witness generation time: {witness_time} ms")

        proof_time = generate_proof(i, args.nargo)
        print(f"Proof generation time:   {proof_time} ms")

if __name__ == "__main__":
    main()
