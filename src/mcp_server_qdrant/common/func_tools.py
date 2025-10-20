import inspect
from functools import wraps
from typing import Callable


def make_partial_function(original_func: Callable, fixed_values: dict) -> Callable:
    sig = inspect.signature(original_func)
    is_async = inspect.iscoroutinefunction(original_func)
    
    # Only keep parameters NOT in fixed_values
    remaining_params = [name for name in sig.parameters if name not in fixed_values]
    new_params = [sig.parameters[name] for name in remaining_params]

    if is_async:
        @wraps(original_func)
        async def async_wrapper(*args, **kwargs):
            # Start with fixed values
            bound_args = dict(fixed_values)

            # Validate that only expected parameters are passed
            unexpected_params = set(kwargs.keys()) - set(remaining_params)
            if unexpected_params:
                raise TypeError(
                    f"Got unexpected keyword arguments: {', '.join(unexpected_params)}. "
                    f"Expected parameters: {', '.join(remaining_params)}"
                )

            # Bind positional/keyword args from caller
            for name, value in zip(remaining_params, args):
                bound_args[name] = value
            bound_args.update(kwargs)

            return await original_func(**bound_args)
        
        wrapper = async_wrapper
    else:
        @wraps(original_func)
        def sync_wrapper(*args, **kwargs):
            # Start with fixed values
            bound_args = dict(fixed_values)

            # Validate that only expected parameters are passed
            unexpected_params = set(kwargs.keys()) - set(remaining_params)
            if unexpected_params:
                raise TypeError(
                    f"Got unexpected keyword arguments: {', '.join(unexpected_params)}. "
                    f"Expected parameters: {', '.join(remaining_params)}"
                )

            # Bind positional/keyword args from caller
            for name, value in zip(remaining_params, args):
                bound_args[name] = value
            bound_args.update(kwargs)

            return original_func(**bound_args)
        
        wrapper = sync_wrapper

    # Set the new __signature__ for introspection
    wrapper.__signature__ = sig.replace(parameters=new_params)  # type:ignore

    return wrapper
