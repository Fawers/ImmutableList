class singleton(type):
    def __init__(cls, *args, **kwargs):
        super(singleton, cls).__init__(*args, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(singleton, cls).__call__(*args, **kwargs)
        return cls._instance
