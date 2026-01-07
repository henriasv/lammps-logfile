# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

.PHONY: examples
examples:
	# Run new getting started example
	cd tutorials/python && python3 getting_started.py > output.txt && cd ../..
	# Run legacy getting started example
	cd reference/legacy/python && python3 getting_started_legacy.py > legacy_output.txt && cd ../../../..

# Target to prepare examples for sphinx-gallery
.PHONY: prepare-examples
prepare-examples:
	mkdir -p examples_source
	ln -sf ../../examples/logfiles/crack_log.lammps examples_source/crack_log.lammps

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile prepare-examples
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
