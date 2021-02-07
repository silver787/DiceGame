from game.game_utilities import *
from tkinter import messagebox


security = Security()
user_db = UserDB(security)
scores_db = HighscoresDB()
helper = Helper()


class TitleLabel(tk.Label):
    def __init__(self, parent, meta_parent, text, padx, pady):
        tk.Label.__init__(self, parent, text=text, font=(FONT, TITLE_FONT_SIZE),
                          fg=meta_parent.font_colour, bg=meta_parent.colour[1])
        self.pack(padx=padx, pady=pady)


class TextLabel(tk.Label):
    def __init__(self, parent, meta_parent, text, padx, pady):
        tk.Label.__init__(self, parent, text=text, fg=meta_parent.font_colour,
                          bg=meta_parent.colour[1])
        self.pack(padx=padx, pady=pady)


class AlertLabel(tk.Label):
    def __init__(self, parent, meta_parent, text, padx, pady):
        tk.Label.__init__(self, parent, text=text, fg='orange',
                          bg=meta_parent.colour[1])
        self.pack(padx=padx, pady=pady)


class UnderlineSubtitle(tk.Label):
    def __init__(self, parent, meta_parent, text, padx, pady):
        tk.Label.__init__(self, parent, text=text, fg=meta_parent.font_colour,
                          bg=meta_parent.colour[1], font=(FONT, 25, "underline"))
        self.pack(padx=padx, pady=pady)


class WatermarkLabel(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, text="© Toby Hogan 2020", fg=meta_parent.font_colour,
                          bg=meta_parent.colour[1], font=(None, 10))
        self.pack(side="bottom")


class TextEntry(tk.Entry):
    def __init__(self, parent, meta_parent, show, padx, pady):
        tk.Entry.__init__(self, parent, fg=meta_parent.font_colour,
                          bg=meta_parent.colour[1], borderwidth=1, relief='flat', show=show)
        self.pack(padx=padx, pady=pady)


class TextButton(tk.Button):
    def __init__(self, parent, meta_parent, text, command, padx, pady):
        tk.Button.__init__(self, parent, text=text, fg='black',
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[1],
                           command=command)

        self.pack(padx=padx, pady=pady)


class MenuButton(tk.Button):
    def __init__(self, parent, meta_parent, text, command, x, y, padx, pady):
        tk.Button.__init__(self, parent, text=text, fg='black',
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[1],
                           width=x, height=y,
                           command=command)

        self.pack(padx=padx, pady=pady)


class BackButton(tk.Button):
    def __init__(self, parent, meta_parent, last_frame):
        tk.Button.__init__(self, parent, text='Back', fg='black',
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[1],
                           command=lambda: meta_parent.switch_frame(last_frame))

        self.pack(anchor='nw', padx=5, pady=5)


class VolumeScale(tk.Scale):
    def __init__(self, parent, meta_parent, command, padx, pady):
        tk.Scale.__init__(self, parent, orient="horizontal",
                          bg=meta_parent.colour[1], fg=meta_parent.font_colour,
                          length=80, troughcolor=meta_parent.colour[1], showvalue=0,
                          highlightcolor=meta_parent.colour[1],
                          highlightbackground=meta_parent.colour[1],
                          activebackground=meta_parent.colour[1], command=command)
        self.pack(padx=padx, pady=pady)


class ThemeCheckbox(tk.Checkbutton):
    def __init__(self, parent, meta_parent, text, padx, pady):
        tk.Checkbutton.__init__(self, parent, text=text, bg=meta_parent.colour[1],
                                fg=meta_parent.font_colour, command=lambda: parent.change_theme(text.lower(), self))
        self.deselect()
        self.pack(padx=padx, pady=pady)


class SettingsOption(tk.Button):
    def __init__(self, parent, meta_parent, text, command, padx, pady):
        tk.Button.__init__(self, parent, text=text, bg=meta_parent.colour[1],
                           highlightbackground=meta_parent.colour[1],
                           command=command)

        self.pack(anchor='se', padx=5, pady=2)


