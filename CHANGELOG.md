# Mesos Metrics (docker.sieve.com.br/mesos-metrics)

## Changelog


### 0.6.0

 * Implementação do entpoint /tasks/count para podermos ter a contagem de tasks no cluster (IN-2535)

### 0.5.0
  - Implementação de endpoints `/attrs/count` e `/slaves-with-attrs/count`;
  - Implementação da leitura de métricas sempre do mesos leader;
  - Uso do asgard-api-sdk para ter acesso a envvars multi-valor.

### 0.4.1
  - Adição de logs de debug na chamada à API do mesos

### 0.4.0
  - Recebe logger que é passado pela API no momento de inicializar o plugin

### 0.3.0rc2
  - Novo endpoint para pegar métricas sempre do atual mesos master lider

### 0.3.0rc1
  - Novos endpoints para buscar métricas dos mesos master e slaves

### 0.2.0
  - Versão 0.1.0 estava quebrada. Faltou o o registro do plugin

### 0.1.0
  - Migração do projeto para ser um plugin do asgard-api

