from common.response_message import API_DOCUMENTS


def response_200():
    response_dict = {}
    response_dict['message'] = 'accepted the certificate.'
    response_dict['code'] = 200
    return response_dict


def response_200_post():
    response_dict = {}
    response_dict['message'] = 'Inserted successfully.'
    response_dict['code'] = 200
    return response_dict


def response_200_put():
    response_dict = {}
    response_dict['message'] = 'Updated successfully.'
    response_dict['code'] = 200
    return response_dict


def response_401():
    response_dict = {}
    response_dict['message'] = 'certification failed.'
    response_dict['code'] = 401
    return response_dict


def response_404():
    response_dict = {}
    response_dict['message'] = 'not found newsid'
    response_dict['code'] = 404
    return response_dict
