from lammps_logfile import File
import argparse
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description="Plot contents from lammps log files")
    parser.add_argument("input_file", type=str)
    parser.add_argument("-x", type=str, default="Time")
    parser.add_argument("-y", type=str, nargs="+")
    args = parser.parse_args()
    return args

def run():
    print("Hello from plotter")
    args = get_args()
    log = File(args.input_file)
    x = log.get(args.x)
    print(x)
    for y in args.y:
        data = log.get(y)
        print(data)
        plt.plot(x, data, label=y)
    plt.legend()
    plt.show()
    
