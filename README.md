# AWS bitbucket pipeline deploy poc

## resources
- [automating aws lambda](https://www.atlassian.com/blog/bitbucket/aws-lambda-deployments-using-bitbucket-pipelines-and-pipes)
- [how to](https://support.atlassian.com/bitbucket-cloud/docs/deploy-a-lambda-function-update-to-aws/)
- [source code](https://bitbucket.org/atlassian/aws-lambda-deploy/src/master/)
- [aws fn configuration via boto](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/update_function_configuration.html)

## setup
- aws: create policy for lambda deployments
- aws: create iam user for lambda deployments ( attach policy )
- aws: create lambda 
- bb: create repo in bitbucket
- bb: enable pipelines in `<repository> / repository settings / pipelines / settings`
- bb: set `AWS_ACCESS_KEY_ID` in `<repository> / repository settings / respository variables`
- bb: set `AWS_SECRET_ACCESS_KEY` in `<repository> / repository settings / respository variables`
- bb: set `AWS_DEFAULT_REGION` in `<repository> / repository settings / respository variables`
- local: create `src/lambda_function.py`
- local: create `conf/dev.json` to update fn configuration
- local: create `conf/prod.json` to update fn configuration
- local: create `bitbucket-pipelines.yml` 
- local: set `bitbucket-pipelines.yml::FUNCTION_NAME` 
- local: set `bitbucket-pipelines.yml::FUNCTION_CONFIGURATION` 

## deploy
- prod: add tag `prod-<identifier>` to any commit ... for example `prod-001` or `prod-20250601.1`
- dev: add tag `prod-<identifier>` to any commit ... for example `prod-001` or `prod-20250601.1`

## after deploy
- check `commit.txt` for lambda fn it should look something like,

```
commit:6275d49af826e782548639857092c165fdad066a
tag:dev-010
```

## testing
set your payload in `Makefile` appropriately

- dev: run `make invoke-dev`
- prod: run `make invoke-prod`

## Iam setup
Deployment policy,
- atlassian states required policy is `AWSLambdaFullAccess` (here)[https://www.atlassian.com/blog/bitbucket/aws-lambda-deployments-using-bitbucket-pipelines-and-pipes]
- we create a user and attach the policy directly

`lambda-deploy-user`
- create user with `console-access=true`
- attach policy `AWSLambdaFullAccess` directly
- create access key with `use case=cli`
- copy `access_key` for use in bitbucket pipeline 
- copy `access_key_secret` for use in bitbucket pipeline 

