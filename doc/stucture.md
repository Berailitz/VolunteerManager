#VolunteerManager Document - v2.2
##Features
* Submit records with Excel-like forms
* Qurey records by projects or volunteers
* Edit and delete records
* Download data in Excel files
* Scan volunteers on `bv2008.cn`
* Authenticate by passwords and tokens
##Requirements
* Python>=3.6.2
* beautifulsoup4>=4.6.0
* Flask_Bcrypt>=0.7.1
* Flask_DebugToolbar>=0.10.1
* Flask_RESTful>=0.3.6
* Flask_SQLAlchemy>=2.2
* Flask>=0.12.2
* openpyxl>=2.4.8
* pandas>=0.20.3
* requests>=2.11.0
* PyMySQL>=0.7.11
* SQLAlchemy>=1.1.11
* Werkzeug>=0.12.2
* And their dependencies

##Data structures
####Table `app_status`
``` sql
CREATE TABLE `app_status` (
  `status_key` varchar(40) NOT NULL,
  `status_value` varchar(40) NOT NULL,
  PRIMARY KEY (`status_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
status_key | status_value | comment
---------- | ------------ | -------
flag_syncing_volunteers | stop/stopped | order sent to syncer
is_syncing_volunteers | started/underway/finished | syncer status
syncing_process_volunteers | {synced}/{total} | syncing progress

