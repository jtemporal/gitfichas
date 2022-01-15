---
layout: post
title: '#{{ ficha }} {{ descen }}'
image: "/assets/img/projects/en/{{ ficha }}/thumbnail.jpg"
translated: "/projects/{{ ficha }}"
permalink: "/en/{{ ficha }}
lang: "en"
previous:
  url: "https://gitfichas.com/en/{{ previd }}"
  title: "{{ prevtitleen }}"
next:
  url: ""
  title: ""
---

<img alt="{{ alten }}" src="/assets/img/projects/{{ ficha }}/full.jpg">

{% if related == "true" %}
<a href="{{ relatedsrcen }}">
  <strong>{{ relatedtexten }}</strong>
</a>
{% endif %}