'use strict';
// the footer's date and stamp, on every page: the date the data were gathered (collect.py: the newest update file) and the
// repository state the timeline was read from
if (D.project.gathered) $('#gathered').textContent = ' up to ' + D.project.gathered;
$('#stamp').textContent = 'Repository state of ' + D.project.timeline.last_commit.replace('T', ' ').replace('Z', ' UTC') + '.';
