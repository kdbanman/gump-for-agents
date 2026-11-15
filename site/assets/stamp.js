'use strict';
// the footer's stamp, on every page (moved from the old page's figure code)
$('#stamp').textContent = 'Repository state of ' + D.project.timeline.last_commit.replace('T', ' ').replace('Z', ' UTC') + '.';
