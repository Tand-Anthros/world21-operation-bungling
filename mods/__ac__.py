import pickle, time, os, inspect


def sync(value: dict, name: str = None):
    if not name: 
        name = inspect.getmodule(inspect.currentframe().f_back)
        name = name.__file__.split("\\")[-1:][0].split('.py')[0]

    if type(value).__name__ == 'dict':
        with open(f'__pycache__/{name}.pkl', 'wb') as file:
            pickle.dump(value, file)
        while True:
            try:
                with open(f'__pycache__/~{name}.pkl', 'rb') as file:
                    variable = pickle.load(file)
                os.remove(f'__pycache__/~{name}.pkl')
                return variable
            except FileNotFoundError: time.sleep(0.016)
    else:
        raise AttributeError(f'\'{type(value).__name__}\' object is not supported')
