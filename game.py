from livewires import games, color
from random import randint, choice

games.init(screen_width=900, screen_height=600, fps=50)


class Object(games.Sprite):
    def __init__(self, x, y):
        super(Object, self).__init__(image=games.load_image("images/obj2.png"),
                                     x=x,
                                     y=y)

    def update(self):
        self.destroy()


class Trash(games.Sprite):
    trash1 = 1
    trash2 = 2
    images = {trash1: games.load_image("images/boots.png"),
              trash2: games.load_image("images/trash.png")}

    def __init__(self, x, y):
        super(Trash, self).__init__(image=Trash.images[choice([Trash.trash1,
                                                               Trash.trash2])],
                                    x=x, y=y,
                                    dx=randint(-1, 0) or randint(1, 2))

    def update(self):
        if self.left > games.screen.width:
            self.y = randint(250, games.screen.height)
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width
            self.y = randint(250, games.screen.height)


class Fish(games.Sprite):

    fish1 = 1
    fish2 = 2
    fish3 = 3
    fish4 = 4

    images = {fish1: games.load_image("images/fish1.png"),
              fish2: games.load_image("images/fish2.png"),
              fish3: games.load_image("images/fish3.png"),
              fish4: games.load_image("images/fish4.png")}

    def __init__(self, x, y):
        n = choice([Fish.fish1, Fish.fish2, Fish.fish3, Fish.fish4])
        self.choice1 = Fish.images[n]

        if n == 3:
            dx = randint(1, 2)
        else:
            dx = randint(-2, -1)
        super(Fish, self).__init__(image=self.choice1,
                                   x=x, y=y,
                                   dx=dx,
                                   dy=randint(-1, 1))

    def update(self):
        if self.left > games.screen.width:
            self.y = randint(250, games.screen.height)
            self.right = 0
        if self.right < 0:
            self.left = games.screen.width
            self.y = randint(250, games.screen.height)

        if self.top < games.screen.height / 2 - 100:
            self.dy = randint(0, 1)
        elif self.bottom > games.screen.height:
            self.dy = randint(-1, 0)


class Boat(games.Sprite):

    image = games.load_image('images/boat2.png')

    def __init__(self, x, y):
        super(Boat, self).__init__(image=Boat.image,
                                   x=x,
                                   y=y)

    def update(self):
        self.destroy()


class FishingRod(games.Sprite):

    image = games.load_image("images/rod.png")

    def __init__(self, x, list1, list2):
        super(FishingRod, self).__init__(image=FishingRod.image,
                                         x=x,
                                         y=250)
        self.score = games.Text(value=0,
                                size=40,
                                right=games.screen.width - 60,
                                top=20,
                                color=color.black)
        self.fail = games.Text(value=0,
                                size=40,
                                right=65,
                                top=20,
                                color=color.black)
        games.screen.add(self.score)
        games.screen.add(self.fail)
        self.list1 = list1
        self.list2 = list2
        self.dict_1 = {}
        self.dict_2 = {}

    def move_up(self):
        self.y -= 3

    def move_down(self):
        self.y += 3

    def update(self):

        if games.keyboard.is_pressed(games.K_d):
            self.x += 2
        if games.keyboard.is_pressed(games.K_a):
            self.x -= 2

        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width

        if games.keyboard.is_pressed(games.K_w):
            self.move_up()
        elif games.keyboard.is_pressed(games.K_s):
            self.move_down()


        boat = Boat(x=self.x+17, y=110)
        games.screen.add(boat)

        self.obj = Object(x=self.x-15, y=self.y+175)
        games.screen.add(self.obj)

        if self.top > boat.bottom - 35:
            self.top = boat.bottom - 35
        if self.bottom < boat.bottom + 50:
            self.bottom = boat.bottom + 50
        self.check_fish()
        self.check_trash()
        self.score.value = len(self.dict_1)
        self.fail.value = len(self.dict_2)
        if len(self.dict_2) >= 2:
            self.game_over()
        if len(self.dict_1) == 15:
            self.win()

    def win(self):
        games.music.stop()
        games.screen.clear()
        games.music.load("images/win.mp3")
        games.music.play(-1)
        f = GoodFinal(480, 350)
        games.screen.add(f)
        text = games.Text(value="Score: " + str(self.score.value),
                          size=80,
                          right=games.screen.width - 20,
                          bottom=games.screen.height - 20,
                          color=color.black)
        games.screen.add(text)

    def game_over(self):
        games.music.stop()
        games.screen.clear()
        games.music.load("images/final.mp3")
        games.music.play(-1)
        f = BadFinal(480, 350)
        games.screen.add(f)
        text = games.Text(value="Score: " + str(self.score.value),
                          size=80,
                          right=games.screen.width - 20,
                          bottom=games.screen.height - 20,
                          color=color.black)
        games.screen.add(text)


    def check_fish(self):
        for i in range(len(self.list1)):
            if self.list1[i].overlaps(self.obj) and games.keyboard.is_pressed(games.K_SPACE):
                self.list1[i].destroy()
                self.dict_1[i] = 1


    def check_trash(self):
        for i in range(len(self.list2)):
            if self.list2[i].overlaps(self.obj) and games.keyboard.is_pressed(games.K_SPACE):
                self.list2[i].destroy()
                self.dict_2[i] = 1
                #self.game_over()


class GoodFinal(games.Sprite):
    def __init__(self, x, y):
        super(GoodFinal, self).__init__(image=games.load_image("images/good.png"),
                                    x=x,
                                    y=y)


class BadFinal(games.Sprite):
    def __init__(self, x, y):
        super(BadFinal, self).__init__(image=games.load_image("images/final.png"),
                                    x=x,
                                    y=y)


class Game:

    def play(self):
        bg = games.load_image("images/back.png", transparent=False)
        games.screen.background = bg
        list_fish = []
        list_trash = []

        for _ in range(15):
            x = randint(0, games.screen.width)
            y = randint(250, games.screen.height)
            new_fish = Fish(x=x, y=y)
            list_fish.append(new_fish)
            games.screen.add(new_fish)

        for _ in range(4):
            x = randint(0, games.screen.width)
            y = randint(250, games.screen.height)
            new_trash = Trash(x=x, y=y)
            list_trash.append(new_trash)
            games.screen.add(new_trash)

        rod = FishingRod(games.screen.width / 2, list_fish, list_trash)
        games.screen.add(rod)


class FirstBg(games.Sprite):
    def __init__(self, x, y):
        super(FirstBg, self).__init__(image=games.load_image("images/bg2.png"),
                                      x=x,
                                      y=y)

    def update(self):
        if games.keyboard.is_pressed(games.K_a):
            self.destroy()
            game = Game()
            game.play()


def main():
    games.music.load("images/music2.mp3")
    games.music.play(-1)
    f = FirstBg(480, 130)
    games.screen.add(f)
    games.screen.mainloop()


if __name__ == '__main__':
    main()
