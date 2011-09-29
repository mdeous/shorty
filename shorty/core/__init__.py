# -*- coding: utf-8 -*-

def setup_routing(app, routes):
    """
    Given the current `Flask` application and a list of routes (a route being
    a tuple where the first element is a '(blueprint_obj, url_prefix)' tuple (or
    None if routes don't belong to a blueprint) and all the other elements being
    '(route, view_func)' tuples, add all the routes and register the blueprints
    to which they belong.
    """
    for route in routes:
        endpoint, rules = route[0], route[1:]
        for pattern, view in rules:
            (app if endpoint is None else endpoint[0]
                ).add_url_rule(pattern, view_func=view)
        if endpoint is not None:
            app.register_blueprint(endpoint[0], url_prefix=endpoint[1])
