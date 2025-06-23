.PHONY: default setup test

include .env
export 

src=src
dist=dist
target=dist/target.zip

default: # noop
	@echo "dev:  fn=$(DEV_FN), url=$(DEV_URL)" \

identity: # configure aws user
	aws sts get-caller-identity

run:
	python src/lambda_function.py

test:
	clear && python -m pytest -vs

dev-invoke:
	@aws lambda invoke --function-name $(DEV_FN) --payload fileb://payload.json res.json && cat res.json |jq

dev-get:
	curl -X GET $(DEV_URL)

dev-headers:
	curl -IL -X GET $(DEV_URL)

prepare:
	git rev-parse HEAD > src/commit.txt \
	&& mkdir -p $(dist) \
	&& rm -f $(target) \
	&& (cd $(src) && zip -r ../$(target) . -x ".*" "__pycache__/*" "venv/*") 

dev-deploy:
	make prepare \
	&& aws lambda update-function-code --function-name $(DEV_FN) --zip-file fileb://$(target) --no-cli-pager \
	&& sleep 5 \
	&& ENV_CONFIG=$$(jq -c .Environment conf/dev.json) \
	&& aws lambda update-function-configuration --function-name $(DEV_FN) --environment "$$ENV_CONFIG" --no-cli-pager 


