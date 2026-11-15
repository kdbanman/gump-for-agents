'use strict';
(function () { // the map's 'Built, and when' line, from git (collect.py)
  const T = D.project.timeline, h = Math.round((Date.parse(T.last_commit.slice(0, 19) + 'Z') - Date.parse(T.first_commit.slice(0, 19) + 'Z')) / 3600e3), n = T.pull_requests.length;
  $('#m-built').textContent = h + ' hours, ' + fmtInt(T.totals.commits) + ' commits';
})();
