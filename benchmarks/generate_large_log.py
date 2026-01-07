import os

FILENAME = "benchmarks/large_benchmark.log"
TARGET_SIZE = 1024 * 1024 * 1024  # 1 GB

header = "Memory usage per processor = 2.4 Mbytes\n" \
         "Step Temp Press KinEng PotEng TotEng Volume\n"
footer = "Loop time of 10.0 on 1 procs for 100 steps with 1000 atoms\n"

def generate():
    print(f"Generating ~1GB log file at {FILENAME}...")
    with open(FILENAME, "w") as f:
        f.write(header)
        current_size = len(header)
        step = 0
        
        # Buffer lines to write in chunks for speed
        chunk_lines = []
        chunk_size = 0
        
        # Each line is approx 45 bytes. Need ~23 million lines.
        while current_size < TARGET_SIZE:
            line = f"{step} 300.0 1.0 100.0 -200.0 -100.0 1000.0\n"
            chunk_lines.append(line)
            chunk_size += len(line)
            
            if len(chunk_lines) >= 50000:
                f.writelines(chunk_lines)
                current_size += chunk_size
                chunk_lines = []
                chunk_size = 0
                if step % 1000000 == 0:
                    print(f"Generated {current_size / 1024 / 1024:.2f} MB", end='\r')
            
            step += 1
            
        if chunk_lines:
            f.writelines(chunk_lines)
            current_size += chunk_size
            
        f.write(footer)
        print(f"\nFinished. Size: {os.path.getsize(FILENAME) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    generate()
