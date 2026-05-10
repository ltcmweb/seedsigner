def __getattr__(name):
    module = __import__(f'seedsigner.gui.screens.generated.{name}')
    module = getattr(module, 'gui')
    module = getattr(module, 'screens')
    module = getattr(module, 'generated')
    module = getattr(module, name)
    return getattr(module, name)
