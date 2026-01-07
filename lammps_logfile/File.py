from io import BytesIO, StringIO

import numpy as np
import pandas as pd


class File:
    """
    Class for handling lammps log files.

    Parameters
    ----------
    ifile : str or file
        Path to lammps log file or a file-like object.
    """
    def __init__(self, ifile):
        # Identifiers for places in the log file
        self.start_thermo_strings = ["Memory usage per processor", "Per MPI rank memory allocation"]
        self.stop_thermo_strings = ["Loop time", "ERROR", "Fix halt condition"]
        self.data_dict = {}
        self.keywords = []
        self.output_before_first_run = ""
        self.partial_logs = []
        if hasattr(ifile, "read"):
            self.logfile = ifile
        else:
            self.logfile = open(ifile, 'r')
        self.read_file_to_dict()

    def read_file_to_dict(self):
        contents = self.logfile.readlines()
        keyword_flag = False
        before_first_run_flag = True
        i = 0
        while i < len(contents):
            line = contents[i]
            if before_first_run_flag:
                self.output_before_first_run += line

            if keyword_flag:
                keywords = line.split()
                tmpString = ""
                # Check wheter any of the thermo stop strings are in the present line
                while not sum([string in line for string in self.stop_thermo_strings]) >= 1:
                    if "\n" in line:
                        tmpString+=line
                    i+=1
                    if i<len(contents):
                        line = contents[i]
                    else:
                        break
                partialLogContents = pd.read_table(StringIO(tmpString), sep=r'\s+')

                if (self.keywords != keywords):
                    # If the log keyword changes, i.e. the thermo data to be outputted chages,
                    # we flush all prevous log data. This is a limitation of this implementation. 
                    self.flush_dict_and_set_new_keyword(keywords)

                self.partial_dict = {}
                for name in keywords:
                    self.data_dict[name] = np.append(self.data_dict[name],partialLogContents[name])
                    self.partial_dict[name] = np.append(np.asarray([]), partialLogContents[name])
                self.partial_logs.append(self.partial_dict)
                keyword_flag = False

            # Check whether the string matches any of the start string identifiers
            if sum([line.startswith(string) for string in self.start_thermo_strings]) >= 1:
                keyword_flag = True
                before_first_run_flag = False
            i += 1

    def flush_dict_and_set_new_keyword(self, keywords):
        self.data_dict = {}
        for entry in keywords:
            self.data_dict[entry] = np.asarray([])
        self.keywords = keywords

    def get(self, entry_name, run_num=-1):
        """
        Get time-series from log file by name.

        If the rows in the log file changes between runs, the logs are being flushed.

        Parameters
        ----------
        entry_name : str
            Name of the entry, for example "Temp".
        run_num : int, optional
            Lammps simulations commonly involve several run-commands. Here you may choose
            what run you want the log data from. Default of -1 returns data from all runs
            concatenated.

        Returns
        -------
        numpy.ndarray or None
            Array containing the requested data, or None if the entry is not found.
        """

        if run_num == -1:
            if entry_name in self.data_dict.keys():
                return self.data_dict[entry_name]
            else:
                return None
        else:
            if len(self.partial_logs) > run_num:
                partial_log = self.partial_logs[run_num]
                if entry_name in partial_log.keys():
                    return partial_log[entry_name]
                else:
                    return None
            else:
                return None

    def get_keywords(self, run_num=-1):
        """
        Return list of available data columns in the log file.

        Parameters
        ----------
        run_num : int, optional
            The run number to get keywords for. Default is -1 (all unique keywords found).

        Returns
        -------
        list
            Sorted list of available data columns.
        """
        if run_num == -1:
            return sorted(self.keywords)
        else:
            if len(self.partial_logs) > run_num: 
                return sorted(list(self.partial_logs[run_num].keys()))
            else:
                return None

    def to_exdir_group(self, name, exdirfile):
        """
        Writes the log file data to an Exdir group.

        Parameters
        ----------
        name : str
            Name of the group to create.
        exdirfile : exdir.File
            The Exdir file object to write to.
        """
        group = exdirfile.require_group(name)
        for i, log in enumerate(self.partial_logs):
            subgroup = group.require_group(str(i))
            for key, value in log.items():
                key = key.replace("/", ".")
                subgroup.create_dataset(key, data=value)

    def to_dataframe(self, run_num=-1):
        """
        Converts the log data for a specific run to a pandas DataFrame.

        Parameters
        ----------
        run_num : int, optional
            The run number to convert. Default is -1 (last run).

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the log data for the specified run.
        """
        return pd.DataFrame(self.partial_logs[run_num])


    def get_num_partial_logs(self):
        """
        Returns the number of partial logs (runs) found in the file.

        Returns
        -------
        int
            Number of runs.
        """
        return len(self.partial_logs)

    @property
    def names(self):
        """
        Exposes the keywords returned by get_keywords.

        Returns
        -------
        list
            List of keywords.
        """
        return self.get_keywords()
