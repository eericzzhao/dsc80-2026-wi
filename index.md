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
document.addEventListener('DOMContentLoaded', function() {
  // Find the "Jump to the current week" button
  const jumpButton = document.querySelector('[data-current-week-link]');
  if (!jumpButton) return;

  // Get all module elements with week data
  const modules = document.querySelectorAll('.module[data-week-start][data-week-end]');
  if (modules.length === 0) return;

  // Helper function to parse dates (YYYY-MM-DD format)
  function parseDate(dateString) {
    if (!dateString) return null;
    const parts = dateString.split('-');
    if (parts.length !== 3) return null;
    const year = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10) - 1; // JS months are 0-indexed
    const day = parseInt(parts[2], 10);
    return new Date(year, month, day);
  }

  // Get today's date (at midnight for comparison)
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Find the current week
  let currentModule = null;
  let upcomingModule = null;
  let mostRecentModule = null;

  modules.forEach(function(module) {
    const startDate = parseDate(module.getAttribute('data-week-start'));
    const endDate = parseDate(module.getAttribute('data-week-end'));

    if (!startDate || !endDate) return;

    // Check if today is within this week's range
    if (today >= startDate && today <= endDate) {
      currentModule = module;
    }

    // Track the first upcoming module
    if (!upcomingModule && startDate > today) {
      upcomingModule = module;
    }

    // Track the most recent past module
    if (endDate < today) {
      if (!mostRecentModule) {
        mostRecentModule = module;
      } else {
        const mostRecentEnd = parseDate(mostRecentModule.getAttribute('data-week-end'));
        if (endDate > mostRecentEnd) {
          mostRecentModule = module;
        }
      }
    }
  });

  // Determine which module to jump to
  let targetModule = currentModule || upcomingModule || mostRecentModule;

  if (targetModule) {
    const moduleId = targetModule.querySelector('.module-header').getAttribute('id');
    if (moduleId) {
      jumpButton.setAttribute('href', '#' + moduleId);
    }
  }
});
</script>