class QuitButton(tk.Button):
    def __init__(self, parent, meta_parent, command, last_frame):
        tk.Button.__init__(self, parent, text='Quit', fg='black',
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[0],
                           command=command)

        self.pack(anchor='nw', pady=5)


class SaveButton(tk.Button):
    def __init__(self, parent, meta_parent, command, last_frame):
        tk.Button.__init__(self, parent, text='Save', fg='black',
                           bg=meta_parent.colour[1], highlightbackground=meta_parent.colour[0],
                           command=command)

        self.pack(anchor='nw')


class GameTitle(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[0], fg=meta_parent.font_colour,
                          font=(FONT, 30))
        self.grid(column=0, row=0, columnspan=3, pady=4)


class P1Title(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[0],
                          fg=meta_parent.font_colour,
                          width=10)
        self.grid(column=0, row=1, sticky="N")


class Score(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text,
                          bg=meta_parent.colour[0], fg=meta_parent.font_colour, width=10)
        self.grid(column=1, row=1, sticky="N")


class P2Title(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[0],
                          fg=meta_parent.font_colour,
                          width=10)
        self.grid(column=2, row=1, sticky="N")


class P1Frame(tk.Frame):
    def __init__(self, parent, meta_parent):
        tk.Frame.__init__(self, parent, bg=meta_parent.colour[1], width=WINDOW_WIDTH / 100 * 40,
                          height=WINDOW_HEIGHT / 4 * 3)
        self.grid(column=0, row=2, sticky="N", padx=5)

        self.pack_propagate(0)


class BorderFrame(tk.Frame):
    def __init__(self, parent, meta_parent):
        tk.Frame.__init__(self, parent, bg=meta_parent.colour[0], width=WINDOW_WIDTH / 100 * 2)
        self.grid(column=1, row=2)


class P2Frame(tk.Frame):
    def __init__(self, parent, meta_parent):
        tk.Frame.__init__(self, parent, bg=meta_parent.colour[1], width=WINDOW_WIDTH / 100 * 40,
                          height=WINDOW_HEIGHT / 4 * 3)
        self.grid(column=2, row=2, sticky="N", padx=5)
        self.pack_propagate(0)


class P1Dice1(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, bg=meta_parent.colour[1],
                          image=meta_parent.dice[5])
        self.pack(pady=5, side="top")


class P1Dice2(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, bg=meta_parent.colour[1],
                          image=meta_parent.dice[5])
        self.pack(pady=5, side="top")


class P1CalcBox(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[1],
                          fg=meta_parent.font_colour,
                          width=50, height=5)

        self.pack(pady=5)


class P2Dice1(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, bg=meta_parent.colour[1],
                          image=meta_parent.dice[5])
        self.pack(pady=5, side="top")


class P2Dice2(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, bg=meta_parent.colour[1],
                          image=meta_parent.dice[5])
        self.pack(pady=5, side="top")


class P2CalcBox(tk.Label):
    def __init__(self, parent, meta_parent, text):
        tk.Label.__init__(self, parent, text=text, bg=meta_parent.colour[1],
                          fg=meta_parent.font_colour,
                          width=50, height=5)
        self.pack(pady=5)


class P1RollButton(tk.Button):
    def __init__(self, parent, meta_parent, command):
        tk.Button.__init__(self, parent, text="ROLL!", bg=meta_parent.colour[1],
                           highlightbackground=meta_parent.colour[1],
                           command=command)
        self.pack()


class P1Info(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, text="OR Press Left Shift!", bg=meta_parent.colour[1],
                          fg=meta_parent.font_colour,
                          height=5)

        self.pack()


class P2RollButton(tk.Button):
    def __init__(self, parent, meta_parent, command):
        tk.Button.__init__(self, parent, text="ROLL!", bg=meta_parent.colour[1],
                           highlightbackground=meta_parent.colour[1],
                           command=command)
        self.pack()


