# 📋 Sistema de Disponibilidade de Motoboys

## 📖 Descrição

Sistema automatizado para análise de disponibilidade de motoboys durante a semana. O programa permite selecionar datas específicas e gera relatórios em Excel e PDF com os motoboys disponíveis (não agendados) para cada data selecionada.

## ✨ Funcionalidades

### 🎯 Principais Recursos
- **Interface gráfica intuitiva** com calendário interativo
- **Seleção flexível de datas** para análise
- **Geração automática de relatórios** em Excel e PDF
- **Detecção automática** de colunas nas planilhas
- **Formatação profissional** dos relatórios
- **Suporte a múltiplas datas** simultaneamente

### 📊 Relatórios Gerados
- **Planilha Excel** (`Motoboys_Nao_Escalados.xlsx`) com abas separadas por data
- **PDF profissional** (`Motoboys_Nao_Escalados.pdf`) com layout elegante

## 🛠️ Requisitos do Sistema

### 📋 Pré-requisitos
- **Python 3.7+** instalado
- **Planilhas de dados** no formato correto
- **Bibliotecas Python** (instaladas automaticamente)

### 📦 Bibliotecas Necessárias
- `pandas` - Manipulação de dados
- `tkinter` - Interface gráfica (incluído no Python)
- `tkcalendar` - Calendário interativo
- `reportlab` - Geração de PDF
- `openpyxl` - Leitura/escrita de arquivos Excel

## 📁 Estrutura de Arquivos

```
disponibilidade-durante-a-semana--main/
├── disponibilidade da semana.py    # Script principal
├── Entregadores.xlsx               # Planilha de cadastro dos motoboys
├── Pedidos.xls                     # Planilha de agendamentos (atualizada constantemente)
├── README.md                       # Este arquivo
├── Motoboys_Nao_Escalados.xlsx     # Relatório Excel gerado
└── Motoboys_Nao_Escalados.pdf      # Relatório PDF gerado
```

## 🚀 Instalação

### 1. **Preparar o Ambiente**
```bash
# Navegar para a pasta do projeto
cd disponibilidade-durante-a-semana--main

# Instalar bibliotecas necessárias
pip install pandas tkcalendar reportlab openpyxl
```

### 2. **Preparar as Planilhas**
- **Entregadores.xlsx**: Deve conter colunas como `Nome`, `Telefone`, `Cidade`, `Bairro`, `CEP`
- **Pedidos.xls**: Deve conter dados de agendamento com colunas de entregador e data

### 3. **Verificar Arquivos**
- Certifique-se de que `Entregadores.xlsx` está na pasta
- Coloque o arquivo `Pedidos.xls` atualizado na pasta antes de executar

## 📖 Como Usar

### 🎯 Execução do Programa
```bash
python "disponibilidade da semana.py"
```

### 📋 Passo a Passo

1. **Iniciar o Programa**
   - Execute o script Python
   - A interface gráfica será aberta automaticamente

2. **Selecionar Datas**
   - **Duplo clique** em qualquer data no calendário para adicioná-la
   - **Ou** selecione uma data e clique em "Adicionar Data"
   - As datas selecionadas aparecerão na lista à direita

3. **Gerenciar Datas**
   - **Adicionar**: Duplo clique no calendário ou botão "Adicionar Data"
   - **Remover**: Selecione uma data na lista e clique "Remover Data"
   - **Limpar**: Clique "Limpar Todas" para remover todas as datas

4. **Gerar Relatórios**
   - Clique em "Gerar Relatório"
   - Aguarde a mensagem de sucesso
   - Os arquivos serão salvos na pasta do projeto

### 🎨 Interface Gráfica

