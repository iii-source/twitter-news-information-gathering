from common.response_message import API_DOCUMENTS


def error_response_400():
    response_dict = {}
    response_dict_child = {}
    response_dict['message'] = 'Bad Request'
    response_dict_child['code'] = 400
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



