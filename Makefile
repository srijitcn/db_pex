PYTHON=$(shell which python)

clean:
	rm -rf .pytest_cache
	rm -rf db_pex.egg-info
	rm -rf target

build: clean
	mkdir -p target
	pex . --disable-cache -r requirements.txt -c test.py -o target/db_pex.pex --python=$(PYTHON) 
