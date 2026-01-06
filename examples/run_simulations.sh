#!/usr/bin/env bash
set -euo pipefail

# Run all example LAMMPS simulations under examples/simulations/*/
#
# Usage:
#   ./run_simulations.sh
#
# Optional env vars:
#   LMP=lmp_mpi            # LAMMPS executable name/path
#   LMP_ARGS="-echo both"  # extra args passed to LAMMPS
#
# Each simulation is expected to have:
#   - in.lammps
#   - out/ (will be created if missing)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIMS_DIR="${ROOT_DIR}/simulations"

LMP="${LMP:-lmp_mpi}"
LMP_ARGS="${LMP_ARGS:-}"

if ! command -v "${LMP}" >/dev/null 2>&1; then
  echo "ERROR: '${LMP}' not found on PATH. Set LMP=/path/to/lmp_mpi and retry." >&2
  exit 1
fi

echo "Using LAMMPS: ${LMP}"
echo "Simulations dir: ${SIMS_DIR}"
echo

shopt -s nullglob
for sim_dir in "${SIMS_DIR}"/*; do
  [[ -d "${sim_dir}" ]] || continue
  [[ -f "${sim_dir}/in.lammps" ]] || continue

  echo "=== Running: $(basename "${sim_dir}") ==="
  mkdir -p "${sim_dir}/out"

  # Always write log inside the sim folder so outputs are isolated.
  (
    cd "${sim_dir}"
    "${LMP}" ${LMP_ARGS} -in "in.lammps" -log "out/log.lammps"
  )

  echo
done

echo "Done."


