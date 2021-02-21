from common.response_message import API_DOCUMENTS


def error_response_400():
    response_dict = {}
    response_dict_child = {}
    response_dict['message'] = 'Bad Request'
    response_dict_child['code'] = 400
    response_dict_child['url_ref'] = API_DOCUMENTS
    response_dict['errors'] = response_dict_child
    return response_dict


def error_response_400_validation_error(f_name):
    # 受け取った値によりエラーメッセージを動的に変更
    response_dict = {}
    response_dict_child = {}
    response_dict['message'] = __error_message(f_name)
    response_dict_child['code'] = 400
    response_dict_child['url_ref'] = API_DOCUMENTS
    response_dict['errors'] = response_dict_child
    return response_dict


def error_response_403():
    response_dict = {}
    response_dict_child = {}
    response_dict['message'] = 'You do not have access to this API.'
    response_dict_child['code'] = 403
    response_dict_child['url_ref'] = API_DOCUMENTS
    response_dict['errors'] = response_dict_child
    return response_dict


def error_response_403_no_uuid():
    response_dict = {}
    response_dict_child = {}
    response_dict['message'] = 'Forbidden, please give [X-Request-ID] ' \
                               'to the header after authentication.'
    response_dict_child['code'] = 403
    response_dict_child['url_ref'] = API_DOCUMENTS
    response_dict['errors'] = response_dict_child
    return response_dict


def error_response_403_expired_or_incorrect_uuid():
    response_dict = {}
    response_dict_child = {}
    response_dict['message'] = 'The X-Request-ID has expired or is incorrect.' \
                               ' Please authenticate and issue again.'
    response_dict_child['code'] = 403
    response_dict_child['url_ref'] = API_DOCUMENTS
    response_dict['errors'] = response_dict_child
    return response_dict


def error_response_500():
    response_dict = {}
    response_dict_child = {}
    response_dict['message'] = 'Internal error please try again later'
    response_dict_child['code'] = 500
    response_dict_child['url_ref'] = API_DOCUMENTS
    response_dict['errors'] = response_dict_child
    return response_dict


def __error_message(f_name):
    if f_name == 'POST_NEWS':
        return ('The key or type is invalid, follow the example.\n'
                 'ex:\n'
                 '{\n'
                 '  "description": str\n'
                 '}\n'
                )
    elif f_name == 'POST_NEWS':
        return ('The key or type is invalid, follow the example.\n'
                'ex:\n'
                '{\n'
                '  "description": str\n'
                '}\n'
                )
