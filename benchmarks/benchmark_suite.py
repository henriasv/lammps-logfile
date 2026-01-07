import time
import os
import psutil
import pandas as pd
import lammps_logfile

BENCHMARKS = [
    ("01_fcc_thermo_multi", "examples/simulations/01_fcc_thermo_multi/out/log.lammps"),
    ("02_bcc_custom_thermo", "examples/simulations/02_bcc_custom_thermo/out/log.lammps"),
    ("03_fcc_custom_longlog", "examples/simulations/03_fcc_custom_longlog/out/log.lammps"),
    ("04_bcc_multi_then_custom", "examples/simulations/04_bcc_multi_then_custom/out/log.lammps"),
    ("1GB_large_file", "benchmarks/large_benchmark.log")
]

def run_suite():
    results = []
    print(f"{'Simulation':<30} | {'Runs':<5} | {'Steps':<10} | {'Memory (MB)':<12} | {'Time (s)':<10}")
    print("-" * 85)

    for name, path in BENCHMARKS:
        if not os.path.exists(path):
            print(f"Skipping {name}: File not found at {path}")
            continue

        # Memory before
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024

        start_time = time.time()
        try:
            df = lammps_logfile.read_log(path)
            duration = time.time() - start_time
            
            # Memory after
            mem_after = process.memory_info().rss / 1024 / 1024
            mem_usage = mem_after - mem_before
            
            # Gather stats
            runs = df['run_num'].nunique() if 'run_num' in df.columns else 1
            steps = len(df)
            
            results.append({
                "Simulation": name,
                "Runs": runs,
                "Steps": steps,
                "Memory (MB)": f"{mem_usage:.2f}",
                "Time (s)": f"{duration:.4f}"
            })
            
            print(f"{name:<30} | {runs:<5} | {steps:<10} | {mem_usage:<12.2f} | {duration:<10.4f}")

        except Exception as e:
            print(f"Error parsing {name}: {e}")

    # Generate Markdown Table
    print("\n\nMarkdown Table:")
    print("| Simulation | Runs | Steps | Memory (MB) | Time (s) |")
    print("|:---|---:|---:|---:|---:|")
    for r in results:
        sim_name = r['Simulation'].replace("examples/simulations/", "")
        print(f"| {sim_name} | {r['Runs']} | {r['Steps']} | {r['Memory (MB)']} | {r['Time (s)']} |")

if __name__ == "__main__":
    run_suite()
