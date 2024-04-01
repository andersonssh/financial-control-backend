build:
	pipenv run pip freeze > requirements.txt
	git archive -o build.zip --format=zip HEAD
	zip build.zip requirements.txt
	rm requirements.txt