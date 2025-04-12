from typing import get_type_hints


ACTION_HANDLERS = {}

def action_handler(name):
        def decorator(fn):
                if name in ACTION_HANDLERS:
                        raise ValueError(f"Intent '{name}' already registered.")
                model_class = get_type_hints(fn).get('data')
                obj = {
                        'function': fn,
                        'model': model_class
                }
                ACTION_HANDLERS[name] = obj
                return obj 
        return decorator
