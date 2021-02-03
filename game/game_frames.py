from game.game_utilities import *
from tkinter import messagebox


class P1Create(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title('Create Account')

        self.back_button = BackButton(self, self.parent, P1Login)
        self.title = TitleLabel(self, self.parent, 'Create Account', 0, 30)
        self.username_label = TextLabel(self, self.parent, 'Username: ', 0, 10)
        self.username_entry = TextEntry(self, self.parent, '', 0, 10)
        self.password_label = TextLabel(self, self.parent, 'Password: ', 0, 10)
        self.password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.confirm_password_label = TextLabel(self, self.parent, 'Confirm Password: ', 0, 10)
        self.confirm_password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.login_create_account = TextButton(self, self.parent, 'Confirm', lambda: self.create_account(), 0, 20)
        self.alert = AlertLabel(self, self.parent, '', 0, 10)
        self.watermark = WatermarkLabel(self, self.parent)

    def create_account(self):
        username, password = self.username_entry.get(), self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        pass_check_result = security.password_check(password, confirm_password)

        if pass_check_result is None:
            if not database.user_exists(username):
                self.parent.p1 = Player(username)
                database.add_user(username, password, 'blue', 0.2)
                switch_user(self.parent, 'blue', 0.2)
                self.parent.switch_frame(GameMenu)

            else:
                self.alert.configure(text='Username already taken')

        else:
            self.alert.configure(text=pass_check_result)


class GameMenu(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.alert_made = False
        self.parent.title(f'game Menu - {self.parent.p1.username}')

        self.title = TitleLabel(self, self.parent, 'game Menu', 0, 60)
        self.duo_button = MenuButton(self, self.parent, 'Duo game',
                                     lambda: self.parent.switch_frame(P2Login), 25, 2, 0, 20)
        self.load_game_button = MenuButton(self, self.parent, 'Load game',
                                           lambda: self.parent.switch_frame(Load), 25, 2, 0, 20)
        self.online_button = MenuButton(self, self.parent, 'Online game',
                                        lambda: self.parent.switch_frame(OnlineGame), 25, 2, 0, 20)
        self.rules_button = MenuButton(self, self.parent, 'Rules',
                                       lambda: self.parent.switch_frame(Rules), 25, 2, 0, 20)
        self.settings_button = MenuButton(self, self.parent, 'Settings',
                                          lambda: self.parent.switch_frame(Settings), 25, 2, 0, 20)
        self.share_button = self.settings_button = MenuButton(self, self.parent, 'Share',
                                                              lambda: self.parent.switch_frame(Share), 25, 2, 0, 20)

        self.watermark = WatermarkLabel(self, self.parent)


class Settings(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title(f'Settings - {self.parent.p1.username}')

        self.back_button = BackButton(self, self.parent, GameMenu)
        self.title = TitleLabel(self, self.parent, 'Settings', 0, 30)
        self.music_subtitle = UnderlineSubtitle(self, self.parent, 'Music', 0, 10)
        self.music_volume_label = TextLabel(self, self.parent, 'Music Volume:', 0, 10)
        self.volume_scale = VolumeScale(self, self.parent, self.change_volume, 0, 10)
        self.themes_subtitle = UnderlineSubtitle(self, self.parent, 'Themes', 0, 10)
        self.blue_checkbox = ThemeCheckbox(self, self.parent, 'Blue', 0, 10)
        self.green_checkbox = ThemeCheckbox(self, self.parent, 'Green', 0, 10)
        self.black_checkbox = ThemeCheckbox(self, self.parent, 'Black', 0, 10)
        self.white_checkbox = ThemeCheckbox(self, self.parent, 'White', 0, 10)
        self.log_out_button = tk.Button(self, text='Log Out', bg=self.parent.colour[1],
                                        highlightbackground=self.parent.colour[1],
                                        command=lambda: self.log_out())
        self.log_out_button.pack(anchor='se', padx=5)
        self.watermark = WatermarkLabel(self, self.parent)

        self.volume_scale.set(pygame.mixer.music.get_volume() * 100)
        if self.parent.colour == BLUE:
            self.blue_checkbox.select()
        elif self.parent.colour == GREEN:
            self.green_checkbox.select()
        elif self.parent.colour == BLACK:
            self.black_checkbox.select()
        elif self.parent.colour == WHITE:
            self.white_checkbox.select()

    def change_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)
        database.update_user_volume(self.parent.p1.username, pygame.mixer.music.get_volume())

    def change_theme(self, theme, button):
        self.blue_checkbox.deselect()
        self.green_checkbox.deselect()
        self.black_checkbox.deselect()
        self.white_checkbox.deselect()
        button.select()

        database.update_user_theme(self.parent.p1.username, theme)
        if theme == 'blue':
            self.parent.colour = BLUE
            self.parent.font_colour = 'white'
        elif theme == 'green':
            self.parent.colour = GREEN
            self.parent.font_colour = 'white'
        elif theme == 'black':
            self.parent.colour = BLACK
            self.parent.font_colour = 'white'
        elif theme == 'white':
            self.parent.colour = WHITE
            self.parent.font_colour = 'black'

        self.configure(bg=self.parent.colour[1])
        self.parent.configure(bg=self.parent.colour[0])
        self.volume_scale.configure(troughcolor=self.parent.colour[1], activebackground=self.parent.colour[1])

        for i in self.pack_slaves():
            i.configure(bg=self.parent.colour[1], highlightbackground=self.parent.colour[1], fg=self.master.font_colour)

        self.back_button.configure(fg='black')
        self.log_out_button.configure(fg='black')

    def log_out(self):
        self.log_out_message = messagebox.askokcancel(title='Confirm', message='Are you sure you want to log out?')

        if self.log_out_message:
            del self.parent.p1
            self.parent.switch_frame(P1Login)


class Rules(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title(f'Rules - {self.parent.p1.username}')
        self.back_button = BackButton(self, self.parent, GameMenu)
        self.title = TitleLabel(self, self.parent, 'Rules', 0, 40)
        with open(RULES_FILE, 'r') as f:
            self.rules_label = TextLabel(self, self.parent, f.read(), 0, 10)
        self.watermark = WatermarkLabel(self, self.parent)


class P2Login(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title('Player Two Login')
        self.alert_made = False

        self.title = TitleLabel(self, self.parent, 'Login', 0, 30)
        self.notice = TextLabel(self, self.parent, 'You will be automatically logged out once the game is over.', 0, 5)
        self.username_label = TextLabel(self, self.parent, 'Username: ', 0, 10)
        self.username_entry = TextEntry(self, self.parent, '', 0, 10)
        self.password_label = TextLabel(self, self.parent, 'Password: ', 0, 10)
        self.password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.login_button = TextButton(self, self.parent, 'Confirm', lambda: self.login(), 0, 20)
        self.create_account_label = TextLabel(self, self.parent, "Don't have an account?\n\nCreate an account:", 0, 30)
        self.create_account_button = TextButton(self, self.parent, 'Confirm',
                                                lambda: self.parent.switch_frame(P2Create), 0, 10)
        self.watermark = WatermarkLabel(self, self.parent)

    def login(self):
        username, password = self.username_entry.get(), self.password_entry.get()

        if database.check_user(username, password):
            self.parent.p2 = Player(username)
            self.parent.switch_frame(DuoGame)

        elif not self.alert_made:
            self.alert = AlertLabel(self, self.parent, 'Invalid credentials', 0, 10)
            self.alert_made = True


class P2Create(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title('Player Two Create Account')

        self.back_button = BackButton(self, self.parent, P1Login)
        self.title = TitleLabel(self, self.parent, 'Create Account', 0, 30)
        self.notice = TextLabel(self, self.parent, 'You will be automatically logged out once the game is over.', 0, 5)
        self.username_label = TextLabel(self, self.parent, 'Username: ', 0, 10)
        self.username_entry = TextEntry(self, self.parent, '', 0, 10)
        self.password_label = TextLabel(self, self.parent, 'Password: ', 0, 10)
        self.password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.confirm_password_label = TextLabel(self, self.parent, 'Confirm Password: ', 0, 10)
        self.confirm_password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.login_create_account = TextButton(self, self.parent, 'Confirm', lambda: self.create_account(), 0, 20)
        self.alert = AlertLabel(self, self.parent, '', 0, 10)
        self.watermark = WatermarkLabel(self, self.parent)

    def create_account(self):
        username, password = self.username_entry.get(), self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        pass_check_result = security.password_check(password, confirm_password)

        if pass_check_result is None:
            if not database.user_exists(username):
                self.parent.p2 = Player(username)
                database.add_user(username, password, 'blue', 0.2)
                self.parent.switch_frame(DuoGame)

            else:
                self.alert.configure(text='Username already taken')

        else:
            self.alert.configure(text=pass_check_result)


class DuoGame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[0])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title(f'Duo game - {self.parent.p1.username} vs {self.parent.p2.username}')
        self.game = Game()

        self.quit_button = QuitButton(self, self.parent, self.quit, GameMenu)
        self.save_button = SaveButton(self, self.parent, self.save, GameMenu)
        self.title = GameTitle(self, self.parent, 'Duo game')
        self.p1_title = P1Title(self, self.parent, f'Player One:\n{self.parent.p1.username}')
        self.score_title = Score(self, self.parent,
                                 f'Round: {self.game.round}\n\nScore:\n{self.parent.p1.score} : {self.parent.p2.score}')
        self.p2_title = P2Title(self, self.parent, f'Player Two\n{self.parent.p2.username}')
        self.p1_frame = P1Frame(self, self.parent)
        self.border = BorderFrame(self, self.parent)
        self.p2_frame = P2Frame(self, self.parent)
        self.parent.p1.dice1 = P1Dice1(self.p1_frame, self.parent)
        self.parent.p1.dice2 = P1Dice2(self.p1_frame, self.parent)
        self.parent.p1.calc_box = P1CalcBox(self.p1_frame, self.parent, 'Result:\nNothing')
        self.parent.p2.dice1 = P2Dice1(self.p2_frame, self.parent)
        self.parent.p2.dice2 = P2Dice2(self.p2_frame, self.parent)
        self.parent.p2.calc_box = P2CalcBox(self.p2_frame, self.parent, 'Result:\nNothing')
        self.parent.p1.roll_button = P1RollButton(self.p1_frame, self.parent,
                                                  lambda: self.roll(self.parent.p1, self.parent.p2))
        self.parent.p1.info = P1Info(self.p1_frame, self.parent)
        self.parent.p2.roll_button = P2RollButton(self.p2_frame, self.parent,
                                                  lambda: self.roll(self.parent.p2, self.parent.p1))
        self.parent.p2.info = P2Info(self.p2_frame, self.parent)

        self.parent.p2.roll_button['state'] = 'disabled'
        self.parent.bind('<Key-Shift_L>', lambda event: self.roll(self.parent.p1, self.parent.p2))
        self.parent.bind('<Key-Return>', lambda event: self.roll(self.parent.p2, self.parent.p1))

    def roll(self, p, o_p):
        if (self.game.round <= 6 or self.parent.p1.score == self.parent.p2.score) and self.game.turn == p:
            p.reset()

            p.roll_1 = random.randint(1, 6)
            p.roll_2 = random.randint(1, 6)
            p.score += p.roll_1 + p.roll_2

            p.dice1.configure(image=self.parent.dice[p.roll_1 - 1])
            p.dice2.configure(image=self.parent.dice[p.roll_2 - 1])

            if (p.roll_1 + p.roll_2) % 2 == 0:
                p.calc += 'Even number, have 10 points!'
                p.score += 10

            else:
                p.calc += 'Odd number, lose ten points.'
                p.score -= 5

            if p.roll_1 == p.roll_2:
                p.calc += '\nYou rolled a double, have a free roll!'
                p.roll_again = True

            if p.score < 0:
                p.score = 0

            p.calc_box.configure(text=p.calc)

            self.score_title.configure(
                text=f'Round: {self.game.round}\n\nScore\n{self.parent.p1.score} : {self.parent.p2.score}')

            if not p.roll_again:
                p.roll_button['state'] = 'disabled'
                o_p.roll_button['state'] = 'normal'
                self.game.turn = o_p

                if p == self.parent.p2:
                    self.game.round += 1

        else:
            self.parent.switch_frame(GameOver)

    def quit(self):
        self.quit_message = messagebox.askokcancel(title='Confirm',
                                                   message='Are you sure you want to quit?\n'
                                                           'game progress will not be saved.')
        if self.quit_message:
            self.parent.switch(GameMenu)

    def save(self):
        self.save_message = messagebox.askokcancel(title='Confirm',
                                                   message='Are you sure you want to quit?\n'
                                                           'game progress will not be saved.')
        if self.save_message:
            database.add_game(database.gen_code(), self.parent.p1, self.parent.p1.score, self.parent.p2,
                              self.parent.p2.score, self.game.round, self.game.p)
            self.parent.switch(GameMenu)
