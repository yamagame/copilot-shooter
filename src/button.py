import pyxel

class Button:
    def __init__(self):
        self.start_buttons = [
            pyxel.KEY_SPACE,
            pyxel.GAMEPAD1_BUTTON_START,
            pyxel.MOUSE_BUTTON_LEFT
        ]
        self.shot_buttons = [
            pyxel.KEY_SPACE,
            pyxel.GAMEPAD1_BUTTON_A,
            pyxel.GAMEPAD1_BUTTON_B,
            pyxel.GAMEPAD1_BUTTON_X,
            pyxel.GAMEPAD1_BUTTON_Y,
        ]
        self.startPushed = False
        self.shotPushed = False
        self.shotPressed = False

    def is_start_pressed(self):
        return any(pyxel.btnp(button) for button in self.start_buttons)

    def is_shot_pressed(self):
        return any(pyxel.btnp(button) for button in self.shot_buttons)
    
    def update(self):
        self.startPushed = self.is_start_pressed()
        self.shotPushed = self.is_start_pressed() or self.is_shot_pressed()
        self.shotPressed = any(pyxel.btn(button) for button in self.shot_buttons)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.mouse_start_x, _ = self.get_mouse_position()
            self.shotPushed = True
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.shotPressed = True

    def is_mouse_left_pressed(self):
        return pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)

    def get_mouse_position(self):
        return pyxel.mouse_x, pyxel.mouse_y
