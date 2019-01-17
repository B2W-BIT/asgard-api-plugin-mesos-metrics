# Asgard API Plugin Metrics Mesos

Esse projeto implementa a interface de plugin da Asgard API e adiciona novs endpoints que retornam
números sobre o cluster de Mesos.

# Interface de Plugins da Asgard API

A interface de plugins consiste em implementar um método com a seguinte assinatura:

```python
def asgard_api_plugin_init(**kwargs):
  pass
```

Esse método será chamado com uma série de keyword arguments. Por enquando o único kwarg passado é
o `logger`. Nesse kwarg é passado uma instância de Logger para que o plugin possa usar.

Essa função deve retornar um dict com essa estrutura:

```python
{
  "blueprint": <blueprint-instance>
}
```

Onde `<blueprint-instance>` é uma instância de um `Flask.Blueprint`. Cada rota registrada nesse blueprint
será plugada na Asgard API abaixo do path: `/_cat/metrics/<package-name>/*`.

Aqui, `<package-name>` é o nome do seu pacote registrado no Pypi.

## Registrando sua função de inicialização

Em seu `setup.py` adicione esse trecho:

```python

    entry_points={
        'asgard_api_metrics_mountpoint': [
            'init = <module>:function_name',
        ],
    }
```

Dessa forma, quando a Asgard API der boot, ela vai chmar a função definida nessa configuração. Os logs as Asgard API indicam se
o carregamento dos plugin foi feito com sucesso ou não.

## Instalando seu plugin em sua Asgard API

Para que esse plugin seja ativado, basta que você faça `pip install asgard-api-plugin-metrics-mesos==<version>` durante o build da sua Asgard API, ou seja,
basta adicionar esse pacote (`asgard-api-plugin-metrics-mesos`) como dependencia no seu deploy da Asgard API.

# Endpoints implementados por esse plugin


## Routes:
* /attrs: Retorna uma lista com todos os atributos usados em todos os slaves do cluster. Atributos de nome igual são agrupados;
* /attrs/count: Retorna a contagem de quantos atributos estão sendo usados em todo o cluster;
* /slaves-with-attrs?**attr**=**value**: Retorna todos os slaves do cluster que possuem o atributo `attr` com valor `value`;
* /slaves-with-attrs/count?**attr**=**value**: Retorna a contagem de slaves que possuem o atributo `attr` com valor `value`;
* /attr-usage?**attr**=**value**: Retorna o uso (percentual e absoluto) de CPU e RAM dos slaves que possuem o atributo `attr` com o valor `value`;
* /master/<ip>?prefix=<prefix>: Retorna as métricas do Mesos master cpm IP=`<ip>` que começam por <prefix>;
* /slave/<ip>?prefix=<prefix>: Retorna as métricas do Mesos slave com IP=`<ip>` que começam por <prefix>;
* /leader?prefix=<prefix>: Igual aos endpoints acima, mas descobre quem é o atual lider e pega os dados dele;
* /masters/alive: Retorna um JSON com cada IP de master e uma indicação se eles responderam ao "ping", ex:

```
{
   "http://172.18.0.11:5050" : 0,
   "http://172.18.0.13:5050" : 1,
   "http://172.18.0.12:5050" : 1
}
```

## Env vars
* Todas as env são lidas pela `asgard-api-sdk`. As que são necessária aqui são 
as que possuem sufixo `_MESOS_ADDRESS_<N>`. Mais detalhes na doc da [asgard-api-sdk](https://github.com/B2W-BIT/asgard-api-sdk).


## Running tests:
Para que você possa rodar os testes é necessário ter uma cópia da [asgard-api](https://github.com/B2W-BIT/asgard-api) na mesma pasta onde está clonado o esse código. Isso porque uma das dependências de um plugin da asgard API é a própria Asgard API. A instalação é feita com `pipenv install -e ../asgard-api`. Essa instalação já é feita quando rodamos `pipenv install --dev`.

`$ PYTHONPATH=. py.test --cov=./ --cov-report term-missing -v -s`
