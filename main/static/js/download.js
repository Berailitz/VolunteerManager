'use strict;'

function download() {
    let type_dict = {
        '活动记录补全版': 'all_in_one',
        '原始活动原始表格': 'records',
        '志愿者信息原始表格': 'volunteers',
        '志愿项目原始表格': 'jobs'
    };
    export_type = type_dict[$('#table-name-input')[0].value];
    $.getJSON('/api/download/', {'token': Cookies.get('token')}, function (rawData) {
        if (rawData['status']) {
            showToast('ERROR: 下载失败');
        } else {
            showToast('下载中');
            set_token(rawData['token']);
            document.location.href = rawData['data']['download_url'];
        }
    });
}

function cleanup() {
    $.ajax({
        url: '/api/download',
        type: 'DELETE',
        data: {'token': Cookies.get('token')},
        success: function (rawResponse) {
            responseJSON = JSON.parse(rawResponse);
            if (responseJSON['status']) {
                showToast('清除成功');
            } else {
                showToast(`ERROR: 清除失败: ${responseJSON['data']['msg']}`);
            }
        }
    });
}