# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Fixed
- Thermo blocks that are not terminated by a `Loop time` line (e.g. an interrupted run, or a LAMMPS build that does not print the loop summary) are now parsed correctly by both `read_log` and `File`. Previously the trailing `Total wall time` line (or the next run's setup output) was swallowed into the data as a garbage row, turning numeric columns into strings. A block now ends at `Total wall time`, at the next run's start marker, or at end of file, and any remaining non-numeric lines inside a block (e.g. a `WARNING` printed mid-run) are skipped.
- `read_log` on a non-mmappable stream such as `io.StringIO` returned an empty DataFrame instead of falling back to the line-based reader.

### Performance
- The mmap reader no longer re-scans to end of file for every run when a stop marker is absent, which made logs with many `run` commands quadratically slow (a 77 MB log with 2000 runs: 56 s -> 0.7 s).

## [1.1.3] - 2026-01-08

### Performance
- **Major Speedup**: Implemented a memory-mapped (`mmap`) based parser that is ~40% faster on large files.
- **Reduced Memory Overhead**: The parser now lazily scans the file on disk instead of loading it entirely into RAM.

### Documentation
- Updated benchmarks in README to reflect new performance.
- Improved "Key Features" section in documentation for better responsiveness.

## [1.1] - 2026-01-06

### Added
- New `get_log` function that returns a pandas DataFrame with all the log file contents. This is now the preferred way to read log files. 
- GitHub Actions workflow for automated releases to PyPI and GitHub Releases.
- Added versioning configuration to documentation.

### Changed
- Documentation overhaul using the PyData Sphinx theme.
- Updated version to 1.1.
