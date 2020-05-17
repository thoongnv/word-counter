def get_paging_params(parse_args):
    params = {
        'offset': parse_args['offset'],
        'limit': parse_args['limit'],
        'order': {}
    }
    if parse_args['order']:
        orders = parse_args['order'].split(',')
        for field in orders:
            field = field.strip()
            if field.startswith('-'):
                params['order'][field[1:]] = 'desc'
            elif field.startswith('+'):
                params['order'][field[1:]] = 'asc'
            else:
                params['order'][field] = 'asc'

    return params
