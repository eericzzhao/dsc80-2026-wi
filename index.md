---
layout: home
title: 🏠 Home
nav_exclude: false
nav_order: 1
---

# {{ site.tagline }}

{: .mb-2 }
{{ site.description }}
{: .fs-6 .fw-300 }

{{ site.staffersnobio }}

[syllabus]: https://dsc80.com/syllabus
[campuswire]: https://campuswire.com/c/GFDCC5DB7
[gradescope]: https://www.gradescope.com/courses/1209672
[github]: https://github.com/dsc-courses/dsc80-2026-fa
[welcome-survey]: https://forms.gle/byE5q4b1iKsBzEwN7

[Jump to the current week](#week-1-from-babypandas-to-pandas){: .btn } 
[Podcasts](https://podcast.ucsd.edu/){: .btn }
[Welcome Survey][welcome-survey]{: .btn }


{: .success }
**Welcome to DSC 80! 👋 Make sure to read the [syllabus][syllabus], check that you can access [Gradescope][gradescope] and [Campuswire][campuswire], and fill out the [Welcome Survey][welcome-survey].**

{% for module in site.modules %}
{{ module }}
{% endfor %}
