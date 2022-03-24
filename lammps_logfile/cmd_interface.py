from lammps_logfile import File
from lammps_logfile import running_mean
import argparse
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def get_parser():
    parser = argparse.ArgumentParser(description="Plot contents from lammps log files")
    parser.add_argument("input_file", type=str, help="Lammps log file containing thermo output from lammps simulation.")
    parser.add_argument("-x", type=str, default="Time", help="Data to plot on the first axis.")
    parser.add_argument("-y", type=str, nargs="+", help="Data to plot on the second axis. You can supply several names to get several plot lines in the same figure.")
    parser.add_argument("-a", "--running_average", type=int, default=1, help="Optionally average over this many log entries with a running average. Some thermo properties fluctuate wildly, and often we are interested in the running average of properties like temperature and pressure.")
    parser.add_argument("-s", "--subplots", default=False, action='store_true', help="Show subplot panels for different graphs.")
    parser.add_argument("-p", "--progress", default=False, action='store_true', help="Show progress of simulation. This requires that 'Step' is written to log file.")
    parser.add_argument("-l", "--live", default=False, action='store_true', help="Show live visualisation of graphs. This is useful when monitoring thermo outputs during simulation.")
    return parser


def create_progress_string(log):
    """Returning string with progress"""
    try:
        steps = log.get("Step")
    except:
        raise ValueError("'Step' is not written to logfile! Not able to monitor progress.")
    rel_step = int(steps[-1] - steps[0])
    num_steps = log.num_timesteps[-1]
    return f"{rel_step}/{num_steps}"


def run():
    args = get_parser().parse_args()
    if args.subplots:
        fig, ax = plt.subplots(len(args.y), sharex=True, squeeze=False)
    else:
        fig = plt.figure()

    def get_data(i=0):
        log = File(args.input_file)
        x = log.get(args.x)
        #print(x)
        plt.cla()
        for i, y in enumerate(args.y):
            data = log.get(y)
            #print(data)

            if args.running_average >= 2:
                x = running_mean(x, args.running_average)
                data = running_mean(data, args.running_average)

            if args.subplots:
                ax[i, 0].cla()
                ax[i, 0].plot(x, data)
                ax[-1, 0].set_xlabel(args.x)
                ax[i, 0].set_ylabel(y)
            else:
                plt.plot(x, data, label=y)
                plt.legend()
        if args.progress:
            fig.suptitle(create_progress_string(log))
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    if args.live:
        ani = FuncAnimation(fig, get_data, interval=1000)
    else:
        get_data()
    plt.show()

