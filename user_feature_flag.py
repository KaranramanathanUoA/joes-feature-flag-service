class UserFeatureFlag:
    def __init__(self, user_id, enabled) -> None:
        self.user_id = user_id
        self.enabled = enabled