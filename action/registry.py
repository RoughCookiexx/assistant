ACTION_HANDLERS = {}

def action_handler(name):
        def decorator(fn):
                if name in ACTION_HANDLERS:
                        raise ValueError(f"Intent '{name}' already registered.")
                ACTION_HANDLERS[name] = fn
                return fn
        return decorator
