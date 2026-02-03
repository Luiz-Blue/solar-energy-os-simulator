# Solar Energy OS Simulador

### Implementação de Modelos de Produção de Energia Fotovoltaica para Integração com o Simulador Wrench

Autoria: Luiz Fernando dos SantosCarvalho
Instituição: universidade federal do estado do Para (UFPA)
Tipo de Pesquisa: Iniciação Científica



## Descrição do Projeto

O Solar Energy OS Simulator é um projeto que propõe a modelagem e implementação de um sistema de simulação de energia fotovoltaica integrada a um simulador de Data Center , inspirado no simulador **Wrench**.

O objetivo principal é modelar a produção de energia solar e o consumo energético de um data center, permitindo analisar como sistemas computacionais podem ser gerenciados com base na disponibilidade de energia renovável.

Para isso, foi desenvolvido um plugin em Python com Flask, que:

* Simula a geração de energia por **três células fotovoltaicas**;
* Modela o consumo energético de uma máquina computacional;
* Gerencia uma fila de processos simulados;
* Decide se um processo pode ser executado com base na energia disponível;
* Armazena um histórico de monitoramento a cada 5 minutos;
* Expõe endpoints para integração com simuladores como o **Wrench**.

---

## Objetivos do projeto

Os objetivos específicos deste trabalho são:

* Implementar um modelo matemático de produção fotovoltaica;
* Integrar esse modelo a um simulador de escalonamento de processos;
* Monitorar dinamicamente geração e consumo energético;
* Permitir análise comparativa entre produção solar e demanda computacional;
* Criar uma base experimental para estudos futuros testes de maneiras sustentáveis.

---

## Ferramentas Utilizadas

O projeto foi desenvolvido utilizando:

*  Python V3.11
*  Flask (API REST)*
*  Docker e Docker Compose
*  Threads para simulação contínua de energia solar
*  Simulação de processos computacionais
*  Monitoramento via endpoint `/monitor`

---

## Modelo Matemático Implementado

###  Produção de Energia Fotovoltaica

A geração de energia por cada célula solar é modelada por:

[ G_i(t) = I(t) \cdot A_i \cdot \eta ]

Onde:

* ( G_i(t) ) = geração da célula ( i ) no tempo ( t )
* ( I(t) ) = irradiância solar no tempo ( t )
* ( A_i ) = área da célula fotovoltaica ( i )
* ( \eta ) = eficiência do painel

A energia total gerada é:

[ G_{total}(t) = \sum_{i=1}^{3} G_i(t) ]

A energia armazenada na bateria é atualizada por:

[ E(t+1) = \min(E(t) + G_{total}(t), E_{max}) ]

### Consumo Energético do Data Center

O consumo total da máquina é modelado como:

[ L = P_{IT} + \alpha \cdot P_{IT} ]

Onde:

* ( P_{IT} ) = potência computacional da máquina
* ( \alpha ) = fator térmico (overhead de resfriamento)

Se ( E(t) \geq L ), o processo é executado; caso contrário, ele é adiado.

---

##  **Estrutura do Projeto**

```
solar-energy-os-simulator/
│
├── plugin/
│   ├── main.py
│   ├── energy_model.py
│   ├── Dockerfile
│
├── consumer/
│   ├── app.py
│   ├── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## Monitoramento em Tempo Rea**

O simulador disponibiliza os seguintes endpoints:

## Monitoramento Geral

```
http://localhost:5000/monitor
```

Retorna:

* Energia gerada pelas células
* Consumo atual
* Energia armazenada na bateria
* Fila de processos
* Histórico de medições (a cada 5 minutos)

###  Dados das Células Solares

```
http://localhost:5000/solar
```

Retorna:

* Irradiância atual
* Geração individual de cada célula
* Geração total do sistema fotovoltaico

---

##  Como Executar o Projeto

###  Pré-requisitos

* Docker instalado
* Docker Compose instalado

### 🔹 Executando o simulador

No diretório raiz do projeto, execute:

```bash
docker-compose up --build
```
Referencias
Após isso, acesse:

* Monitor: [http://localhost:5000/monitor](http://localhost:5000/monitor)
* Dados solares: [http://localhost:5000/solar](http://localhost:5000/solar)

Matérias apontando o problema dos Data Centers (impactos ambientais e energéticos)

ICL Notícias. Entenda os impactos de data centers. Disponível em:
(https://iclnoticias.com.br/economia/entenda-os-impactos-de-data-centers/)

Comunica UFU. Cientistas alertam: data centers podem causar crise de água e energia. Disponível em:
(https://comunica.ufu.br/noticias/2025/09/cientistas-alertam-data-centers-podem-causar-crise-de-agua-e-energia)

Material de estudo / base teórica

WRENCH Simulator Documentation. Disponível em:
https://wrench-project.org/

Beloglazov, A.; Buyya, R. Energy-efficient resource management in cloud computing. (Base clássica na área).
