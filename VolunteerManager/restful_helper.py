#!/usr/env/python3
# -*- coding: UTF-8 -*-

def parse_all_args(parser):
    parser.add_argument('job_id', type=int)
    parser.add_argument('legal_name', type=str)
    parser.add_argument('length', type=int)
    parser.add_argument('page', type=int)
    parser.add_argument('project_id', type=int)
    parser.add_argument('project_name', type=str)
    parser.add_argument('query_type', type=str)
    parser.add_argument('student_id', type=str)
    parser.add_argument('query_type', type=str)
    parser.add_argument('user_id', type=int)
    return parser.parse_args()

def get_arg(current, default=None, call_back=lambda arg: arg):
    if current:
        return call_back(current)
    else:
        return default
