# Mesos Metrics (docker.sieve.com.br/mesos-metrics)

## Changelog


* 0.5.0-rc1
  - Implementação de endpoints `/attrs/count` e `/slaves-with-attrs/count`;
  - Implementação da leitura de métricas sempre do mesos leader;
  - Uso do asgard-api-sdk para ter acesso a envvars multi-valor.

* 0.4.1
  - Adição de logs de debug na chamada à API do mesos

* 0.4.0
  - Recebe logger que é passado pela API no momento de inicializar o plugin

* 0.3.0rc2
  - Novo endpoint para pegar métricas sempre do atual mesos master lider

* 0.3.0rc1
  - Novos endpoints para buscar métricas dos mesos master e slaves

* 0.2.0
  - Versão 0.1.0 estava quebrada. Faltou o o registro do plugin

* 0.1.0
  - Migração do projeto para ser um plugin do asgard-api


## Env vars
* Todas as env são lidas pela `asgard-api-sdk`. As que são necessária aqui são 
as que possuem sufixo `_MESOS_ADDRESS_<N>`. Mais detalhes na doc da `asgard-api-sdk`.

## Routes:
* /attrs: Returns the attrs available on the cluster.
* /attrs/count: Returns the count of all attributes used on the cluster
* /slaves-with-attrs?**attr**=**value**: Returns slaves with the given attrs and values.
* /slaves-with-attrs/count?**attr**=**value**: Returns the count of slaves with the given attrs and values.
* /attr-usage?**attr**=**value**: Returns resource usage information about the given attributes.
* /master/<ip>?prefix=<prefix>: Retorna as métricas do master que começam por <prefix>.
* /slave/<ip>?prefix=<prefix>: Retorna as métricas do slave que começam por <prefix>
* /leader?prefix=<prefix>: Igual aos endpoints acima, mas descobre quem é o atual lider e pega dele.

## Running tests:
`$ py.test --cov=metrics --cov-report term-missing -v -s`
