# Contributing Guide

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

There are a bunch of issues already open, you can either work on one of them or you can add to the project based on your experience and usage.

Ideally you can discuss the topic via a issue before you start working.

All contributions are welcomed. ☺️
