Quando Sua IA Não Consegue Explicar Por Que Marcou um Documento
Classificação de segurança chega ao Decompose v0.1.1 — determinística, local, sem LLM.

---

Aqui vai um cenário real. Seu pipeline de IA processa um documento de 200 páginas — um memorial descritivo de engenharia, um contrato, uma especificação técnica. A IA marca o documento como "sensível". Você pergunta: por quê? A resposta: um score de confiança. 0.82. Sem rastreabilidade. Sem justificativa reproduzível.

Você roda de novo. Agora é 0.79. Mesmo documento. Mesmo modelo. Resultado diferente.

Isso não é uma ferramenta. Isso é um cara-ou-coroa.

## O problema com classificação probabilística

Quando você precisa classificar documentos em ambientes de alta confiança — jurídico, engenharia, compliance — a pergunta nunca é "qual o score?". A pergunta é: "por que essa unidade foi classificada assim, e eu consigo reproduzir esse resultado amanhã?"

Modelos de linguagem não respondem essa pergunta. Eles geram probabilidades. Rodam em GPU. Custam por token. E o pior: o resultado muda entre chamadas.

## Decompose v0.1.1: classificação de segurança determinística

Na versão 0.1.1 do Decompose, adicionei a categoria `security` à saída de classificação. Cada unidade semântica do texto agora recebe uma avaliação de risco de segurança — sem LLM, sem API key, sem GPU.

Uma chamada de função. Resultado idêntico toda vez.

```python
from decompose import decompose_text

result = decompose_text(
    "Access credentials for the production database are stored in /etc/secrets/db.key. "
    "The root password was last rotated on 2024-01-15."
)

for unit in result:
    print(f"[{unit['classification']}] risk={unit['risk_score']} | {unit['text'][:80]}")
```

A saída classifica cada unidade semântica com categoria, nível de autoridade e score de risco. A categoria `security` captura referências a credenciais, chaves, endpoints internos, configurações sensíveis — tudo que um pipeline de compliance precisa rastrear.

Determinístico. Mesmo input, mesma saída. Sempre.

## O que mudou na v0.1.1

31 commits. 44 arquivos modificados. As mudanças principais:

- **Categoria `security` na classificação**: nova dimensão de risco aplicada a cada unidade semântica
- **Publicação no ClawHub marketplace**: instalação direta via OpenClaw
- **CONTRIBUTING.md e LICENSE**: o projeto agora tem guia de contribuição e licença formal
- **Open Graph e Twitter Card meta tags**: todas as páginas do site com preview social
- **Documentação atualizada**: links para blog posts no README e SKILL.md

## O que o Decompose não faz

Vou ser direto. O Decompose não entende contexto semântico profundo. Ele não infere que uma frase sobre "rotação de credenciais" implica risco operacional para um sistema específico. Ele classifica padrões estruturais no texto — não faz raciocínio causal.

Se você precisa de inferência contextual, precisa de um LLM. Se precisa de classificação reproduzível, rápida e auditável, o Decompose resolve.

São problemas diferentes. Use a ferramenta certa para cada um.

## Por que classificação determinística importa

Em indústrias reguladas, auditabilidade não é feature — é requisito. Quando um auditor pergunta "por que esse documento foi classificado como sensível?", a resposta precisa ser rastreável até uma regra, não até um peso estatístico em uma rede neural de 70 bilhões de parâmetros.

O Decompose decompõe texto em unidades semânticas e classifica cada uma com categorias, scores de risco, entidades extraídas e flags de irredutibilidade. Tudo local. Tudo determinístico. Sem chamada de rede.

Isso significa que você pode rodar em ambientes air-gapped. Pode integrar em pipelines CI/CD. Pode versionar os resultados no git e comparar diffs entre releases de um documento.

## Instale e teste

```bash
pip install decompose-mcp==0.1.1
```

Para usar como servidor MCP (compatível com Claude, Cursor e outros clientes):

```json
{
  "mcpServers": {
    "decompose": {
      "command": "uvx",
      "args": ["decompose-mcp", "--serve"]
    }
  }
}
```

Ou direto no Python:

```python
from decompose import decompose_text

units = decompose_text("Seu texto aqui.")
print(units)
```

Código aberto. Sem API key. Sem GPU. Uma função.

GitHub: [github.com/echology-io/decompose](https://github.com/echology-io/decompose)
PyPI: [decompose-mcp](https://pypi.org/project/decompose-mcp/)
Site: [echology.io](https://echology.io)