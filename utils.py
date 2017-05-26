import pkgutil

def get_strategies():
    """
    Gets a list of all available strategies

    Returns:
        A list of methods, each representing a strategy from the strategies module
    """
    strategy_names = [name for _, name, _ in pkgutil.iter_modules(['strategies'])]

    strategy_methods = []

    for strategy in strategy_names:
        module_name = "strategies." + strategy
        module = __import__(module_name, fromlist=[''])
        method = getattr(module, strategy)
        strategy_methods.append(method)

    return strategy_methods