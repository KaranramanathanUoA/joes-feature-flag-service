from user_feature_flag import UserFeatureFlag
import hashlib


class FeatureFlagService:
    def __init__(self) -> None:
        self.global_feature_flags = {}
        self.user_feature_flags = {}

    def set_globally(self, feature_flag_name : str, enabled : bool) -> None:
        # self.global_feature_flags tracks the global feature flags and is a hashmap that maps the
        # name of the flag to its enabled value ie. True or False 
        self.global_feature_flags[feature_flag_name] = enabled

    def set(self, user_id : int, feature_flag_name : str, enabled : bool) -> None:
        # self.user_feature_flags tracks the overriden user feature flags and is a hashmap that maps the
        # name of the flag to an instance of the UserFeatureFlag class
        self.user_feature_flags[feature_flag_name] = UserFeatureFlag(user_id, enabled)

    def enabled_flags(self, user_id: int) -> list:
        list_of_enabled_flags = []

        for feature_flag_name, enabled in self.global_feature_flags.items():
            if enabled:
                list_of_enabled_flags.append(feature_flag_name)

        for user_feature_flag_name, user_feature_flag in self.user_feature_flags.items():
            if (user_feature_flag.user_id == user_id and user_feature_flag.enabled is True):
                list_of_enabled_flags.append(user_feature_flag_name)

        return list_of_enabled_flags

    def is_enabled(self, feature_flag_name : str, user_id : int = -1) -> bool:
        is_global_flag = False
        is_user_feature_flag = False
        is_enabled = False

        if feature_flag_name in self.global_feature_flags:
            if self.global_feature_flags[feature_flag_name] is True:
                is_global_flag = True
        
        if feature_flag_name in self.user_feature_flags:
            user_feature_flag = self.user_feature_flags[feature_flag_name]
            if user_feature_flag.user_id == user_id and user_feature_flag.enabled is True:
                is_user_feature_flag = True
        
        if is_global_flag or is_user_feature_flag:
            is_enabled = True
        
        return is_enabled

    @staticmethod
    def return_hashed_integer_value_from_user_id(user_id):
        # convert user_id to string with utf-8 encoding as this function only accepts bytes objects as input
        hash = hashlib.sha256(str(user_id).encode('utf-8')).hexdigest()
        # converts the hashed value back to an integer from hexadecimal notation
        return int(hash, base=16)

    def user_in_segment(self, user_id : int, rollout: int) -> bool:
        user_in_segment = False

        hashed_user_id = self.return_hashed_integer_value_from_user_id(user_id)
        print (hashed_user_id % 100)

        if (hashed_user_id % 100 < rollout):
            user_in_segment = True

        return user_in_segment


def main() -> None:
    feature_flag_service = FeatureFlagService()
    feature_flag_service.set_globally("Global Feature 1", True)
    feature_flag_service.set(100, "User Feature 1", True)
    feature_flag_service.set(100, "User Feature 1", True)
    # enabled_flags = feature_flag_service.enabled_flags(100)
    # is_enabled = feature_flag_service.is_enabled("User Feature 1", 100)
    # user_in_segment = feature_flag_service.user_in_segment(32, 15)
    
if __name__ == "__main__":
    main()
