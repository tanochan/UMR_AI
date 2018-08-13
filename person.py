from mouth import *
from head import *

class Umr:
    def __init__(self, name):
        self.name = name
        self.brain = Brain()
        self.emotion = Emotion(self.brain)
        
        self.res_random = RandomResponse('Random', self.brain)
        self.res_pattern = PatternResponse('Pattern', self.brain)

    def getPhrase(self, input):
        """ 応答フレーズを取得する
        """
        self.emotion.recovery(input)
        
        x = random.randint(1, 100)
     
        if x <= 100:
            self.responder = self.res_pattern
        else:
            self.responder = self.res_random

        # 応答フレーズを生成
        resp = self.responder.response(input, self.emotion.mood)
        print(self.emotion.mood)

        self.brain.study(input)
       
        return resp

    def memorize(self):
        self.brain.memorize()
        

class Emotion:
    MIN = -20
    MAX = 20
    RECOVERY = 1

    def __init__(self, memory):
        self.memory = memory
        self.mood = 0

    def recovery(self, input):
        if self.mood < 0:
          self.mood += Emotion.RECOVERY
        # パターン辞書の各行を繰り返しパターンマッチさせる
        for umr_line in self.memory.pattern:
            # パターンマッチすればadjustで機嫌値を変動させる
            if umr_line.match(input):
                self.adjust(umr_line.judge)
                break

    def adjust(self, num):
        """ mood値を調整
        """
        self.mood += int(num)

        if self.mood > Emotion.MAX:
          self.mood = Emotion.MAX
        elif self.mood < Emotion.MIN:
          self.mood = Emotion.MIN
