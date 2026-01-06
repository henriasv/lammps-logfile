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
	cd getting_started/python && python3 getting_started.py > output.txt && cd ../..
	# Run legacy getting started example
	# We need to make sure the output goes where the legacy docs expect it (../../getting_started/python/output.txt)
	# But the legacy script is now in docs/legacy/python.
	# The legacy/index.md expects images in ../../getting_started/python/
	# and output in ../../getting_started/python/output.txt
	# The legacy script writes to current directory.
	# So we can run it, but we might want to suppress its output if it conflicts, or just run the new one last to overwrite if names collide.
	# However, the legacy script generates output.txt too.
	# Let's see: legacy/index.md includes output.txt from ../../getting_started/python/output.txt
	# getting_started/index.md includes output.txt from python/output.txt (relative to getting_started/index.md, so getting_started/python/output.txt)
	# So both point to the same file.
	# The new script prints columns. The legacy script prints keywords.
	# We should probably let the new script win for the "output.txt" used in getting_started/index.md.
	# For legacy/index.md, we might need a separate output file.
	# I will update legacy/index.md to point to a different output file if I can, or just accept that they share for now?
	# No, legacy/index.md shows `log.get_keywords()`. New shows `data.columns`. They are different.
	# So I should update legacy/index.md to look for `legacy_output.txt`.

	cd legacy/python && python3 getting_started_legacy.py > legacy_output.txt && cd ../..

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
