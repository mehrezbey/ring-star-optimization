PY=python3
PKGDIR=.packages

.PHONY: install check run clean

install:
	@mkdir -p $(PKGDIR)
	$(PY) -m pip install --target $(PKGDIR) -r requirements.txt

check:
	PYTHONPATH=$(PKGDIR) $(PY) -c "import pulp, matplotlib; print('OK: pulp et matplotlib OK')"

run:
	PYTHONPATH=$(PKGDIR) $(PY) src/main.py

clean:
	rm -rf $(PKGDIR) _pycache_ *.pyc
	rm -f src/results.csv