# Mesos Metrics

## Env vars
* MESOS_URL: Url to connect to Mesos
* BASICAUTH_USERNAME: Username credential to access the metrics
* BASICAUTH_PASSWORD: Password credential to access the metrics

## Routes:
* /attrs: Returns the attrs available on the cluster.
* /slaves-with-attrs?**attr**=**value**: Returns slaves with the given attrs and values.
* /attr-usage?**attr**=**value**: Returns resource usage information about the given attributes.

## Running tests:
`$ py.test --cov=metrics --cov-report term-missing -v -s`
