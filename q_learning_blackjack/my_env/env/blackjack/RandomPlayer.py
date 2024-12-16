from my_env.env.blackjack.base_package.BasePlayer import BasePlayer
import random

class RandomPlayer(BasePlayer):

  def action(self):
    random_num = random.randint(1, 4)
    if random_num == 1:
      return "h"
    elif random_num == 2:
      return "st"
    elif random_num == 3:
      return "dd"
    elif random_num == 4:
      return "sr"