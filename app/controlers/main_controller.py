from app.ui.admin_windows import AdminWindow
from app.ui.client_windows import ClientViewSessionsWindow, ClientReserveWindow
from app.ui.main_window import RegistrationWindow


class Controller:

    def __init__(self):
        super().__init__()
        pass

    def main_window(self):
        self.registration = RegistrationWindow()
        self.registration.switch_window.connect(self.second_window)
        self.registration.show()

    def second_window(self):
        if self.registration.mode_return == 0:
            self.registration.close()
            self.client = ClientViewSessionsWindow()
            self.client.switch_window.connect(self.third_window)
            self.client.show()
            self.client.back_win.connect(self.back_from_first_client_window)
        elif self.registration.mode_return == 1:
            self.registration.close()
            self.ad = AdminWindow()
            self.ad.show()
            self.ad.switch_window.connect(self.back_from_admin_window)

    def third_window(self):
        session = self.client.sessions[self.client.curind]
        email = self.client.email
        self.client.close()
        self.client = ClientReserveWindow(session, email)
        self.client.update_window.connect(self.update_third_window)
        self.client.back_win.connect(self.back_from_second_client_window)
        self.client.show()

    def update_third_window(self):
        session = self.client.session
        email = self.client.email
        self.client.close()
        self.client = ClientReserveWindow(session, email)
        self.client.update_window.connect(self.update_third_window)
        self.client.back_win.connect(self.back_from_second_client_window)
        self.client.show()

    def back_from_admin_window(self):
        self.ad.close()
        self.main_window()

    def back_from_first_client_window(self):
        self.client.close()
        self.main_window()

    def back_from_second_client_window(self):
        self.client.close()
        self.second_window()