# 📦 Sistema de Conferência e Triagem Logística de Volumes

<p align="center">
  <img src="riopre.png" alt="Logo do Sistema" width="220" />
</p>

<p align="center">
  <strong>Solução web leve, autônoma e inteligente para conferência, triagem por leitor de código de barras e controle de expedição em transportadoras e centros de distribuição.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white" alt="PowerShell" />
</p>

---

## 📌 Sobre o Projeto

Em operações logísticas de **cross-docking** e expedição, a chegada de grandes lotes de volumes de diversos clientes frequentemente gera gargalos operacionais: contagem manual propensa a erros, extravio de volumes e falta de visibilidade em tempo real sobre pendências de carga.

Este projeto foi desenvolvido como **Trabalho de Conclusão de Curso (TCC)** para eliminar esses problemas, oferecendo uma plataforma ágil, com zero necessidade de instalação de banco de dados no terminal de operação (*Client-Side First*), permitindo importação direta de manifestos em planilhas, bipagem rápida por scanner físico e exportação gerencial automatizada.

---

## ✨ Principais Funcionalidades

- **📥 Importação de Manifestos (Excel):**
  Leitura automática de planilhas `.xls` e `.xlsx` com cálculo instantâneo da quantidade esperada de volumes por marca e por cidade.

- **⚡ Triagem Inteligente via Scanner Físico:**
  Algoritmo heurístico baseado em **Expressões Regulares (RegEx)** e padrões de código de barras que identifica automaticamente a marca/cliente a partir da leitura do bipador.

- **🟢 Feedback Visual Imediato (Flash Verde) & Sincronização Multi-Aba:**
  A tela pisca em verde confirmando o registro da caixa sem que o operador precise desviar a atenção da esteira. Utiliza a API `StorageEvent` para sincronizar leituras em tempo real entre abas e monitores secundários.

- **🛡️ Prevenção de Duplicidades & Auditoria Temporal:**
  Valida códigos já lidos na mesma remessa e registra a hora exata (`hh:mm:ss`) de cada bipe.

- **📊 Telas Satélites & Auditoria Individual:**
  Páginas dedicadas para cada uma das mais de 25 marcas (como *Adidas, Fila, Vulcabras, Nakata, Piccadilly, Cambuci*, etc.), permitindo consulta detalhada e exclusão pontual de leituras indevidas.

- **📑 Relatórios Gerenciais Estilizados:**
  Geração em tempo real de planilhas `.xlsx` com formatação condicional (destaque verde para cargas completas e vermelho para pendências), resumo por marcas e detalhes completos.

---

## 🛠️ Stack Tecnológica

| Tecnologia | Finalidade no Projeto |
| :--- | :--- |
| **HTML5 & CSS3** | Estruturação semântica, efeito translúcido (*glassmorphism*) e design responsivo. |
| **Bootstrap 5** | Grid responsivo, componentes visuais, tipografia e badges dinâmicos. |
| **JavaScript (ES6+)** | Lógica de negócio, processamento no navegador, manipulação de DOM e `localStorage`. |
| **SheetJS (`xlsx-js-style`)** | Leitura de romaneios e geração de arquivos Excel estilizados no cliente. |
| **Python** | Scripts de metaprogramação (geração em lote de telas satélites e sanitização UTF-8). |
| **PowerShell** | Scripts de manutenção automatizada e substituição de funções em lote no Windows. |

---

## 🔄 Fluxo de Funcionamento

```text
  [Planilha Manifesto (.xls/.xlsx)]
                 │
                 ▼
       [index.html (Dashboard)]
                 │
                 ├── Leitura do Scanner Físico (Input)
                 ├── Reconhecimento da Marca via RegEx
                 ├── Registro com Timestamp no LocalStorage
                 ├── Disparo do Flash Verde (Multi-Aba)
                 │
                 ├──► [Telas de Marcas Individuais (Auditoria)]
                 │
                 └──► [Exportação de Relatório Geral em Excel (.xlsx)]
```

---

## 🎯 Regras de Identificação de Marcas (Exemplos)

O sistema conta com rotinas de classificação heurística direta no código de barras:

* **Adidas:** 20 dígitos numéricos iniciando com `00000` e contendo `99999`.
* **Vulcabras:** Padrão logístico GS1 com `(00)` ou 30 dígitos começando com `185`.
* **Fila:** 10 caracteres terminando com sufixo `#3`.
* **Dass:** 11 caracteres terminando com sufixo `#15`.
* **Nakata:** 12 caracteres contendo o termo `vol`.
* **Jamef:** Padrão alfanumérico contendo `JAAA` ou prefixo `08J`.
* Demais padrões catalogados para *Piccadilly, Cambuci, Penalty, Pegada, Nautica, Stampa*, etc.

---

## 🚀 Como Executar o Projeto

Por se tratar de uma aplicação baseada em arquitetura **Client-Side**, você não precisa configurar servidores, Node ou banco de dados externo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/daveghmar/transportadora.git
   ```
2. Acesse a pasta do projeto:
   ```bash
   cd transportadora
   ```
3. Abra o arquivo **`index.html`** em qualquer navegador moderno (Google Chrome, Edge, Firefox, etc.).
4. Carregue uma planilha de manifesto de teste (ex: `teste1.xls`) e inicie as leituras!

---

## 📂 Estrutura de Arquivos

```text
├── index.html             # Painel geral de contagem e triagem central
├── adidas.html            # Tela dedicada de auditoria da Adidas
├── vulcabras.html         # Tela dedicada de auditoria da Vulcabras
├── fila.html              # Tela dedicada de auditoria da Fila
├── ...                    # (Mais de 20 páginas HTML dedicadas por marca)
├── generate_pages.py      # Script Python gerador automatizado de páginas HTML
├── generate_pages.js      # Versão Node.js do gerador de páginas
├── patch_export.py        # Script utilitário para atualização em lote do exportador Excel
├── update_excel.ps1       # Script PowerShell para manutenção automatizada no Windows
├── teste1.xls             # Planilha de exemplo para testes de importação
└── riopre.png             # Identidade visual / logotipo do sistema
```

---

## 👨‍💻 Autor

Desenvolvido por **Davi ([@daveghmar](https://github.com/daveghmar))**  
Projeto de Conclusão de Curso (TCC) em Logística e Tecnologia da Informação.
