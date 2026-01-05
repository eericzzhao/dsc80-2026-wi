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

[syllabus]: syllabus
[campuswire]: https://campuswire.com/c/GFDCC5DB7
[gradescope]: https://www.gradescope.com/courses/1209672
[github]: https://github.com/dsc-courses/dsc80-2026-fa
[welcome-survey]: google.com

[Jump to the current week](#week-1-dataframes){: .btn } 
[Podcasts](https://podcast.ucsd.edu/){: .btn }
[Welcome Survey][welcome-survey]{: .btn }

{: .warning }
This site is **under construction**. Anything you read here is not finalized. This disclaimer will be removed when the site is ready for Fall 2025. 

{: .success }
**Welcome to DSC 80! 👋 Make sure to read the [syllabus][syllabus], check that you can access [Gradescope][gradescope] and [Campuswire][campuswire], and fill out the [Welcome Survey][welcome-survey].**

{% for module in site.modules %}
{{ module }}
{% endfor %}
