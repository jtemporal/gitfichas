# Contributing Guide | Guia de Contribuição

| Table of content | Índice |
| ------- | --------- |
| &nbsp;&nbsp;• [Before You Start](#before-you-start)<br>&nbsp;&nbsp;• [Code of Conduct](#code-of-conduct)<br>&nbsp;&nbsp;• [Cards Types](#cards-types)<br>&nbsp;&nbsp;• [File Naming Convention](#file-naming-convention)<br>&nbsp;&nbsp;• [Running the Project](#running-the-project)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Local way](#local-way)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Install dependencies](#install-dependencies)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Run the project](#run-the-project)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Docker way](#docker-way)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Building image](#building-image)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Serving](#serving)<br>&nbsp;&nbsp;• [Working with Mermaid Diagrams](#working-with-mermaid-diagrams)<br>&nbsp;&nbsp;• [The Basics of Contributing](#the-basics-of-contributing)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [The Git basics](#the-git-basics)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Issue Assignment](#issue-assignment) | &nbsp;&nbsp;• [Antes de Começar](#antes-de-começar)<br>&nbsp;&nbsp;• [Código de Conduta](#código-de-conduta)<br>&nbsp;&nbsp;• [Tipos de Fichas](#tipos-de-fichas)<br>&nbsp;&nbsp;• [Convenção de Nomes de Arquivos](#convenção-de-nomes-de-arquivos)<br>&nbsp;&nbsp;• [Rodando o Projeto](#rodando-o-projeto)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Localmente](#localmente)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Instalando depedências](#instalando-depedências)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Rodar o projeto](#rodar-o-projeto)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Com Docker](#com-docker)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Montando a imagem](#montando-a-imagem)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Servindo](#servindo)<br>&nbsp;&nbsp;• [Trabalhando com Diagramas Mermaid](#trabalhando-com-diagramas-mermaid)<br>&nbsp;&nbsp;• [Fazendo Contribuições](#fazendo-contribuições)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [O básico de git](#o-básico-de-git)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Atribuição de issues](#atribuição-de-issues) |

## Before You Start

Thank you for wanting to contribute to GitFichas | GitStudyCards. Here you'll find most of the information you'll need for contributing.

**🚀 Quick Setup:** Before you begin, run the setup script to install all required dependencies:

```bash
bash scripts/setup.sh
```

This script will automatically configure your development environment with all necessary tools including Node.js dependencies, Python packages, and Mermaid diagram generation capabilities.

If you have any questions create an issue.

## Code of Conduct

GitFichas is a welcoming and inclusive space for everyone. All contributors are expected to follow our [Code of Conduct](https://github.com/jtemporal/gitfichas/blob/main/CONTRIBUTING.md). Please take a moment to read it and help us maintain a positive environment for all.

[Read the full Code of Conduct](https://github.com/jtemporal/gitfichas/blob/main/CONTRIBUTING.md).

## Cards Types

There are two types of cards:

1. **Command**: explain a command such as "git add -p" or "git commit --allow-empty";
2. **Concept**: explain git and versioning related concepts such as "pull requests" and "conflicts";

Here's a list of all fields you could find in both types:

| Front-Matter Key | Concept Card | Command Card | Description |
| ---------------- | ------------ | ------------ | ----------- |
| `layout` | `mandatory` | `mandatory` | always `post` |
| `pretitle` | `optional` | `optional` | Text before the main part of the card title |
| `title` | `mandatory` | `mandatory` |  Main part of the card title  |
| `subtitle` | `optional` | `optional` | Text after the main part of the card title |
| `command` | - | `mandatory` | Spelled out content e.g.: `git init` |
| `descriptors` | `mandatory` | `mandatory` | Section with the descriptions for each part of the command |
| `descriptors.command` | - | `optional` | Description of the command |
| `descriptors.part{}` | - | `optional` | Decription for the extra bits of a command (e.g.: flags). Each extra part will called "part" followed by the index |
| `concept` | `mandatory` | - | Always `true` |
| `parts` | `mandatory` | - | Section with the descriptions for the concept |
| `parts.part{}` | `mandatory` | - | Descriptions for the concept that can be broken down in blocks each called part followed by the index |
| `info` | `optional` | `optional` | Extra information for a card. |
| `author` | `mandatory` | `mandatory` | GitHub username of person who created the card e.g.: `@jtemporal` |
| `number` | `mandatory` | `mandatory` |  Number of the card e.g.: `"001"`. Quotes are necessary for the leading zero |
| `mermaid` | `mandatory` | `mandatory` |  Always `true` |
| `use_static_image` | `mandatory*` | `mandatory*` | Always `true` when SVG image is generated. *Only required if an SVG file is created for the card |
| `permalink` |  `mandatory` | `mandatory` |  Follows `/projects/{number}` for pt cards, `/en/{number}` for en cards, and `/es/{number}` for es cards |
| `lang` | `mandatory` | `mandatory` | Either `"pt"`, `"en"`, or `"es"`. These are the currently supported languages |
| `translations` | `optional` | `optional` |  Array of translation links e.g.: `- lang: en` `url: /en/{number}` `- lang: es` `url: /es/{number}` |
| `pv` | `mandatory` | `mandatory` | information about the previous card for arrow linking |
| `pv.url` | `mandatory` | `mandatory` | Path to previous card e.g.: `/projects/{number}` |
| `pv.title` | `mandatory` | `mandatory` | Command to previous card e.g.: `#001 git init` |
| `nt` | `mandatory` | `mandatory` | information about the next card for arrow linking |
| `nt.url` | `mandatory` | `mandatory` | Path to next card e.g.: `/projects/{number}` |
| `nt.title` | `mandatory` | `mandatory` | Command to next card e.g.: `#001 git init` |

## File Naming Convention

**IMPORTANT:** All post files must follow the Jekyll naming convention: `YYYY-MM-DD-XXX.md`

### For New Cards
- Format: `YYYY-MM-DD-XXX.md` where XXX is the card number with leading zeros
- Use the current date when creating a new card
- Example: `2024-10-26-054.md` for card #054

### For Translations
- **Must use the SAME date as the original post**
- Portuguese (original): `2024-10-26-054.md` → English: `2024-10-26-054.md` → Spanish: `2024-10-26-054.md`
- Check the original post's filename to get the correct date
- **Never use a different date for translations**

### Directory Structure
- Portuguese cards: `_posts/YYYY-MM-DD-XXX.md`
- English cards: `en/_posts/YYYY-MM-DD-XXX.md`
- Spanish cards: `es/_posts/YYYY-MM-DD-XXX.md`

### Command Cards Example

Command cards have this structure:

```yaml
---
layout: post
pretitle:
title: Renaming
subtitle: a file
command: git mv source target
descriptors:
  - command: command to\nmove files
  - part1: current file name
  - part2: new file name
info: this command can be used to move files between folders
author: "@jtemporal"
number: "052"
mermaid: true
use_static_image: true
translations:
- lang: pt
  url: /projects/052
permalink: "/en/052"
lang: "en"
pv:
  url: "/en/051"
  title: "#051 git commit --allow-empty"
nt:
  url: "https://gitfichas.com/en"
  title: "GitStudyCards | GitFichas"
---

{% include mermaid-graphs.html %}
```

### Concept Cards Example

Command cards have this front-matter structure:

```yaml
---
layout: post
pretitle: What is a
title: conflict
subtitle:
concept: true
parts:
  - part1: it happens when two or more changes are made to the\n same chunk of a file and git doesn't know\nhow to apply the most recent change
  - part2: conflicts are indicated by the markers >>> === <<<
number: "030"
author: "@jtemporal"
mermaid: true
use_static_image: true
permalink: "/en/030"
translations:
- lang: pt
  url: /projects/030
lang: "en"
pv:
  url: "/en/029"
  title: "#029 git restore --staged nome"
nt:
  url: "/en/031"
  title: "#031 git commit --amend"
---

{% include mermaid-graphs.html %}
```

## Running the Project

The website runs on Jekyll but it is prepared to run on docker as well (although it has been a while since I used it for development).

### Devcontainer way (Recommended)

The fastest way to get started is using the provided devcontainer configuration:

1. **Open in GitHub Codespace or VS Code with Dev Containers extension**
2. **Automatic Setup**: Dependencies are installed automatically via `.devcontainer/devcontainer.json`
3. **Jekyll + Mermaid Ready**: Both Jekyll and Mermaid SVG generation are pre-configured

The devcontainer includes:
- Ruby and Jekyll dependencies
- Node.js and Mermaid CLI
- Python scripts for SVG generation
- All system dependencies for headless Chrome

### Local way

Install [Bundler](https://bundler.io/guides/getting_started.html) follow the steps below.

#### Install dependencies

```console
bundle install
```

#### Run the project

```console
bundle exec jekyll s
```

### Docker way

#### Building image

```console
docker build -t gitfichas .
```

#### Serving

```console
docker run --rm --volume="$PWD:/srv/jekyll"  -p 4001:4000 -it gitfichas jekyll serve --livereload
```

## Working with Mermaid Diagrams

GitFichas uses Mermaid diagrams for visualizing Git concepts and commands. The project includes scripts to generate static SVG images from these diagrams.

> 📖 **For detailed technical information** about the Mermaid conversion system, see the [Mermaid Converter README](MERMAID_CONVERTER_README.md).

### Image Generation Scripts

The project includes Python scripts in the `scripts/` folder:

- **`scripts/generate_images_only.py`**: Main script for generating SVG images from Mermaid diagrams
- **`scripts/generate_embedded_fonts.py`**: Utility script for embedding fonts into CSS (run when fonts need updating)
- **`scripts/setup.sh`**: Automated setup script for new codespaces (installs dependencies and configures the environment)

> 💡 **New to the project?** Run `scripts/setup.sh` to automatically set up all dependencies and test the environment.

### Development Workflow

When working on cards with Mermaid diagrams:

1. **Add/edit your Mermaid diagram** in the post's front matter
2. **Generate SVG images** for your changes:
   ```bash
   # Generate images for all posts
   python3 scripts/generate_images_only.py

   # Generate images for specific post (faster for testing)
   python3 scripts/generate_images_only.py "053.md"

   # Force regeneration of existing images
   python3 scripts/generate_images_only.py --force
   ```
3. **Test locally** using Jekyll serve to see both interactive and static versions
4. **Commit both** the post changes and generated SVG files

### Font Management

The project uses embedded Google Fonts (Chilanka and Borel) for consistent rendering. If you need to update fonts:

1. **Generate new embedded fonts**:
   ```bash
   python3 scripts/generate_embedded_fonts.py
   ```
2. **Regenerate all SVG images** to use the new fonts:
   ```bash
   python3 scripts/generate_images_only.py --force
   ```

### CSS Architecture

The project uses a separated CSS architecture:
- **`assets/css/mermaid.css`**: Web-specific styles for interactive diagrams
- **`assets/css/embedded-svg.css`**: SVG-specific styles with embedded fonts
- **`assets/css/embedded-fonts.css`**: Base64-embedded font definitions (auto-generated)

### Theme Configuration

Mermaid theme settings are stored in `gitfichas-mermaid-theme.json` for consistent SVG generation.

## Migrating Cards from Images to Mermaid with Copilot

GitFichas is migrating from image-based cards to dynamic Mermaid diagrams. This guide helps you use GitHub Copilot for efficient migration.

### Quick Migration Examples

**Before (Image-based):**
```markdown
---
layout: post
title: '#002 git add file.txt'
image: "https://res.cloudinary.com/.../thumbnail.jpg"
---
##### Adding files to a commit
<img src="...">
| Command | Description |
| `add` | Command to add files |
```

**After (Mermaid):**
```markdown
---
layout: post
title: Adding
subtitle: files to a commit
command: git add file.txt
descriptors:
  - command: command to add files<br>to staging
  - part1: name of the file
author: "@jtemporal"
number: "002"
mermaid: true
use_static_image: true
---
{% include mermaid-graphs.html %}
```

### Copilot Migration Prompts

**Setup Prompt:**
```
Migrate this GitFichas card from image to Mermaid format:
[paste old card]

Requirements:
- Extract title → pretitle/title/subtitle
- Convert table → descriptors array
- Add: author, number, mermaid: true
- Keep navigation links intact
- Remove image URLs and HTML
- Follow proper file naming: YYYY-MM-DD-XXX.md (use same date as original for translations)
```

**For Command Cards:** Add `command: git xxx` and `descriptors` with `command` + `part1`, `part2`, etc.

**For Concept Cards:** Use `concept: true` and `parts` array instead of `descriptors`. Add `use_static_image: true` only after SVG is generated.

### Migration Workflow

1. **Migrate with Copilot** using prompts above
2. **Ensure proper file naming**: Use `YYYY-MM-DD-XXX.md` format with same date as original post for translations
3. **Generate SVG:** `python3 scripts/generate_images_only.py "filename.md"`
4. **Add `use_static_image: true`** to front matter only after successful SVG generation
5. **Test locally:** `bundle exec jekyll serve`
6. **Commit both files:** `git add post.md svg-file.svg`

### Key Patterns

- **Line breaks:** Use `<br>` in command descriptors, `\n` in concept parts
- **Long descriptions:** Break at ~30 characters without splitting words
- **Title extraction:** `"#042 git rebase -i HEAD~3"` → `pretitle: "Interactive"`, `title: "Rebase"`, `subtitle: "for last 3 commits"`

### Quality Checklist

- [ ] Content matches original card
- [ ] SVG generates successfully
- [ ] Navigation links preserved
- [ ] No trailing whitespaces

## The Basics of Contributing

All contributions are welcome. ☺️

I wrote this [blog post that has a detailed step-by-step on how to make pull requests](https://jtemporal.com/making-pull-requests-with-github-codespaces/) for this project.

There are a bunch of issues already open, you can either work on one of them or you can add to the project based on your experience and usage.

Ideally you can discuss the topic via a issue before you start working.

[_Shout out to Serenata de Amor for having a great contributing guide that inspired this one_](https://github.com/okfn-brasil/serenata-de-amor/blob/main/CONTRIBUTING.md).

### The Git basics

[**1. _Fork_ this repository**](https://github.com/jtemporal/gitfichas/fork)

**2. Clone your fork of the repository**

```console
git clone http://github.com/<YOUR-GITHUB-USERNAME>/gitfichas.git
```

**3. Create a feature branch**

```console
git switch -c <YOUR-GITHUB-USERNAME>-<description-or-issue-number>
```

Please, note that we prefix branch names with GitHub usernames, this helps us in keeping track of changes and who is working on them.

**4. Do what you do best**

Now it's your time to shine and write meaningful code to raise the bar of the project!

**5. Commit your changes**

```console
git commit -m '<Add the description of your changes>'
```

Aim to have small changes per commit that way is easier to understand what you are making when reviewing your pull request.

**6. Push to the branch to your fork**

```consle
git push -u origin <YOUR-GITHUB-USERNAME>-<description-or-issue-number>
```

**7. Create a new _Pull Request_**

From your fork at GitHub usually there is a button to open pull requests.

Remember to [link your issue in your pull request](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

### Issue Assignment

To keep things running smoothly and fair for everyone:

* **Only core maintainers assign issues:** If you’d like to work on something, just drop a comment saying you’re picking it up and go ahead with your PR. No assignment needed!
* **No assignments for potential contributors:** This helps us welcome all contributions and keeps the contribution process open.
* **2-day window:** If there’s no PR within 2 days of a comment expressing interest, the issue is open for anyone to jump in.

This way, we keep a friendly, low-barrier process and ensure issues don’t get blocked. Thanks for being part of the community!

---

## Antes de Começar

Obrigada por querer contribuir com o GitFichas. Aqui você encontrará a maioria das informações que precisará para contribuir.

**🚀 Configuração Rápida:** Antes de começar, execute o script de configuração para instalar todas as dependências necessárias:

```bash
bash scripts/setup.sh
```

Este script configurará automaticamente seu ambiente de desenvolvimento com todas as ferramentas necessárias, incluindo dependências Node.js, pacotes Python e capacidades de geração de diagramas Mermaid.

Se tiver alguma dúvida, crie uma issue.

## Código de Conduta

O GitFichas é um espaço acolhedor e inclusivo para todas pessoas. Isso quer dizer que devemos seguir nosso [Código de Conduta](https://github.com/jtemporal/gitfichas/blob/main/CONTRIBUTING.md). Por favor, leia-o com atenção antes de contribuir.

[Leia o Código de Conduta completo](https://github.com/jtemporal/gitfichas/blob/main/CONTRIBUTING.md).

## Tipos de Fichas

Existem dois tipos de fichas:

1. **Comando**: explica um comando como "git add -p" ou "git commit --allow-empty";
2. **Conceito**: explica conceitos relacionados ao git e versionamento, como "pull requests" e "conflitos";

Aqui está uma lista de todos os campos que você pode encontrar em ambos os tipos:

| Chave Front-Matter | Ficha de Conceito | Ficha de Comando | Descrição |
| ---------------- | ------------ | ------------ | ----------- |
| `layout` | `obrigatório` | `obrigatório` | Sempre presente `post` |
| `pretitle` | `opcional` | `opcional` | Texto antes da parte principal do título da ficha |
| `title` | `obrigatório` | `obrigatório` | Parte principal do título da ficha |
| `subtitle` | `opcional` | `opcional` | Texto após a parte principal do título da ficha |
| `command` | - | `obrigatório` | Comando escrito por extenso, por exemplo: `git init` |
| `descriptors` | `obrigatório` | `obrigatório` | Seção com as descrições para cada parte do comando |
| `descriptors.command` | - | `opcional` | Descrição do comando |
| `descriptors.part{}` | - | `opcional` | Descrição das partes extras de um comando (por exemplo: opções). Cada parte extra será chamada de "part" seguida pelo índice |
| `concept` | `obrigatório` | - | Sempre presente `true` |
| `parts` | `obrigatório` | - | Seção com as descrições para o conceito |
| `parts.part{}` | `obrigatório` | - | Descrições para o conceito que podem ser divididas em blocos, cada um chamado de part seguido pelo índice |
| `info` | `opcional` | `opcional` | Informação extra para uma ficha. |
| `author` | `obrigatório` | `obrigatório` | Nome de usuário do GitHub da pessoa que criou a ficha, por exemplo: `@jtemporal` |
| `number` | `obrigatório` | `obrigatório` | Número da ficha, por exemplo: `"001"`. As aspas são necessárias para o zero à esquerda |
| `mermaid` | `obrigatório` | `obrigatório` | Sempre presente `true` |
| `use_static_image` | `obrigatório*` | `obrigatório*` | Sempre `true` quando imagem SVG é gerada. *Obrigatório apenas se um arquivo SVG for criado para a ficha |
| `permalink` | `obrigatório` | `obrigatório` | Segue `/projects/{number}` para fichas em pt, `/en/{number}` para fichas em en, e `/es/{number}` para fichas em es |
| `lang` | `obrigatório` | `obrigatório` | `"pt"`, `"en"`, ou `"es"`. Estes são os idiomas atualmente suportados |
| `translations` | `opcional` | `opcional` | Array de links de tradução, por exemplo: `- lang: en` `url: /en/{number}` `- lang: es` `url: /es/{number}` |
| `pv` | `obrigatório` | `obrigatório` | Informação sobre a ficha anterior para linkagem com setas |
| `pv.url` | `obrigatório` | `obrigatório` | Caminho para a ficha anterior, por exemplo: `/projects/{number}` |
| `pv.title` | `obrigatório` | `obrigatório` | Comando da ficha anterior, por exemplo: `#001 git init` |
| `nt` | `obrigatório` | `obrigatório` | Informação sobre a próxima ficha para linkagem com setas |
| `nt.url` | `obrigatório` | `obrigatório` | Caminho para a próxima ficha, por exemplo: `/projects/{number}` |
| `nt.title` | `obrigatório` | `obrigatório` | Comando da próxima ficha, por exemplo: `#001 git init` |

### Exemplo de Ficha de Comando

Fichas de comando têm esta estrutura:

```yaml
---
layout: post
pretitle:
title: Renomeando
subtitle: um arquivo
command: git mv origem destino
descriptors:
  - command: comando para \nmover arquivos
  - part1: nome atual \ndo arquivo
  - part2: novo nome \ndo arquivo
info: esse comando pode ser usado \npara mover arquivos entre pastas
number: "052"
author: "@jtemporal"
mermaid: true
use_static_image: true
permalink: "/projects/052"
lang: "pt"
translations:
- lang: en
  url: /en/052
pv:
  url: "/projects/051"
  title: "#051 git commit --allow-empty"
nt:
  url: "/projects/053"
  title: "#053 git log --all --grep='palavra'"
---

{% include mermaid-graphs.html %}
```

### Exemplo de Ficha de Conceito

Fichas de comando têm esta estrutura de front-matter:

```yaml
---
layout: post
pretitle: O que é um
title: conflito
subtitle:
concept: true
parts:
  - part1: acontece quando duas ou mais alterações são realizadas\nno mesmo pedaço de um arquivo e o git\nnão sabe como aplicar a alteração mais recente
  - part2: conflitos são indicados pelos marcadores \n >>>  === e <<<
number: "030"
author: "@jtemporal"
mermaid: true
use_static_image: true
permalink: "/projects/030"
translations:
- lang: en
  url: /en/030
lang: "pt"
pv:
  url: "/projects/029"
  title: "#029 git restore --staged nome"
nt:
  url: "/projects/031"
  title: "#031 git commit --amend"
---

{% include mermaid-graphs.html %}
```

## Convenção de Nomes de Arquivos

**IMPORTANTE:** Todos os arquivos de posts devem seguir a convenção de nomenclatura do Jekyll: `YYYY-MM-DD-XXX.md`

### Para Fichas Novas
- Formato: `YYYY-MM-DD-XXX.md` onde XXX é o número da ficha com zeros à esquerda
- Use a data atual ao criar uma nova ficha
- Exemplo: `2024-10-26-054.md` para a ficha #054

### Para Traduções
- **Deve usar a MESMA data do post original**
- Português (original): `2024-10-26-054.md` → Inglês: `2024-10-26-054.md` → Espanhol: `2024-10-26-054.md`
- Verifique o nome do arquivo do post original para obter a data correta
- **Nunca use uma data diferente para traduções**

### Estrutura de Diretórios
- Fichas em português: `_posts/YYYY-MM-DD-XXX.md`
- Fichas em inglês: `en/_posts/YYYY-MM-DD-XXX.md`
- Fichas em espanhol: `es/_posts/YYYY-MM-DD-XXX.md`

## Rodando o Projeto

O site é executado no Jekyll, mas também está preparado para rodar no Docker (embora já faz um tempo desde que eu usei o Dockerfile para desenvolvimento).

### Com Devcontainer (Recomendado)

A maneira mais rápida de começar é usando a configuração de devcontainer fornecida:

1. **Abra no GitHub Codespace ou VS Code com extensão Dev Containers**
2. **Configuração Automática**: Dependências são instaladas automaticamente via `.devcontainer/devcontainer.json`
3. **Jekyll + Mermaid Prontos**: Tanto Jekyll quanto geração de SVG Mermaid estão pré-configurados

O devcontainer inclui:
- Ruby e dependências do Jekyll
- Node.js e Mermaid CLI
- Scripts Python para geração de SVG
- Todas as dependências do sistema para Chrome headless

### Localmente

Instale o [Bundler](https://bundler.io/guides/getting_started.html) e siga os passos abaixo.

#### Instalando depedências

```console
bundle install
```

#### Rodar o projeto

```console
bundle exec jekyll s
```

### Com Docker

#### Montando a imagem

```console
docker build -t gitfichas .
```

#### Servindo

```console
docker run --rm --volume="$PWD:/srv/jekyll"  -p 4001:4000 -it gitfichas jekyll serve --livereload
```

## Trabalhando com Diagramas Mermaid

GitFichas usa diagramas Mermaid para visualizar conceitos e comandos Git. O projeto inclui scripts para gerar imagens SVG estáticas desses diagramas.

> 📖 **Para informações técnicas detalhadas** sobre o sistema de conversão Mermaid, veja o [Mermaid Converter README](MERMAID_CONVERTER_README.md).

### Scripts de Geração de Imagens

O projeto inclui scripts Python na pasta `scripts/`:

- **`scripts/generate_images_only.py`**: Script principal para gerar imagens SVG dos diagramas Mermaid
- **`scripts/generate_embedded_fonts.py`**: Script utilitário para incorporar fontes no CSS (execute quando as fontes precisarem ser atualizadas)
- **`scripts/setup.sh`**: Script automatizado de configuração para novos codespaces (instala dependências e configura o ambiente)

> 💡 **Novo no projeto?** Execute `scripts/setup.sh` para configurar automaticamente todas as dependências e testar o ambiente.

### Fluxo de Desenvolvimento

Ao trabalhar em fichas com diagramas Mermaid:

1. **Adicione/edite seu diagrama Mermaid** no front matter do post
2. **Gere imagens SVG** para suas mudanças:
   ```bash
   # Gerar imagens para todos os posts
   python3 scripts/generate_images_only.py

   # Gerar imagens para post específico (mais rápido para testes)
   python3 scripts/generate_images_only.py "053.md"

   # Forçar regeneração de imagens existentes
   python3 scripts/generate_images_only.py --force
   ```
3. **Teste localmente** usando Jekyll serve para ver as versões interativas e estáticas
4. **Comite tanto** as mudanças do post quanto os arquivos SVG gerados

### Gerenciamento de Fontes

O projeto usa Google Fonts incorporadas (Chilanka e Borel) para renderização consistente. Se você precisar atualizar as fontes:

1. **Gere novas fontes incorporadas**:
   ```bash
   python3 scripts/generate_embedded_fonts.py
   ```
2. **Regenere todas as imagens SVG** para usar as novas fontes:
   ```bash
   python3 scripts/generate_images_only.py --force
   ```

### Arquitetura CSS

O projeto usa uma arquitetura CSS separada:
- **`assets/css/mermaid.css`**: Estilos específicos para web para diagramas interativos
- **`assets/css/embedded-svg.css`**: Estilos específicos para SVG com fontes incorporadas
- **`assets/css/embedded-fonts.css`**: Definições de fontes em base64 incorporadas (gerado automaticamente)

### Configuração de Tema

As configurações do tema Mermaid estão armazenadas em `gitfichas-mermaid-theme.json` para geração consistente de SVG.

## Migrando Fichas de Imagens para Mermaid com Copilot

O GitFichas está migrando de fichas baseadas em imagens para diagramas Mermaid dinâmicos. O GitHub Copilot pode ajudar a agilizar esse processo de migração com os prompts e fluxo de trabalho corretos.

### Visão Geral da Migração

A migração envolve converter fichas antigas baseadas em imagens para o novo formato Mermaid, preservando a precisão do conteúdo e links de navegação.

#### Antes (formato baseado em imagem):
```markdown
---
layout: post
title: '#002 git add arquivo.txt'
image: "https://res.cloudinary.com/.../thumbnail.jpg"
permalink: "/projects/002"
lang: "pt"
---
##### Adicionando arquivos para commit

<img alt="..." src="https://res.cloudinary.com/.../full.jpg">

| Comando | Descrição |
|---------|-------------|
| `add` | Comando para adicionar arquivos em staging |
| `arquivo.txt` | Nome do arquivo |
```

#### Depois (formato Mermaid):
```markdown
---
layout: post
pretitle:
title: Adicionando
subtitle: arquivos para commit
command: git add arquivo.txt
descriptors:
  - command: comando para adicionar arquivos<br>em staging
  - part1: nome do arquivo
author: "@jtemporal"
number: "002"
mermaid: true
use_static_image: true
permalink: "/projects/002"
lang: "pt"
---

{% include mermaid-graphs.html %}
```

### Fluxo de Trabalho de Migração com Copilot

#### 1. **Prompt de Configuração Inicial**
Use este prompt para preparar o Copilot para migração:

```
Estou migrando fichas do GitFichas do formato baseado em imagens para diagramas Mermaid.
Ajude-me a converter fichas existentes seguindo estes requisitos:
- Extrair componentes do título em pretitle/title/subtitle
- Converter tabelas de comandos em array descriptors
- Adicionar campos obrigatórios: author, number, mermaid: true
- Preservar todos os links de navegação e traduções
- Remover URLs de imagens e conteúdo HTML
- Seguir convenção de nomes: YYYY-MM-DD-XXX.md (usar mesma data do original para traduções)
```

#### 2. **Prompts para Migração Ficha por Ficha**

**Para Fichas de Comando:**
```
Converta esta ficha de comando GitFichas para formato Mermaid:
[cole o conteúdo da ficha antiga]

Siga esta estrutura:
- Extrair comando do título
- Dividir descriptors em command + part1, part2, etc.
- Usar <br> para quebras de linha em descriptors maiores que 30 caracteres
- Adicionar campos de metadados faltantes
- Manter toda navegação intacta
```

**Para Fichas de Conceito:**
```
Converta esta ficha de conceito GitFichas para formato Mermaid:
[cole o conteúdo da ficha antiga]

Siga esta estrutura:
- Usar concept: true em vez de command
- Converter descrições em array parts (part1, part2, etc.)
- Usar \n para quebras de linha em partes de conceito
- Adicionar `use_static_image: true` apenas se um SVG for gerado com sucesso
- Manter toda navegação intacta
```

#### 3. **Prompts de Validação**

**Validação de Estrutura:**
```
Revise esta ficha GitFichas migrada para precisão:
[cole a ficha migrada]

Verificar:
- Todos os campos obrigatórios presentes
- Estrutura adequada de descriptor/parts
- Links de navegação preservados
- Idioma e permalink corretos
- Quebras de linha formatadas adequadamente
```

### Processo de Migração Passo a Passo

#### 1. **Preparar a Migração**
```bash
# Verificar estrutura atual da ficha
git status

# Criar uma branch de feature
git switch -c migrate-cards-[numeros-das-fichas]
```

#### 2. **Migrar com Copilot**
- Abrir o arquivo da ficha antiga
- Usar os prompts de migração acima com Copilot
- Revisar e refinar o conteúdo gerado
- Garantir que todos os campos estejam formatados corretamente

#### 3. **Verificar Convenção de Nomes**
- Garantir formato `YYYY-MM-DD-XXX.md`
- Para traduções, usar a MESMA data do post original
- Verificar se o arquivo está no diretório correto

#### 4. **Gerar Arquivos SVG**
```bash
# Gerar SVG para ficha específica
python3 scripts/generate_images_only.py "nome-arquivo-ficha.md"

# Verificar se a geração foi bem-sucedida
ls -la assets/img/mermaid/ | grep "numero-ficha"
```

#### 5. **Adicionar use_static_image após SVG**
- Adicionar `use_static_image: true` ao front matter APENAS após geração bem-sucedida do SVG

#### 6. **Testar e Verificar**
```bash
# Iniciar servidor local
bundle exec jekyll serve

# Visitar a URL da ficha migrada
# Comparar com a versão original da imagem
# Verificar precisão do conteúdo e consistência visual
```

#### 7. **Fazer Commit das Mudanças**
```bash
# Adicionar ao stage tanto arquivos markdown quanto SVG
git add _posts/nome-arquivo-ficha.md assets/img/mermaid/numero-ficha.svg

# Commit com mensagem descritiva
git commit -m "Migrar ficha XXX de imagem para formato Mermaid

- Converter [título original] para nova estrutura
- Preservar toda navegação e traduções
- Gerar SVG estático para fallback"
```

### Lista de Verificação de Qualidade da Migração

Antes de fazer commit de uma ficha migrada, verificar:

- [ ] Conteúdo reflete com precisão a ficha original
- [ ] Links de navegação preservados e funcionando
- [ ] SVG gera com sucesso
- [ ] Sem espaços em branco finais nos arquivos

## Fazendo Contribuições

Todas as contribuições são bem-vindas. ☺️

Eu escrevi esse [blog post que tem o passo a passo detalhado de como fazer pull requests](https://jtemporal.com/fazendo-pull-requests-com-github-codespaces/) para esse projeto.

Existem várias issues já abertas, você pode trabalhar em uma delas ou adicionar ao projeto com base na sua experiência e uso.

Idealmente, você pode discutir o tópico através de uma issue antes de começar a trabalhar.

[_Agradecimento ao Serenata de Amor por ter um ótimo guia de contribuição que inspirou este_](https://github.com/okfn-brasil/serenata-de-amor/blob/main/CONTRIBUTING.md).

### O básico de git

[**1. Faça um _Fork_ desse repositório**](https://github.com/jtemporal/gitfichas/fork)

**2. Clone o seu fork do repositório**

```console
git clone http://github.com/<YOUR-GITHUB-USERNAME>/gitfichas.git
```

**3. Crie uma branch nova**

```console
git switch -c <NOME-DE-USUÁRIO-NO-GITHUB>-<descrição-ou-número-da-issue>
```

Note que os nomes das branches começam com o nome de usuário do GitHub, isso nos ajuda a acompanhar as mudanças e quem está trabalhando nelas.

**4. Faça o que você faz de melhor**

Agora é a sua hora de brilhar e escrever um código significativo para elevar o nível do projeto!

**5. Comite suas mudanças**

```console
git commit -m '<Adicione a descrição das suas mudanças>'
```

Tente fazer pequenas mudanças por commit, assim é mais fácil entender o que você está fazendo ao revisar seu pull request.

**6. Envie as mudanças para o seu fork**

```console
git push -u origin <NOME-DE-USUÁRIO-NO-GITHUB>-<descrição-ou-número-da-issue>
```

**7. Crie um _Pull Request_**

Do seu fork no GitHub, geralmente há um botão para abrir pull requests.

Lembre-se de [linkar a sua issue no seu pull request](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

### Atribuição de Issues

Para manter o fluxo de trabalho organizado:

* **Somente mantenedores principais terão atribuição de issues:** Se você quiser trabalhar em algo, basta comentar dizendo que vai pegar a tarefa e abrir seu PR. Não é necessário atribuição formal.
* **Sem atribuição para eventuais contribuições:** Isso ajuda a manter o processo aberto e acolhedor para todos.
* **Janela de 2 dias:** Se não houver PR em até 2 dias após alguém demonstrar interesse, a issue fica aberta para qualquer pessoa trabalhar.

Assim, mantemos o processo amigável, com baixa barreira de entrada e evitamos que issues fiquem paradas. Obrigado por fazer parte da comunidade!
