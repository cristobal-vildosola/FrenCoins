class Handler:
    def __init__(self, driver):
        self.driver = driver

    def handle(self):
        pass


class StartGame(Handler):
    def handle(self):
        self.driver.start_game()
        return


class ContinueGame(Handler):
    def handle(self):
        self.driver.state.unpause()
        return


class MainMenuHandler(Handler):
    def handle(self):
        self.driver.main_menu()
        return


class QuitGame(Handler):
    def handle(self):
        self.driver.quit_game()
        return
