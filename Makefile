PYTEST_PROCCESS_COUNT = 4

test-sample_app:
	pytest -n $(PYTEST_PROCCESS_COUNT) --cov=sample_app sample_app/tests --cov-report term-missing

test:
	pytest -n $(PYTEST_PROCCESS_COUNT) \
		--cov=users users/tests \
		--cov=social social/tests \
		--cov-report term-missing

test-seperated-report:
	make test-sample_app


dev-setup : 
	$ pip install --upgrade pip
	$ pip install -r requirements.dev.txt
	$ pre-commit install


format : 
	$ python -m autoflake --in-place --remove-unused-variables --recursive ./*/*.py
	$ python -m black --preview ./*/*.py 
