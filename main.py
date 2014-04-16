__version__ = '0.2.2'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from time import sleep



class PongPaddle (Widget):
    score = NumericProperty (0)

    def bounce_ball (self, ball, player):
        if self.collide_widget (ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector (-1 * vx, vy)
            vel = bounced * 1.05
            ball.velocity = vel.x, vel.y +offset
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
    
    def __init__ (self):
        super (PongGame, self) . __init__ ()

        
    def serve_ball (self):
        self.ball.center = self.center
        vel = (- self.width / 140, 0)
        self.ball.velocity = vel

    def update (self, dt):
        if self.ball.velocity == [0,0] and self.player2.score < 5:
	    self.serve_ball ()
        if self.player2.score >= 5:
            self.player1.center_y = self.player1.center_y
            self.player2.center_y = self.player2.center_y
        elif self.player1.center_y - 2 < self.y:
            self.player1.center_y = self.y
            self.player2.center_y = self.ball.center_y
        else:
            self.player1.center_y = self.player1.center_y - 2
            self.player2.center_y = self.ball.center_y

        self.player1.bounce_ball (self.ball, self.player1)
        self.player2.bounce_ball (self.ball, None)

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            if self.player2.score < 5:
                self.serve_ball ()
            elif self.player2.score >= 5:
                self.ball.velocity = (0,0)
                self.add_widget (Label (text = 'Game over', font_size='50sp', color=(0.686, 0.067, 0.106, 1), center = self.center))

        if self.ball.x > self.width:
            self.serve_ball ()
        self.ball.move ()

    def on_touch_move (self, touch):
        if touch.x < self.width:
            if self.player1.center_y + 50 < self.top and self.player2.score <=5:
                self.player1.center_y = self.player1.center_y + 50
            elif self.player2.score >= 5:
                self.player1.center_y = self.player1.center_y
            else:
                self.player1.center_y = self.top


class LazyPongApp (App):

    use_kivy_settings = False
    
    def build (self):
        game = PongGame ()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    LazyPongApp().run()