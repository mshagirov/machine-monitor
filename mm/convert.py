import math

def byte2human( in_bytes:int|float)->str:
    """Converts `int` and `float` bytes to human-readable string

    E.g.:
        >> print(byte2human(1024))
        1Ki
    """
    if not (isinstance(in_bytes, int) or isinstance(in_bytes, float)):
        raise(ValueError(f"expected input type int|float, got {type(in_bytes)} "))
    if not( in_bytes > 0):
        raise(ValueError("input must be positive int or float"))
    magnitude = ('Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei')

    id = min( max( 0, int(math.log2(in_bytes)/10) -1), len(magnitude) - 1 )
    scaled_value = f"{in_bytes / (1 << ((1 + id)*10)):.1f}"
    
    if scaled_value.split('.')[-1] == '0':
        scaled_value = scaled_value[:-2]
    
    return f"{scaled_value}{magnitude[id]}"


