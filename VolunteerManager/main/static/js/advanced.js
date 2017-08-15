// 'use strict;'

function start_sync_volunteer_info() {
  $.getJSON('/api/sync', {
    'token': Cookies.get('token'),
    'sync_type': 'volunteer_info',
    'sync_command': 'start'
    }, function (rawData) {
      setToken(rawData['token']);
    if (rawData['status']) {
      showToast(`ERROR: ${rawData['data']['msg']}`);
    } else {
      showToast(`${rawData['data']['msg']}`);
    }
  });
}

function start_sync_volunteer_info() {
  $.getJSON('/api/sync', {
    'token': Cookies.get('token'),
    'sync_type': 'volunteer_info',
    'sync_command': 'start'
  }, function (rawData) {
    setToken(rawData['token']);
    if (rawData['status']) {
      showToast(`ERROR: ${rawData['data']['msg']}`);
    } else {
      showToast(`${rawData['data']['msg']}`);
    }
  });
}

function stop_sync_volunteer_info() {
  $.getJSON('/api/sync', {
    'token': Cookies.get('token'),
    'sync_type': 'volunteer_info',
    'sync_command': 'stop'
  }, function (rawData) {
    setToken(rawData['token']);
    if (rawData['status']) {
      showToast(`ERROR: ${rawData['data']['msg']}`);
    } else {
      showToast(`${rawData['data']['msg']}`);
    }
  });
}

function force_stop_volunteer_info() {
  $.getJSON('/api/sync', {
    'token': Cookies.get('token'),
    'sync_type': 'volunteer_info',
    'sync_command': 'force-stop'
  }, function (rawData) {
    setToken(rawData['token']);
    if (rawData['status']) {
      showToast(`ERROR: ${rawData['data']['msg']}`);
    } else {
      showToast(`${rawData['data']['msg']}`);
    }
  });
}

function force_stop_volunteer_info() {
  $.getJSON('/api/sync', {
    'token': Cookies.get('token'),
    'sync_type': 'volunteer_info',
    'sync_command': 'force-stop'
  }, function (rawData) {
    setToken(rawData['token']);
    if (rawData['status']) {
      showToast(`ERROR: ${rawData['data']['msg']}`);
    } else {
      showToast(`${rawData['data']['msg']}`);
    }
  });
}

function check_sync_volunteer_info() {
  $.getJSON('/api/sync', {
    'token': Cookies.get('token'),
    'sync_type': 'volunteer_info',
    'sync_command': 'check'
  }, function (rawData) {
    setToken(rawData['token']);
    if (rawData['status']) {
      showToast(`ERROR: ${rawData['data']['msg']}`);
    } else {
      showToast(`同步状态: ${rawData['data']['status']} @ ${rawData['data']['progress']}`, 2000);
    }
  });
}