```
┌─────────────────────────────────────────────────────────────┐
│                Seleção de Datas para Análise                │
├─────────────────────┬───────────────────────────────────────┤
│ Calendário          │ Datas Selecionadas                    │
│ (Duplo clique       │ ┌─────────────────────────────────────┐ │
│ para adicionar)     │ │ 22/07/2025                          │ │
│                     │ │ 23/07/2025                          │ │
│ ┌─────────────────┐ │ │ 24/07/2025                          │ │
│ │     JULHO       │ │ └─────────────────────────────────────┘ │
│ │ 2025            │ │ [Adicionar] [Remover] [Limpar Todas]   │
│ │                 │ │                                       │
│ │  Su Mo Tu We    │ │                                       │
│ │  Th Fr Sa       │ │                                       │
│ └─────────────────┘ │                                       │
├─────────────────────┴───────────────────────────────────────┤
│                    [Gerar Relatório] [Sair]                │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Formato das Planilhas

### 📋 Entregadores.xlsx
| Nome | Telefone | Cidade | Bairro | CEP |
|------|----------|--------|--------|-----|
| João Silva | 11999999999 | São Paulo | Centro | 01234-567 |
| Maria Santos | 11888888888 | São Paulo | Vila Madalena | 05433-000 |

### 📋 Pedidos.xls
- **Cabeçalho**: Linha 4 (ajustável no código se necessário)
- **Colunas**: Entregador, Data de agendamento, etc.
- **Formato**: Detectado automaticamente pelo programa

## 🔧 Configurações Avançadas

### 📝 Ajustar Linha do Cabeçalho
Se o cabeçalho da planilha `Pedidos.xls` estiver em uma linha diferente:

```python
# No arquivo disponibilidade da semana.py, linha 25
self.agendamento_df = pd.read_excel(agendamento_path, header=3)  # Mude o número 3
```

### 🎨 Personalizar Colunas
Para incluir/excluir colunas no relatório:

```python
# No arquivo disponibilidade da semana.py, linha 180
colunas_desejadas = [col for col in ['nome', 'telefone', 'cidade', 'bairro', 'cep'] if col in self.cadastro_df.columns]
```

## 🚨 Solução de Problemas

### ❌ Erro: "FileNotFoundError: 'Pedidos.xls'"
**Causa**: Arquivo não encontrado na pasta
**Solução**: 
- Verifique se `Pedidos.xls` está na pasta do projeto
- Confirme o nome exato do arquivo (maiúsculas/minúsculas)

### ❌ Erro: "PermissionError: Permission denied"
**Causa**: Arquivo Excel/PDF aberto em outro programa
**Solução**:
- Feche o arquivo `Motoboys_Nao_Escalados.xlsx` se estiver aberto
- Delete o arquivo existente antes de gerar novo

### ❌ Erro: "Coluna 'entregador' não encontrada"
**Causa**: Estrutura da planilha diferente do esperado
**Solução**:
- Verifique se a planilha `Pedidos.xls` tem a estrutura correta
- Ajuste a linha do cabeçalho se necessário

### ❌ Erro: "Biblioteca não encontrada"
**Causa**: Bibliotecas não instaladas
**Solução**:
```bash
pip install tkcalendar reportlab pandas openpyxl
```

### ⚠️ Aviso: "Parsing dates in %d/%m/%Y format"
**Causa**: Formato de data brasileiro
**Solução**: O programa já trata automaticamente com `dayfirst=True`

## 📈 Exemplos de Uso

### 🎯 Cenário 1: Análise Semanal
1. Selecione 7 datas consecutivas (segunda a domingo)
2. Gere relatório para ver disponibilidade da semana toda

### 🎯 Cenário 2: Análise Específica
1. Selecione apenas datas importantes (feriados, eventos)
2. Gere relatório focado nessas datas

### 🎯 Cenário 3: Comparação Mensal
1. Selecione datas do início e fim do mês
2. Compare disponibilidade entre períodos

## 🔄 Atualizações

### 📅 Atualizar Dados
- **Entregadores.xlsx**: Atualize quando houver novos cadastros
- **Pedidos.xls**: Substitua sempre que houver novos agendamentos

### 🔧 Atualizar Script
- O script detecta automaticamente mudanças nas planilhas
- Não é necessário reconfigurar após atualizações

## 📞 Suporte

### 🐛 Reportar Problemas
Se encontrar algum erro:
1. Verifique se todos os arquivos estão na pasta correta
2. Confirme se as bibliotecas estão instaladas
3. Verifique o formato das planilhas
4. Execute novamente o script

### 💡 Dicas
- **Mantenha backup** das planilhas originais
- **Feche arquivos Excel** antes de gerar novos relatórios
- **Use datas específicas** para análises mais precisas
- **Verifique os relatórios** gerados para confirmar os dados

## 📄 Licença

Este projeto é de uso livre para fins comerciais e pessoais.

---

**Desenvolvido para otimizar a gestão de disponibilidade de motoboys** 🚚✨