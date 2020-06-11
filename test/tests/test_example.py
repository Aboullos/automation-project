from main.automation.model.testing.SuiteManager import SuiteManager
from main.project.steps.Steps import Steps


class TestDebugging:

    suite_m = SuiteManager("Performance")

    def performance(self):
        cases_matrix = self.suite_m.initialize_test_objects("Performance", None, "testData.csv")

        for test_case, test_id in cases_matrix:
            try:
                user_s = self.suite_m.create_user_story(test_case, test_id)
                steps: Steps = Steps(user_s)

                user_s.given(steps.log_in) \
                    .when(steps.run_performance)\
                    .run()
            except Exception as e:
                print("Error:", e.with_traceback())

        self.suite_m.create_html_report()


test = TestDebugging()
test.performance()
