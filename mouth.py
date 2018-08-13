import random
import re

class Response:
    """ 応答クラスのスーパークラス
    """
    def __init__(self, name, memory):
        self.name = name
        self.memory = memory

    def response(self, input, mood):
        return ''

    def getName(self):
        return self.name

class RandomResponse(Response):
    """ 適当に答える
    """
    def response(self, input, mood):
        return random.choice(self.memory.random)

class PatternResponse(Response):
    """ しっかり答える
    """
    def response(self, input, mood):
        self.resp = None
        for umr_line in self.memory.pattern:
            m = umr_line.match(input)
            if (m):
                self.resp = umr_line.choice(mood)
            # 応答例の中の%match%をインプットされた文字列内の
            # マッチした文字列に置き換える
            if self.resp != None:
                return re.sub('%match%', m.group(), self.resp)
        # パターンマッチしない場合はランダム辞書から返す
        return random.choice(self.memory.random)
