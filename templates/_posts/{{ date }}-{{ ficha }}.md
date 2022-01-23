---
layout: post
title: '#{{ ficha }} {{ desc }}'
image: "{{ thumbnail }}"
permalink: "/projects/{{ ficha }}"
translated: "/en/{{ ficha }}"
lang: "pt"
previous:
  url: "https://gitfichas.com/projects/{{ previd }}"
  title: "{{ prevtitle }}"
{% if next == "true" %}next:
  url: "https://gitfichas.com/projects/{{ nextid }}"
  title: "{{ nexttitle }}"
{% else %}next:
  url: ""
  title: ""
{% endif %}---{% if subtitle %}
##### {{ subtitle }}{% endif %}

<img alt="{{ alt }}" src="{{ highres }}"><br><br>

| Comando | Descrição |
|---------|-----------|

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
