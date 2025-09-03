# 🚚 Sistema de Disponibilidade de Motoboys

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> Sistema automatizado para análise de disponibilidade de motoboys durante a semana. Permite selecionar datas específicas e gera relatórios profissionais em Excel e PDF com os motoboys disponíveis (não agendados) para cada data selecionada.

## 📋 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Instalação](#️-instalação)
- [🚀 Uso Rápido](#-uso-rápido)
- [📖 Guia Completo](#-guia-completo)
- [📊 Formato das Planilhas](#-formato-das-planilhas)
- [⚙️ Configuração](#️-configuração)
- [🔧 Solução de Problemas](#-solução-de-problemas)
- [📈 Exemplos de Uso](#-exemplos-de-uso)
- [🤝 Contribuição](#-contribuição)

## ✨ Funcionalidades

### 🎯 Principais Recursos

- **🎨 Interface gráfica intuitiva** com calendário interativo
- **📅 Seleção flexível de datas** para análise personalizada
- **📊 Geração automática de relatórios** em Excel e PDF
- **🔍 Detecção automática** de colunas nas planilhas
- **🎨 Formatação profissional** dos relatórios
- **📱 Suporte a múltiplas datas** simultaneamente
- **⚙️ Sistema de configuração** flexível
- **📝 Logs detalhados** para debugging
- **🔄 Carregamento automático** de dados

### 📊 Relatórios Gerados

- **📈 Planilha Excel** (`Motoboys_Nao_Escalados.xlsx`) com abas separadas por data
- **📄 PDF profissional** (`Motoboys_Nao_Escalados.pdf`) com layout elegante
- **📋 Logs detalhados** (`disponibilidade_motoboys.log`) para auditoria

## 🛠️ Instalação

### 📋 Pré-requisitos

- **Python 3.7+** instalado
- **Planilhas de dados** no formato correto
- **Conexão com internet** (para instalação de dependências)

### 🚀 Instalação Automática (Recomendada)

```bash
# 1. Clone ou baixe o repositório
git clone <url-do-repositorio>
cd disponibilidade-durante-a-semana--main

# 2. Execute o script de inicialização
python iniciar.py
```

O script `iniciar.py` irá:
- ✅ Verificar a versão do Python
- 📦 Instalar dependências automaticamente
- 📁 Criar arquivos de exemplo
- 🚀 Iniciar o sistema

### 🔧 Instalação Manual

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Criar arquivos de exemplo (opcional)
python criar_exemplos.py

# 3. Executar o sistema
python disponibilidade_motoboys.py
```

### 📦 Dependências

| Biblioteca | Versão | Descrição |
|------------|--------|-----------|
| `pandas` | ≥1.5.0 | Manipulação de dados |
| `tkcalendar` | ≥1.6.0 | Calendário interativo |
| `reportlab` | ≥3.6.0 | Geração de PDF |
| `openpyxl` | ≥3.0.0 | Leitura/escrita Excel |
| `xlrd` | ≥2.0.0 | Suporte a .xls |

## 🚀 Uso Rápido

### 1️⃣ **Preparar Dados**
- Coloque `Entregadores.xlsx` na pasta do projeto
- Coloque `Pedidos.xls` na pasta do projeto

### 2️⃣ **Executar Sistema**
```bash
python disponibilidade_motoboys.py
```

### 3️⃣ **Usar Interface**
1. **Selecionar arquivos** (se não carregados automaticamente)
2. **Escolher datas** no calendário (duplo clique)
3. **Gerar relatórios** (botão "Gerar Relatórios")

### 4️⃣ **Resultados**
- 📊 `Motoboys_Nao_Escalados.xlsx` - Planilha com abas por data
- 📄 `Motoboys_Nao_Escalados.pdf` - Relatório PDF profissional

## 📖 Guia Completo

### 🎨 Interface Gráfica

```
┌─────────────────────────────────────────────────────────────────┐
│                Sistema de Disponibilidade de Motoboys           │
├─────────────────────────────────────────────────────────────────┤
│ Arquivos de Dados                                               │
│ Cadastro: [Entregadores.xlsx] [Selecionar]                     │
│ Agendamento: [Pedidos.xls] [Selecionar]                        │
├─────────────────────────────────────────────────────────────────┤
│ Calendário (Duplo clique)    │ Datas Selecionadas              │
│ ┌─────────────────────────┐  │ ┌─────────────────────────────┐ │
│ │        JULHO 2024       │  │ │ 22/07/2024                  │ │
│ │                         │  │ │ 23/07/2024                  │ │
│ │  Su Mo Tu We Th Fr Sa   │  │ │ 24/07/2024                  │ │
│ │                         │  │ └─────────────────────────────┘ │
│ │                         │  │ [Adicionar] [Remover] [Limpar] │
│ └─────────────────────────┘  │                                 │
├─────────────────────────────────────────────────────────────────┤
│ [Gerar Relatórios] [Configurações] [Sair]                      │
└─────────────────────────────────────────────────────────────────┘
```

### 📋 Passo a Passo Detalhado

#### **Passo 1: Preparação dos Dados**
1. **Planilha de Cadastro** (`Entregadores.xlsx`):
   - Deve conter colunas: `Nome`, `Telefone`, `Cidade`, `Bairro`, `CEP`
   - Cada linha representa um motoboy cadastrado

2. **Planilha de Agendamento** (`Pedidos.xls`):
   - Deve conter colunas de entregador e data de agendamento
   - Cada linha representa um agendamento

#### **Passo 2: Execução do Sistema**
1. Execute `python disponibilidade_motoboys.py`
2. A interface gráfica será aberta automaticamente
3. Se os arquivos estiverem na pasta, serão carregados automaticamente

#### **Passo 3: Seleção de Datas**
1. **Duplo clique** em qualquer data no calendário para adicioná-la
2. **Ou** selecione uma data e clique em "Adicionar Data"
3. As datas selecionadas aparecerão na lista à direita
4. Use os botões para gerenciar a lista de datas

#### **Passo 4: Geração de Relatórios**
1. Clique em "Gerar Relatórios"
2. Aguarde a mensagem de sucesso
3. Os arquivos serão salvos na pasta do projeto

## 📊 Formato das Planilhas

### 📋 Entregadores.xlsx

| Nome | Telefone | Cidade | Bairro | CEP |
|------|----------|--------|--------|-----|
| João Silva | 11999999999 | São Paulo | Centro | 01234-567 |
| Maria Santos | 11888888888 | São Paulo | Vila Madalena | 05433-000 |
| Pedro Oliveira | 11777777777 | São Paulo | Moema | 04038-001 |

**Colunas obrigatórias:**
- `Nome` - Nome completo do motoboy
- `Telefone` - Número de telefone (texto)
- `Cidade` - Cidade de atuação
- `Bairro` - Bairro de atuação
- `CEP` - CEP do bairro

### 📋 Pedidos.xls

| Data de Agendamento | Entregador | Cliente | Endereço | Valor |
|---------------------|------------|---------|----------|-------|
| 22/07/2024 08:00 | joão silva | Cliente A | Rua A 123 | 25.50 |
| 22/07/2024 09:30 | maria santos | Cliente B | Rua B 456 | 30.00 |

**Colunas obrigatórias:**
- Coluna com data de agendamento (detectada automaticamente)
- Coluna com nome do entregador (detectada automaticamente)

**Formato de data:** `DD/MM/AAAA HH:MM`

## ⚙️ Configuração

### 📝 Arquivo config.json

```json
{
    "arquivos": {
        "cadastro": "Entregadores.xlsx",
        "agendamento": "Pedidos.xls"
    },
    "planilha": {
        "header_agendamento": 3,
        "colunas_cadastro": ["nome", "telefone", "cidade", "bairro", "cep"],
        "coluna_entregador": "entregador",
        "coluna_data": "data_agendamento"
    },
    "relatorio": {
        "formato_data": "%d/%m/%Y",
        "nome_excel": "Motoboys_Nao_Escalados.xlsx",
        "nome_pdf": "Motoboys_Nao_Escalados.pdf"
    },
    "interface": {
        "titulo": "Sistema de Disponibilidade de Motoboys",
        "largura": 900,
        "altura": 700
    }
}
```

### 🔧 Personalizações Comuns

#### **Ajustar Linha do Cabeçalho**
Se o cabeçalho da planilha `Pedidos.xls` estiver em uma linha diferente:

```json
{
    "planilha": {
        "header_agendamento": 2  // Mude para a linha correta
    }
}
```

#### **Personalizar Colunas do Relatório**
Para incluir/excluir colunas no relatório:

```json
{
    "planilha": {
        "colunas_cadastro": ["nome", "telefone", "cidade", "bairro", "cep", "observacoes"]
    }
}
```

#### **Alterar Nomes dos Arquivos**
Para personalizar os nomes dos relatórios gerados:

```json
{
    "relatorio": {
        "nome_excel": "Relatorio_Disponibilidade.xlsx",
        "nome_pdf": "Relatorio_Disponibilidade.pdf"
    }
}
```

## 🔧 Solução de Problemas

### ❌ Erro: "FileNotFoundError"

**Causa:** Arquivo não encontrado na pasta
**Solução:**
- Verifique se os arquivos estão na pasta do projeto
- Confirme os nomes exatos dos arquivos
- Use a interface para selecionar os arquivos manualmente

### ❌ Erro: "PermissionError: Permission denied"

**Causa:** Arquivo Excel/PDF aberto em outro programa
**Solução:**
- Feche o arquivo `Motoboys_Nao_Escalados.xlsx` se estiver aberto
- Delete o arquivo existente antes de gerar novo
- Verifique se não há outros programas usando os arquivos

### ❌ Erro: "Coluna 'entregador' não encontrada"

**Causa:** Estrutura da planilha diferente do esperado
**Solução:**
- Verifique se a planilha `Pedidos.xls` tem a estrutura correta
- Ajuste a linha do cabeçalho no `config.json`
- Use os arquivos de exemplo como referência

### ❌ Erro: "Biblioteca não encontrada"

**Causa:** Dependências não instaladas
**Solução:**
```bash
pip install -r requirements.txt
```

### ⚠️ Aviso: "Parsing dates in %d/%m/%Y format"

**Causa:** Formato de data brasileiro
**Solução:** O programa já trata automaticamente com `dayfirst=True`

### 🔍 Logs e Debugging

O sistema gera logs detalhados em `disponibilidade_motoboys.log`:

```bash
# Visualizar logs em tempo real
tail -f disponibilidade_motoboys.log

# Visualizar últimos logs
tail -n 50 disponibilidade_motoboys.log
```

## 📈 Exemplos de Uso

### 🎯 Cenário 1: Análise Semanal
```bash
# Objetivo: Ver disponibilidade da semana toda
# Passos:
1. Selecione 7 datas consecutivas (segunda a domingo)
2. Gere relatório para ver disponibilidade da semana toda
3. Analise as abas do Excel para cada dia
```

### 🎯 Cenário 2: Análise de Feriados
```bash
# Objetivo: Verificar disponibilidade em datas específicas
# Passos:
1. Selecione apenas datas importantes (feriados, eventos)
2. Gere relatório focado nessas datas
3. Compare com dias normais
```

### 🎯 Cenário 3: Comparação Mensal
```bash
# Objetivo: Comparar disponibilidade entre períodos
# Passos:
1. Selecione datas do início e fim do mês
2. Compare disponibilidade entre períodos
3. Identifique padrões de disponibilidade
```

### 🎯 Cenário 4: Análise de Capacidade
```bash
# Objetivo: Verificar se há motoboys suficientes
# Passos:
1. Selecione datas de alta demanda
2. Gere relatório de disponíveis
3. Compare com demanda esperada
```

## 📁 Estrutura do Projeto

```
disponibilidade-durante-a-semana--main/
├── 📄 disponibilidade_motoboys.py    # Script principal
├── 🚀 iniciar.py                     # Script de inicialização
├── 📋 criar_exemplos.py              # Gerador de exemplos
├── ⚙️ config.json                    # Configurações
├── 📦 requirements.txt               # Dependências
├── 📖 README.md                      # Este arquivo
├── 📁 exemplos/                      # Arquivos de exemplo
│   ├── 📊 Entregadores_Exemplo.xlsx
│   └── 📊 Pedidos_Exemplo.xlsx
└── 📝 disponibilidade_motoboys.log   # Logs (gerado automaticamente)
```

## 🤝 Contribuição

### 🐛 Reportar Problemas
1. Verifique se o problema já foi reportado
2. Inclua informações detalhadas:
   - Versão do Python
   - Sistema operacional
   - Mensagens de erro completas
   - Passos para reproduzir

### 💡 Sugerir Melhorias
1. Descreva a funcionalidade desejada
2. Explique o benefício para outros usuários
3. Inclua exemplos de uso se possível

### 🔧 Desenvolvimento
1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto é de uso livre para fins comerciais e pessoais.

---

## 🆘 Suporte

### 📞 Contato
- **Issues:** Use a aba Issues do GitHub
- **Documentação:** Consulte este README
- **Exemplos:** Veja a pasta `exemplos/`

### 💡 Dicas
- **Mantenha backup** das planilhas originais
- **Feche arquivos Excel** antes de gerar novos relatórios
- **Use datas específicas** para análises mais precisas
- **Verifique os relatórios** gerados para confirmar os dados
- **Consulte os logs** em caso de problemas

---

**Desenvolvido para otimizar a gestão de disponibilidade de motoboys** 🚚✨

*Versão 2.0 - Sistema completamente reformulado com interface moderna e funcionalidades avançadas*