class P2Info(tk.Label):
    def __init__(self, parent, meta_parent):
        tk.Label.__init__(self, parent, text="OR Press Return!", bg=meta_parent.colour[1],
                          fg=meta_parent.font_colour,
                          height=5)

        self.pack()


class P1Login(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title('Login')
        self.alert_made = False

        self.parent.colour = BLUE
        self.parent.font_colour = 'white'
        self.parent.dice = BLUE_DICE
        self.parent.configure(bg=self.parent.colour[0])

        self.title = TitleLabel(self, self.parent, 'Login', 0, 30)
        self.username_label = TextLabel(self, self.parent, 'Username: ', 0, 10)
        self.username_entry = TextEntry(self, self.parent, '', 0, 10)
        self.password_label = TextLabel(self, self.parent, 'Password: ', 0, 10)
        self.password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.login_button = TextButton(self, self.parent, 'Confirm', lambda: self.login(), 0, 20)
        self.create_account_label = TextLabel(self, self.parent, "Don't have an account?\n\nCreate an account:", 0, 30)
        self.create_account_button = TextButton(self, self.parent, 'Confirm',
                                                lambda: self.parent.switch_frame(P1Create), 0, 10)
        self.watermark = WatermarkLabel(self, self.parent)

    def login(self):
        username, password = self.username_entry.get(), self.password_entry.get()

        if user_db.check_user(username, password):
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0)
            self.parent.p1 = Player(username, 1)
            colour, volume = user_db.get_user_details(self.parent.p1.username)[2:4]
            helper.switch_user(self.parent, colour, volume)
            self.parent.switch_frame(GameMenu)

        elif not self.alert_made:
            self.alert = AlertLabel(self, self.parent, 'Invalid credentials', 0, 10)
            self.alert_made = True


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
            if not user_db.user_exists(username):
                self.parent.p1 = Player(username, 1)
                user_db.add_user(username, password, 'blue', 0.2)
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
        self.parent.title(f'Game Menu - {self.parent.p1.username}')

        self.title = TitleLabel(self, self.parent, 'Game Menu', 0, 60)
        self.duo_button = MenuButton(self, self.parent, 'Duo game',
                                     lambda: self.parent.switch_frame(P2Login), 25, 2, 0, 15)
        self.online_button = MenuButton(self, self.parent, 'Online game',
                                        lambda: self.parent.switch_frame(OnlineGameInit), 25, 2, 0, 15)
        self.rules_button = MenuButton(self, self.parent, 'Rules',
                                       lambda: self.parent.switch_frame(Rules), 25, 2, 0, 15)
        self.settings_button = MenuButton(self, self.parent, 'Settings',
                                          lambda: self.parent.switch_frame(Settings), 25, 2, 0, 15)

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
        self.log_out_button = SettingsOption(self, self.parent, 'log out', self.log_out, 0, 0)
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
        user_db.update_user_volume(self.parent.p1.username, pygame.mixer.music.get_volume())

    def change_theme(self, theme, button):
        self.blue_checkbox.deselect()
        self.green_checkbox.deselect()
        self.black_checkbox.deselect()
        self.white_checkbox.deselect()
        button.select()

        user_db.update_user_theme(self.parent.p1.username, theme)
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
            pygame.mixer.music.stop()
            self.parent.colour = BLUE
            self.parent.font_colour = "white"
            self.parent.dice = BLUE_DICE
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

        self.back_button = BackButton(self, self.parent, GameMenu)
        self.title = TitleLabel(self, self.parent, 'Login', 0, 20)
        self.notice = TextLabel(self, self.parent, 'You will be automatically logged out once the game is over.', 0, 5)
        self.username_label = TextLabel(self, self.parent, 'Username: ', 0, 10)
        self.username_entry = TextEntry(self, self.parent, '', 0, 10)
        self.password_label = TextLabel(self, self.parent, 'Password: ', 0, 10)
        self.password_entry = TextEntry(self, self.parent, '*', 0, 10)
        self.login_button = TextButton(self, self.parent, 'Confirm', lambda: self.login(), 0, 20)
        self.create_account_label = TextLabel(self, self.parent, "Don't have an account?\n\nCreate an account:", 0, 20)
        self.create_account_button = TextButton(self, self.parent, 'Confirm',
                                                lambda: self.parent.switch_frame(P2Create), 0, 10)
        self.watermark = WatermarkLabel(self, self.parent)

    def login(self):
        username, password = self.username_entry.get(), self.password_entry.get()

        if user_db.check_user(username, password):
            self.parent.p2 = Player(username, 2)
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

        self.back_button = BackButton(self, self.parent, P2Login)
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
            if not user_db.user_exists(username):
                self.parent.p2 = Player(username)
                user_db.add_user(username, password, 'blue', 0.2)
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
        if (self.game.round <= 6 or self.parent.p1.score == self.parent.p2.score):
            if self.game.turn == p.num:
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
                    self.game.turn = o_p.num

                    if p == self.parent.p2:
                        self.game.round += 1

        else:

            self.game.round = 0
            self.game.turn = 1
            self.parent.p1.score = 0
            self.parent.p1.roll_again = False
            self.parent.p1.calc = ''
            self.parent.p1.roll_1 = 0
            self.parent.p1.roll_2 = 0
            self.parent.switch_frame(GameOver)

    def quit(self):
        self.quit_message = messagebox.askokcancel(title='Confirm',
                                                   message='Are you sure you want to quit?\n'
                                                           'game progress will not be saved.')
        if self.quit_message:
            self.parent.unbind("<Key-Shift_L>")
            self.parent.unbind("<Key-Return>")
            scores_db.add_highscore(self.parent.p1.username, self.parent.p1.score)
            scores_db.add_highscore(self.parent.p1.username, self.parent.p2.score)
            self.parent.switch_frame(GameMenu)

    def save(self):
        self.save_message = messagebox.askokcancel(title='Confirm',
                                                   message='Are you sure you want to save game?.')
        if self.save_message:
            games_db.add_game(games_db.gen_code(), self.parent.p1, self.parent.p1.score, self.parent.p2,
                              self.parent.p2.score, self.game.round, self.game.p)
            self.parent.switch(GameMenu)


