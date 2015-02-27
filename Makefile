# Copyright (C) 2015 Craig Phillips.  All rights reserved.

all:
	@true

verbose:
	@true

debug:
	@true

export BUILDROOT:= $(shell readlink -m BUILDROOT)
export PATH:= $(shell readlink -f bin):$(PATH)

SILENT:= $(if $(filter verbose,$(MAKECMDGOALS)),,@)
DEBUG:= $(if $(filter debug,$(MAKECMDGOALS)),1,)

ifneq (,$(SILENT))
define fn_silent
	( t=`mktemp` ; \
	e=0 ; \
	if ! ( $1 ) 1>$$t.out 2>$$t.err ; then \
		e=1 ; \
		cat $$t.err ; \
	fi ; \
	rm -f $$t.* ; \
	exit $$e ; )
endef
else
define fn_silent
	( t=`mktemp` ; \
	e=0 ; \
	( $1 ) 1>$$t.out 2>&1 || e=$$? ; \
	cat $$t.out ; \
	rm -f $$t.* ; \
	exit $$e ; )
endef
endif

V:= $(if $(SILENT),,-v)
X:= $(if $(DEBUG),-x,)

tests:= $(wildcard tests/*/test.sh)
run_test_targets:= $(tests:tests/%/test.sh=run_test_%)

run_tests: $(run_test_targets)

coverage:
	@shlcov -i $(SHCOV_DATADIR) $(BUILDROOT)/shcov/html

clean:
	@rm $V -rf $(BUILDROOT)

$(run_test_targets): run_test_% : tests/%/test.sh
	@$(call fn_silent,echo "Running test $*")
	@rm $V -rf $(BUILDROOT)/$*
	@TEST_DEBUG=$(DEBUG) bash $X tests/run_test.sh $*