####Table `jobs`
``` sql
CREATE TABLE `jobs` (
  `project_id` int(11) NOT NULL,
  `project_name` varchar(20) NOT NULL,
  `job_id` int(11) NOT NULL,
  `job_name` varchar(30) NOT NULL,
  `job_start` date DEFAULT NULL,
  `job_end` date DEFAULT NULL,
  `director` varchar(20) DEFAULT NULL,
  `location` varchar(30) DEFAULT NULL,
  `note` varchar(100) DEFAULT NULL,
  `blank1` int(11) DEFAULT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
**NOTE: `project_id` must be dictinct numbers, while `job_id` must be dictinct numbers in the same project.**

####Table `records`
``` sql
CREATE TABLE `records` (
  `record_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL,
  `working_date` date NOT NULL,
  `working_time` int(11) NOT NULL,
  `record_note` varchar(50) DEFAULT NULL,
  `operator_id` int(11) NOT NULL,
  `operation_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `record_status` int(11) DEFAULT '1',
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4;
```
**NOTE: `user_id` is constrained by `user_id` in table `volunteers`, while `operator_id` is constrained by `admin_id` in table `token`.**

####Table `tokens`
``` sql
CREATE TABLE `tokens` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(64) NOT NULL,
  `token` varchar(64) DEFAULT NULL,
  `login_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `blank1` int(11) DEFAULT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
```

####Table `volunteers`, `volunteers_temp`
``` sql
CREATE TABLE `volunteers` (
  `user_id` int(11) NOT NULL,
  `volunteer_id` varchar(20) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `student_id` varchar(20) DEFAULT NULL,
  `class_index` varchar(12) DEFAULT NULL,
  `legal_name` varchar(40) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `volunteer_time` float DEFAULT NULL,
  `note` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
**NOTE: `class_index` is `0` by default (after syncing with `bv2008.cn`).**

##Components
####Directory structure
```
├───.vscode
├───doc
├───log
├───note
├───old
├───test_mess
└───VolunteerManager
    ├───backup
    └───main
        ├───static
        │   ├───css
        │   ├───js
        │   └───temp
        └───templates
```

####HTML pages
* `main_blueprint` in `/VolunteerManager/main/views.py`, including all pages (single app pages) with HTML templates at `/VolunteerManager/main/templates` only
* `/VolunteerManager/main/static`, including js scripts, CSSs and Excels to be downloaded directly through nginx

####API handles
* `/VolunteerManager/main/api_handle.py`, handle all APIs under URL `/api`

####Mess
* zipped json files of MySQL databases, under `/VolunteerManager/backup`
* log files at `/log`, at the maximum of 7 files

##Routes
####`/*`
1. Tokens in cookies will be checked by `guest_only_view()` or `admin_only_view()`.
     * Visitor will be redirected to `restricted_view()` or `admin_only_view()` accordingly without reaching the requested resource.
     * Or requests will be past to backpoints `show_*_page()` in `main_blueprint`, which will return rendered templetes.
2. Response will be sent to warppers in `*_only_view()`, where new token will be added by `set_cookie()`.

####`/api/*`

1. Tokens at `/token` will be checked by `load_token_api()`.
    * Response with `/status` of `error_status_code` and `/data/msg` of `鉴权失败` will be returned immediately (without asking the target APIs).
    * The target API functions will be invoked with `admin` object as the first argument, whose `token` should be already updated, and then new `token` will be added to its response at `/token`.

####`/static/*/*`
1. Target files will be delivered by nginx without any authentication.

##Inner structure
####SQL handle
Namely, `get_*()` -> `query_items()` -> `table_object.query.filter()`.
Diffrent `query_type` will lead to diffrent types of results. an object for `one` and `first`, and a list for others.
Legal queries may lead to errors, including `NoResultFound` and `MultipleResultsFound` for `query_type` of `one`.
There is no need to commit after querying, but `db.session.commit()` should be called after any modification.
Any SQL object should be made serializable by invoke `item_to_dict` and remove `_sa_instance_state` from coyy of its `__dict__`.

####Auth handle
Namely, `*_only_view()` -> `check_cookie()` -> `check_token()`, `load_token_api()` -> `check_token()`.
All backpoints should be decorated by authentication decorators except `/api/token`, and current token object can be accessed by invoking `get_current_user()`.

####Sync handel
Namely, `VolunteerSyncer()` -> `SyncManager()`, `SyncApi()` -> `check_sync_command()` -> `start()`/`stop()`/`force_stop()`.
After checking `is_syncing_volunteers`, `_start_command()` will be invoked by `start()` to start a new process `execute_volunteer_sync()`, which will change `is_syncing_volunteers` and call `login()` and `scan()`, invoking `prase_list_soap()` to transfer HTML text to `volunteer_list`. All volunteers will be imported by `import_volunteers()`, which insert data into truncated table `volunteers_temp` and updates main table `volunteers` by `ON DUPLICATE KEY UPDATE`.
In Linux, `wait_process` will be called after syncer process exits to avoid defucnt/zombie process and set attribute `syncer_process` to None.

##APIs
**NOTE: All APIs should be called with token at `/token`, and new token will be placed at `/token` as well, or ```{'status': `error_status_code`, 'data': {'msg': '鉴权失败'}}``` will be returned.**
####`/api/token`
#####GET
* PARAMETERS: `username`, `password`, `token`
* RESPONSE: 
    * {'status': 1, 'data': {'msg': '鉴权失败'}}: Invalid arguments
    * {'status': 0, 'token': `token`}

####`/api/volunteers`
#####GET
* PARAMETERS: ANYTHING
* RESPONSE:
    * {'status': 1, 'data': {'info': {}, 'msg': '查无此人'}}: Invalid arguments
    * {'status': 0, 'data': {'info': `volunteer_dict`}}

####`/api/jobs`
#####GET
* PARAMETERS: ANYTHING
* RESPONSE:
    * {'status': 1, 'data': {'info': {}, 'msg': '查无此项'}}: Invalid arguments
    * {'status': 0, 'data': `job_list`}

####`/api/records`
#####GET
* PARAMETERS: ANYTHING
* RESPONSE:
    * {'status': 1, 'data': {'msg': '查无此记录'}}: Invalid arguments
    * {'data': {'records': `record_list`}}

#####POST
* PARAMETERS: `/data`
* RESPONSE:
    * {'status': 1, 'data': {'msg': '参数错误'}}: Invalid `/data`
    * {'status': 1, 'data': {'msg': '查无此记录'}}: Invalid `record_id`
    * {'status': 1, 'data': {'msg': '志愿项目或志愿者参数错误'}}: Invalid `student_id` or `job_id`
    * {'status': 0, 'data': {'msg': '已更新(ID:`record_id`)'}}

#####PUT
* PARAMETERS: `/data`
* RESPONSE:
    * {'status': 1, 'data': {'msg': '参数错误'}}: Invalid `/data`
    * {'status': 1, 'data': {'msg': '查无此人'}}: Invalid `student_id` or `legal_name`
    * {'status': 1, 'data': {'msg': '查无此项目'}}: Invalid `user_id` or `project_id`
    * {'status': 0, 'data': {'msg': '已录入(ID:`record_id`)'}}

#####DELETE
* PARAMETERS: `/data`
* RESPONSE:
    * {'status': 1, 'data': {'msg': '参数错误'}}: Invalid `/data`
    * {'status': 1, 'data': {'msg': '查无此记录'}}: Invalid `record_id`
    * {'status': 0, 'data': {'msg': '已删除(ID:`record_id`)'}}

####`/api/relationship`
#####GET
* RESPONSE:
  ``` json
  {
    'status': 0,
    'data': {
      'project_id_dict': {
      `project_id`: {
        'project_name': `project_name`,
        'job_id_dict': {`job_id`: `job_name`},
        'job_name_dict': {`job_name`: `job_id`}
        }
      },
      'project_name_dict': {`project_name`: `project_id`}
    }
  }
  ```

##Todos
- [ ] Add `class_index` after syncing
- [ ] Add backup for Table `records`
- [ ] Sync records
- [ ] Fix Edge, 360

##Mess
* Without `wait_process`, syncer process will 'hang up' after it exits (only on main server)
