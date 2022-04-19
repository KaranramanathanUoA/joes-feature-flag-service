from feature_flag_service import FeatureFlagService
from user_feature_flag import UserFeatureFlag
import unittest


class FeatureFlagServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.feature_flag_service = FeatureFlagService()
        self.global_feature_flags = {}
        self.user_feature_flags = {}

    def test_set_globally_function_initialises_global_flag(self):
        self.feature_flag_service.set_globally("Test Global Flag", True)
        self.assertIn("Test Global Flag", self.feature_flag_service.global_feature_flags)

    def test_set_function_initialises_user_feature_flag(self):
        self.feature_flag_service.set(100, "Test User Feature Flag", True)
        self.assertIn("Test User Feature Flag", self.feature_flag_service.user_feature_flags)
        for key, value in self.feature_flag_service.user_feature_flags.items():
            self.assertIsInstance(value, UserFeatureFlag)

    def test_enabled_flags_function_returns_list_of_enabled_flags(self):
        self.feature_flag_service.global_feature_flags = {"Test Global Flag 1": True, "Test Global Flag 2" : False}
        self.feature_flag_service.user_feature_flags = {"Test User Flag": UserFeatureFlag(120, True)}
        list_of_test_flags = self.feature_flag_service.enabled_flags(120)
        self.assertEqual(len(list_of_test_flags), 2)
        self.assertIn("Test User Flag", list_of_test_flags)

    def test_is_enabled_function_returns_correct_boolean_value(self):
        self.feature_flag_service.global_feature_flags = {"Test Global Flag 1": True, "Test Global Flag 2" : False}
        self.feature_flag_service.user_feature_flags = {"Test User Flag": UserFeatureFlag(120, True)}
        self.assertEqual(self.feature_flag_service.is_enabled("Test Global Flag 1", 1000), True)
        self.assertEqual(self.feature_flag_service.is_enabled("Test Global Flag 2"), False)
        self.assertEqual(self.feature_flag_service.is_enabled("Test User Flag", 120), True)

if __name__ == "__main__":
    unittest.main()