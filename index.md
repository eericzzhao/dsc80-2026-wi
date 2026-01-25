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

[Jump to the current week](#{{ site.modules.first.title | slugify }}){: .btn data-current-week-link } 
[Podcasts](https://podcast.ucsd.edu/){: .btn }
[Welcome Survey][welcome-survey]{: .btn }


{: .success }
**Welcome to DSC 80! 👋 Make sure to read the [syllabus][syllabus], check that you can access [Gradescope][gradescope] and [Campuswire][campuswire], and fill out the [Welcome Survey][welcome-survey].**

{% for module in site.modules %}
{{ module }}
{% endfor %}


<script>
(function() {
  const jumpLink = document.querySelector('[data-current-week-link]');
  if (!jumpLink) {
    return;
  }

  const modules = Array.from(document.querySelectorAll('.module'));
  if (!modules.length) {
    return;
  }

  // Define the quarter start date (first day of Week 1)
  const quarterStart = new Date('2026-01-06T00:00:00');
  const today = new Date();
  const todayMidnight = new Date(today.getFullYear(), today.getMonth(), today.getDate());

  // Calculate the week number based on days since quarter start
  const daysSinceStart = Math.floor((todayMidnight - quarterStart) / (1000 * 60 * 60 * 24));
  const currentWeekNumber = Math.max(1, Math.min(Math.floor(daysSinceStart / 7) + 1, modules.length));

  // Find the module for the current week
  let target = null;

  // Try to match by week number first (looking for "Week N" in the header)
  for (const moduleEl of modules) {
    const header = moduleEl.querySelector('.module-header');
    if (!header) continue;

    const headerText = header.textContent || '';
    const weekMatch = headerText.match(/Week\s+(\d+)/i);

    if (weekMatch && parseInt(weekMatch[1]) === currentWeekNumber) {
      target = header;
      break;
    }
  }

  // Fallback: if we can't find by week number, use the calculated index
  if (!target && currentWeekNumber > 0 && currentWeekNumber <= modules.length) {
    const targetModule = modules[currentWeekNumber - 1];
    if (targetModule) {
      target = targetModule.querySelector('.module-header');
    }
  }

  // If we're before the quarter starts or can't find a match, default to first week
  if (!target && modules.length > 0) {
    target = modules[0].querySelector('.module-header');
  }

  if (target && target.id) {
    jumpLink.setAttribute('href', '#' + target.id);
    // Automatically scroll to the current week
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
})();
</script>