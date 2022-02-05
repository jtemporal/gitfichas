---
layout: post
title: '#{{ ficha }} {{ desc }}'
image: "{{ thumbnail }}"
permalink: "/projects/{{ ficha }}"
translated: "/en/{{ ficha }}"
lang: "pt"
pv:
  url: "/projects/{{ previd }}"
  title: "{{ prevtitle }}"
{% if next == "true" %}nt:
  url: "/projects/{{ nextid }}"
  title: "{{ nexttitle }}"
{% else %}nt:
  url: "https://gitfichas.com/"
  title: "GitFichas"
{% endif %}---{% if subs == "true" %}
##### {{ subtitle }}{% endif %}

<img alt="{{ alt }}" src="{{ highres }}"><br><br>

| Comando | Descrição |
|---------|-----------|{{ table }}
{: .styled-table}

{% if related == "true" %}<br>

Leia mais sobre esse comando no blog post a seguir:

<a href="{{ relatedsrc }}">
  <strong>{{ relatedtext }}</strong>
</a>
{% else %}<!--
<br>

Leia mais sobre esse comando no blog post a seguir:

<a href="{{ relatedsrc }}">
  <strong>{{ relatedtext }}</strong>
</a>
-->
{% endif %}
