"""handle restful related problems"""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

def parse_all_args(parser, expected_args=None):
    """prase all args, `None` by default, return args dict"""
    if not expected_args:
        expected_args = {
            'job_id': int,
            'legal_name': str,
            'length': int,
            'page': int,
            'project_id': int,
            'project_name': str,
            'query_type': str,
            'record_id': int,
            'student_id': str,
            'user_id': int
        }
    for arg in expected_args.items():
        parser.add_argument(arg[0], type=arg[1])
    return parser.parse_args()

def parse_one_arg(parser, arg_key, arg_type, default=None, call_back=lambda arg: arg):
    """prase all args, `None` by default, return args dict"""
    parser.add_argument(arg_key, type=arg_type)
    return get_arg(parser.parse_args()[arg_key], default, call_back)

def get_arg(current, default=None, call_back=lambda arg: arg):
    """check whether a value is None (or equal to False), return default value, None by default, or call_back(value)"""
    if current:
        return call_back(current)
    return default

def check_args(received_args, expected_args):
    """#DEBUG: Check args, return diffrences."""
    if received_args and received_args == expected_args.keys():
        return None
    else:
        missing_args = {key:received_args[key] for key in expected_args.keys() if received_args[key] is None}
        unexpected_args = {key:received_args[key] for key in received_args.keys() if key not in expected_args.keys()}
        return {**missing_args, **unexpected_args}
