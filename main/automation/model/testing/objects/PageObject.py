from main.automation.configuration import AutomationConstants
from main.automation.model.testing.UserStory import UserStory
from main.automation.model.testing.objects.InteractionObject import InteractionObject
from main.automation.model.webdriver.DriverHelper import DriverHelper


class PageObject(InteractionObject):

    _web_driver: DriverHelper

    def __init__(self, user_story: UserStory):
        super().__init__(user_story)

        self._web_driver = user_story.get_web_driver()

        if self._web_driver.get_driver() is None and self._web_driver.get_driver_type() is AutomationConstants.WEB:
            self._web_driver.initialize_driver()