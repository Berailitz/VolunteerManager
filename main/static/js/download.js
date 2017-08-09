'use strict;'

function download() {
    let type_dict = {
        '活动记录补全版': '0',
        '原始活动原始表格': 'records',
        '志愿者信息原始表格': 'volunteers',
        '志愿项目原始表格': 'jobs'
    };
    document.location.href = '/download/' + type_dict[$('#table-name-input')[0].value]
}