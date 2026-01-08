# Changelog

All notable changes to this project will be documented in this file.

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
