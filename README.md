# Mesos Metrics (docker.sieve.com.br/mesos-metrics)

## Changelog

* 0.2.0
  - Versão 0.1.0 estava quebrada. Faltou o o registro do plugin

* 0.1.0
  - Migração do projeto para ser um plugin do asgard-api


## Env vars
* ASGARD_MESOS_METRICS_URL: Url to connect to Mesos

## Routes:
* /attrs: Returns the attrs available on the cluster.
* /slaves-with-attrs?**attr**=**value**: Returns slaves with the given attrs and values.
* /attr-usage?**attr**=**value**: Returns resource usage information about the given attributes.
* /master/<ip>?prefix=<prefix>: Retorna as métricas do master que começam por <prefix>.
* /slave/<ip>?prefix=<prefix>: Retorna as métricas do slave que começam por <prefix>
* /leader?prefix=<prefix>: Igual aos endpoints acima, mas descobre quem é o atual lider e pega dele.

## Running tests:
`$ py.test --cov=metrics --cov-report term-missing -v -s`
