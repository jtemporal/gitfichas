---
layout: post
title: '#{{ ficha }} {{ descen }}'
image: "/assets/img/projects/en/{{ ficha }}/thumbnail.jpg"
translated: "/projects/{{ ficha }}"
permalink: "/en/{{ ficha }}"
lang: "en"
previous:
  url: "https://gitfichas.com/en/{{ previd }}"
  title: "{{ prevtitleen }}"
{% if next == "true" %}
next:
  url: "https://gitfichas.com/en/{{ nextiden }}"
  title: "{{ nexttitleen }}"
{% else %}
next:
  url: ""
  title: ""
{% endif %}
{% endif %}
---

<img alt="{{ alten }}" src="/assets/img/projects/{{ ficha }}/full.jpg">

{% if related == "true" %}
<a href="{{ relatedsrcen }}">
  <strong>{{ relatedtexten }}</strong>
</a>
{% else %}
<!--
<a href="{{ relatedsrcen }}">
  <strong>{{ relatedtexten }}</strong>
</a>
-->
{% endif %}