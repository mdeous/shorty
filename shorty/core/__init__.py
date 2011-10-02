# -*- coding: utf-8 -*-

def setup_routing(app, routes):
    """
    Registers :class:`flask.Blueprint` instances and adds routes all at once.

    :param app: The current application.
    :type app: flask.Flask.
    :param routes: The routes definition in the format:
        ((blueprint_instance, url_prefix),
            ('/route1/<param>', view_function1),
            ('/route2', view_function2),
            ...
        )
    :type routes: tuple.
    :returns: None
    """
    for route in routes:
        # endpoint: (blueprint_instance, url_prefix)
        # rules: [('/route/', view_function), ...]
        endpoint, rules = route[0], route[1:]
        for pattern, view in rules:
            if endpoint is None:
                app.add_url_rule(pattern, view_func=view)
            else:
                endpoint[0].add_url_rule(pattern, view_func=view)
        if endpoint is not None:
            app.register_blueprint(endpoint[0], url_prefix=endpoint[1])
