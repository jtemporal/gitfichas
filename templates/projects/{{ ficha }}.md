---
layout: post
title: '#{{ ficha }} {{ desc }}'
image: "/assets/img/projects/{{ ficha }}/thumbnail.jpg"
translated: "/en/{{ ficha }}"
lang: "pt"
previous:
  url: "https://gitfichas.com/projects/{{ previd }}"
  title: "{{ prevtitle }}"
{% if next == "true" %}
next:
  url: "https://gitfichas.com/projects/{{ nextid }}"
  title: "{{ nexttitle }}"
{% else %}
next:
  url: ""
  title: ""
{% endif %}
---

<img alt="{{ alt }}" src="/assets/img/projects/{{ ficha }}/full.jpg">

{% if related == "true" %}Leia mais sobre esse comando no blog post a seguir:

<a href="{{ relatedsrc }}">
  <strong>{{ relatedtext }}</strong>
</a>
{% else %}<!--
Leia mais sobre esse comando no blog post a seguir:

<a href="{{ relatedsrc }}">
  <strong>{{ relatedtext }}</strong>
</a>
-->
{% endif %}
