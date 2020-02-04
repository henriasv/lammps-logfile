from lammps_logfile import File
from lammps_logfile import running_mean
import argparse
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description="Plot contents from lammps log files")
    parser.add_argument("input_file", type=str)
    parser.add_argument("-x", type=str, default="Time")
    parser.add_argument("-y", type=str, nargs="+")
    parser.add_argument("-a", "--running_average", type=int, default=1)
    args = parser.parse_args()
    return args

def run():
    args = get_args()
    log = File(args.input_file)
    x = log.get(args.x)
    print(x)
    for y in args.y:
        data = log.get(y)
        print(data)

        if args.running_average >= 2:
            x = running_mean(x, args.running_average)
            data = running_mean(data, args.running_average)

        plt.plot(x, data, label=y)
    plt.legend()
    plt.show()
    
