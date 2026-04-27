class SessionFactoryAlreadyInitializedError(RuntimeError):
    """Raised when trying to initialize session factory second time"""

    def __init__(self):
        super().__init__("Session factory already initialized")
