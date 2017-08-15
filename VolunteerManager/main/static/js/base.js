'use strict;'

let relationshipDict = {};

function showToast(messageText, timeout=1000) {
  $('#snackbar')[0].MaterialSnackbar.showSnackbar(
    {
      'message': messageText,
      'timeout': timeout,
    }
  );
}

function setToken(token) {
  Cookies.set('token', token, {
    expires: 7,
    secure: true
  });
}

const getRelationship = new Promise((resolve, reject) => {
  $.getJSON('/api/relationship', {'token': Cookies.get('token')}, raw_response => {
    relationshipDict = raw_response['data'];
    setToken(raw_response['token']);
    resolve();
  });
});

const project_id_to_name = project_id => relationshipDict['project_id_dict'][String(project_id)]['project_name'];
const project_name_to_id = project_name => relationshipDict['project_name_dict'][project_name];
const job_id_to_name = (project_id, job_id) => relationshipDict['project_id_dict'][String(project_id)]['job_id_dict'][String(job_id)];
const job_name_to_id = (project_id, job_name) => relationshipDict['project_id_dict'][String(project_id)]['job_name_dict'][job_name];

function decodeLine(rawLine) {
  rawLine['project_name'] = project_id_to_name(rawLine['project_id']);
  rawLine['job_name'] = job_id_to_name(rawLine['project_id'], rawLine['job_id']);
  return rawLine;
}

function logout() {
  Cookies.remove('token');
  document.location.href = '/';
}

$(document).pjax('a.enable-pjax', '#pjax-container');

$(document).on('pjax:success', function() {
  let layout = $('.mdl-layout');
  let drawer = $('.mdl-layout__drawer');
  drawer.removeClass('is-visible');
  drawer.attr('aria-hidden', 'true');
  $('.mdl-layout__obfuscator').removeClass('is-visible');
  // if this doesn’t happen, the drawer disappears
  // at an upgradeElement call
  layout.removeClass('is-upgraded');
  layout.removeClass('has-drawer');
  layout.removeAttr('data-upgraded');
  // upgrade all the elements!
  $('*[class^=mdl]').each(function(index, element) {
    componentHandler.upgradeElement(element);
  });
  // re-bind PJAX
  // $(document).pjax('a.enable-pjax', '#pjax-container');
 });
 