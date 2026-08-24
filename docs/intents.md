# Cheat Sheet - Intents do Agente Reembolso (v1)

| Intent é a ação de negócio final que o agente executa/comunica.

## Reembolso
| Agente de triagem, responsável por fazer a trigame inicial para validar o reembolso.

### reembolso_solicitar
É o principal fluxo do sistema.

**Objetivo:** O beneficiário quer iniciar um pedido de reembolso

**Exemplos:**
- "Quero solicitar um reembolso."
- "Quero pedir reembolso de uma consulta."
- "Quero solicitar reembolso da minha terapia."
- "Preciso pedir reembolso desse exame."
- "Quero enviar um documento para solicitar reembolso."

**Data inicial:**
```text
{
    carteirinha?
    categoria?
    valor_pago?
    data_atendimento?
    codigo_procedimento?
    finalidade_procedimento?
}
```

**Fluxo provável:**
```plantuml
reembolso solicitar
        ↓
ag_triagem
        ↓
carteirinha?
        ↓
MCP consultar_beneficiario()
        ↓
ag_documento
        ↓
ag_normas
        ↓
decisao
        ↓
MCP abrir_protocolo()
```
### reembolso_simular
**Objetivo:** descobrir se uma despesa provavelmente é elegível sem abir um pedido.

**Exemplos:**
- "Uma consulta médica tem reembolso?"
- "Terapia tem reembolso?"
- "Quanto eu posso receber por esse exame?"
- "Esse procedimento é coberto?"
- "Posso pedir reembolso desse material?"

**Sem carteirinha**
```text
"Consulta médica tem reembolso?"
```
Podemos consultar as normas gerais sem MCP.

**Com carteirinha**
```text
"Com meu plano, quanto eu recebo por terapia?"
```
Ai:
```text
carteirinha -> consultar_beneficiario -> ag_normas
```

### reembolso_consultar

Não consultar histórico sem identificação do beneficiário.

**Exemplo:**
"Qual o status do meu reembolso?"

**Fluxo:**
```text
Tenho a carteirinha?
       │
       ├── NÃO → pedir carteirinha
       │
       └── SIM → consultar_historico(carteirinha)
```

## Documentos

### documento_analisar
**Objetivo:** analisar um documento fornecido pelo beneficiário.

**Exemplos:**
- "Analise esse documento."
- "Veja se esse recibo serve para o reembolso."
- "Confira esse documento."
- "Esse documento está correto?"
- "Leia esse recibo e veja os dados."

o ag_documento produz coisas como:
```text
categoria
valor_pago
data_atendimento
codigo_procedimento
finalidade_procedimento
campos_faltantes
documento_valido
numero_sessao_ano
```

## Normas

### norma_consulta
**Objetivo:** perguntar sobre as regras de reembolso sem necessariamente iniciar um pedido.

Exemplos:

- "Quais documentos preciso para reembolso?"
- "Quais são as regras para terapia?"
- "Qual é o limite de reembolso?"
- "Como funciona o reembolso?"
- "Quais despesas não são cobertas?"

**Fluxo:**
```text
norma_consultar -> ag_normas -> RAG
```

### MCP

### beneficiario_consultar

**Exemplos:**
- "Quero consultar meus dados."
- "Qual é o meu plano?"
- "Qual a minha situação contratual?"
- "Quando comecei no plano?"
- "Quantas sessões de terapia já utilizei?"