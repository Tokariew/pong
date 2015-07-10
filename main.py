__version__ = '0.2.8'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from time import sleep
from kivy.core.window import Window
from kivy.animation import Animation
from math import sin, cos, pi

text = Label (text = 'Game over', font_size='50sp', color=(0.686, 0.067, 0.106, 1), center = Window.center)

class PongPaddle (Widget):
    score = NumericProperty (0)
    bounce = NumericProperty (0)

    def bounce_ball (self, ball, player):
        if self.collide_widget (ball) and self.bounce < 0:
            self.bounce = 12
            if self.x < Window.width / 2.0:
	        factor  =  1
	    else:
	        factor = -1
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2) * 30 * pi /180.0 * factor
            bounced = Vector (-1 * vx, vy)
            vel = bounced * 1.05
            ball.velocity = vel.x * cos (offset) - vel.y * sin (offset), vel.x * sin (offset) + vel.y * cos (offset)
            try:
                player.score += 1
            except AttributeError:
                pass

class PongBall (Widget):
    velocity_x = NumericProperty (0)
    velocity_y = NumericProperty (0)
    velocity = ReferenceListProperty (velocity_x, velocity_y)

    def move (self):
        self.pos = Vector (*self.velocity) + self.pos

class PongGame (Widget):
    ball = ObjectProperty (None)
    player1 = ObjectProperty (None)
    player2 = ObjectProperty (None)

    def __init__ (self, **kwargs):
        super (PongGame, self) . __init__ ()
        self.restart


    def serve_ball (self, vel = (-Window.width / 140.0, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        self.player1.center_y = self.center_y
        self.player2.center_y = self.center_y

    def move_player2 (self):
        if self.player2.score >= 5:
            self.player2.center_y = self.player2.center_y
        elif self.player2.y - Window.height / 300.0 < self.y:
            self.player2.y = self.y
        else:
            self.player2.center_y = self.player2.center_y - Window.height / 300.0

        if self.player2.center_y < self.ball.center_y - Window.height / 8.0:
	    if self.player2.top + Window.height * 15 / 128.0 < self.top: 
                self.player2.center_y += Window.height * 15 / 128.0


    def update (self, dt):
        if self.ball.velocity == [0,0] and self.player2.score < 5:
            self.serve_ball ()
        if self.player2.score >= 5:
            self.player1.center_y = self.player1.center_y
        elif self.player1.y - Window.height / 300.0 < self.y:
            self.player1.y = self.y
        else:
            self.player1.center_y = self.player1.center_y - Window.height / 300.0

        self.player1.bounce_ball (self.ball, self.player1)
        self.player2.bounce_ball (self.ball, None)
        self.player1.bounce -= 1
        self.player2.bounce -= 1

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            if self.player2.score < 5:
                self.serve_ball ()
            elif self.player2.score >= 5:
                self.serve_ball ((0,0))
                self.end ()


        if self.ball.x > self.width:
            self.serve_ball ()
        self.move_player2 ()
        self.ball.move ()

    def on_touch_move (self, touch):
        if touch.x < self.width:
            if self.player1.center_y + Window.height / 8 < self.top and self.player2.score <=5:
                self.player1.center_y = self.player1.center_y + Window.height / 16
            elif self.player2.score >= 5:
                self.player1.center_y = self.player1.center_y
            else:
                self.player1.top = self.top

    def end (self):
        end = self.ids.end.__self__
        self.remove_widget (end)
        self.add_widget (end)
        Animation (opacity = 1., d=.5).start(end)

    def restart (self):
        self.player2.score = 0
        self.player1.score = 0
        Clock.schedule_once (self.update, 1/60.0)
        self.ids.end.opacity = 0
        self.player1.center_y = self.center_y
        self.player2.center_y = self.center_y



class LazyPongApp (App):

    use_kivy_settings = False

    def build (self):
        game = PongGame ()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    LazyPongApp().run()