class GameOver(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title(f'Game Over - {self.parent.p1.username}')

        winner = self.parent.p1.username if self.parent.p1.score > self.parent.p2.score else self.parent.p2.username

        self.back_button = BackButton(self, self.parent, GameMenu)
        self.result = TextLabel(self, self.parent, f'Congratulations {winner}, you win!', 0, 20)
        self.scores = TextLabel(self, self.parent, f"Highscores:\n\n" + '\n'.join(scores_db.twenty_scores()), 0, 20)



class OnlineGameInit(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=WINDOW_WIDTH / 5 * 4, height=WINDOW_HEIGHT,
                          bg=parent.colour[1])
        self.pack_propagate(0)
        self.parent = parent
        self.parent.title(f'Online Game - {self.parent.p1.username}')

        self.back_button = BackButton(self, self.parent, GameMenu)
        self.title = TitleLabel(self, self.parent, 'Online Game', 0, 20)
        with open(ONLINE_GAME_INFO_FILE, 'r') as f:
            self.info_label = TextLabel(self, self.parent, f.read(), 0, 20)
        self.server_ip_label = TextLabel(self, self.parent, 'Server IP:\nE.g. 192.168.1.1', 0, 20)
        self.server_ip_entry = TextEntry(self, self.parent, '', 0, 20)
        self.confirm_button = TextButton(self, self.parent, 'confirm',
                                         lambda: self.parent.switch_frame(OnlineGame), 0, 20)
        self.watermark_label = WatermarkLabel(self, self.parent)
