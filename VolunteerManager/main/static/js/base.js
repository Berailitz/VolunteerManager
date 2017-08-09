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

function logout() {
  Cookies.remove('token');
  document.location.href = '/';
}