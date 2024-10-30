# Contributing Guide | Guia de Contribuição

| Table of content | Índice |
| ------- | --------- |
| &nbsp;&nbsp;• [Before You Start](#before-you-start)<br>&nbsp;&nbsp;• [Cards Types](#cards-types)<br>&nbsp;&nbsp;• [Running the Project](#running-the-project)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Local way](#local-way)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Install dependencies](#install-dependencies)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Run the project](#run-the-project)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Docker way](#docker-way)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Building image](#building-image)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Serving](#serving)<br>&nbsp;&nbsp;• [The Basics of Contributing](#the-basics-of-contributing)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [The Git basics](#the-git-basics) | &nbsp;&nbsp;• [Antes de Começar](#antes-de-começar)<br>&nbsp;&nbsp;• [Tipos de Fichas](#tipos-de-fichas)<br>&nbsp;&nbsp;• [Rodando o Projeto](#rodando-o-projeto)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Localmente](#localmente)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Instalando depedências](#instalando-depedências)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Rodar o projeto](#rodar-o-projeto)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Com Docker](#com-docker)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Montando a imagem](#montando-a-imagem)<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• [Servindo](#servindo)<br>&nbsp;&nbsp;• [O Básico de Contribuições](#o-básico-de-contribuições)<br>&nbsp;&nbsp;&nbsp;&nbsp;• [O básico de git](#o-básico-de-git) |

## Before You Start

Thank you for wanting to contribute to GitFichas | GitStudyCards. Here you'll find most of the information you'll need for contributing.

If you have any questions create an issue.

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
| `permalink` |  `mandatory` | `mandatory` |  Folows `/projects/{number}` for pt cards and `/en/{number}` for en cards |
| `lang` | `mandatory` | `mandatory` | Either `"pt"` or `"en"`. These are the only languages supported at the moment |
| `translated` | `optional` | `optional` |  Path to translated card e.g.: `/projects/{number}` |
| `pv` | `mandatory` | `mandatory` | information about the previous card for arrow linking |
| `pv.url` | `mandatory` | `mandatory` | Path to previous card e.g.: `/projects/{number}` |
| `pv.title` | `mandatory` | `mandatory` | Command to previous card e.g.: `#001 git init` |
| `nt` | `mandatory` | `mandatory` | information about the next card for arrow linking |
| `nt.url` | `mandatory` | `mandatory` | Path to next card e.g.: `/projects/{number}` |
| `nt.title` | `mandatory` | `mandatory` | Command to next card e.g.: `#001 git init` |

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
translated: "/projects/052"
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
permalink: "/en/030"
translated: "/projects/030"
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

---

## Antes de Começar

Obrigada por querer contribuir com o GitFichas. Aqui você encontrará a maioria das informações que precisará para contribuir.

Se tiver alguma dúvida, crie uma issue.

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
| `permalink` | `obrigatório` | `obrigatório` | Segue `/projects/{number}` para fichas em pt e `/en/{number}` para fichas em en |
| `lang` | `obrigatório` | `obrigatório` | `"pt"` ou `"en"`. Estes são os únicos idiomas suportados no momento |
| `translated` | `opcional` | `opcional` | Caminho para a ficha traduzida, por exemplo: `/projects/{number}` |
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
permalink: "/projects/052"
lang: "pt"
translated: "/en/052"
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
permalink: "/projects/030"
translated: "/en/030"
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

## Rodando o Projeto

O site é executado no Jekyll, mas também está preparado para rodar no Docker (embora já faz um tempo desde que eu usei o Dockerfile para desenvolvimento).

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

```consle
git push -u origin <NOME-DE-USUÁRIO-NO-GITHUB>-<descrição-ou-número-da-issue>
```

**7. Crie um _Pull Request_**

Do seu fork no GitHub, geralmente há um botão para abrir pull requests.

Lembre-se de [linkar a sua issue no seu pull request](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).