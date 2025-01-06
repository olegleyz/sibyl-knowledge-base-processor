.PHONY: clean build deploy deploy-guided

PATH_TO_PROJECT := $(shell pwd)

clean:
	rm -rf .aws-sam

build: clean
	export PATH_TO_PROJECT=$(PATH_TO_PROJECT) && sam build

deploy-guided:
	sam deploy --guided

deploy:
	sam deploy --profile admin