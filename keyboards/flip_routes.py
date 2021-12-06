from aiogram.types import InlineKeyboardMarkup
from aiogram_utils.keyboards import InlineKeyboardButton


class FlipRoutes(InlineKeyboardMarkup):
    FLIP = InlineKeyboardButton('{sign}', callback_data='flip_routes:flip:{index}')
    FAKE_BUTTON = InlineKeyboardButton(' ', callback_data='flip_routes:fake_button')

    def __init__(self, current_index: int):
        super().__init__(row_width=2)

        if current_index > 0:
            self.insert(self.FLIP.format(sign='<<', index=current_index - 1))
        else:
            self.insert(self.FAKE_BUTTON)

        self.insert(self.FLIP.format(sign='>>', index=current_index + 1))
