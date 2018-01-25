# Mesos Metrics (docker.sieve.com.br/mesos-metrics)

## Env vars
* ASGARD_MESOS_METRICS_URL: Url to connect to Mesos

## Routes:
* /attrs: Returns the attrs available on the cluster.
* /slaves-with-attrs?**attr**=**value**: Returns slaves with the given attrs and values.
* /attr-usage?**attr**=**value**: Returns resource usage information about the given attributes.

## Running tests:
`$ py.test --cov=metrics --cov-report term-missing -v -s`
