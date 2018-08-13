import random
import re

class Brain:
    def __init__(self):
        self.random = []
      
        random_file = open('memory/storage.txt', 'r', encoding = 'utf_8')
        # 各行を要素としてリストに格納
        random_lines = random_file.readlines()
        random_file.close()

        self.random = []
        for line in random_lines:
            str = line.rstrip('\n')
            if (str!=''):
                 # リストに格納
                self.random.append(str)


        pattern_file = open('memory/pattern.txt', 'r', encoding = 'utf_8')

        pattern_lines = pattern_file.readlines()
        pattern_file.close()

        self.new_lines = []
        for line in pattern_lines:
            str = line.rstrip('\n')
            if (str!=''):
                self.new_lines.append(str)

        self.pattern = []

        for line in self.new_lines:
            regex, response = line.split('\t')
            self.pattern.append(ParseItem(regex, response))

    def study(self, input):
        """ ユーザーの発言を学習する
        """
        input = input.rstrip('\n')
        # 発言がランダム辞書に存在しなければself.randomの末尾に追加
        if not input in self.random:
            self.random.append(input)

    def memorize(self):
        """ self.randomの内容をまるごと辞書に書き込む
        """
        for index, element in enumerate(self.random):
            self.random[index] = element +'\n'
        # 書き込み
        with open('memory/storage.txt', 'w', encoding = 'utf_8') as f:
            f.writelines(self.random)

class ParseItem:
    SEPARATOR = '^((-?\d+)##)?(.*)$'

    def __init__(self, pattern, phrases):
        # 辞書のパターンの部分にSEPARATORをパターンマッチさせる
        m = re.findall(ParseItem.SEPARATOR, pattern)
        self.judge = 0
        
        if m[0][1]:
          self.judge =int(m[0][1])
        # インスタンス変数patternにマッチ結果のパターン部分を代入
        self.pattern = m[0][2]
        
        self.phrases = []   # 応答例を保持するインスタンス変数
        self.memory = {} 
       
        for phrase in phrases.split('|'):
            # 応答例に対してパターンマッチを行う
            m = re.findall(ParseItem.SEPARATOR, phrase)
            self.memory['need'] = 0
            if m[0][1]:
                self.memory['need'] = int(m[0][1])
            self.memory['phrase'] = m[0][2]
            self.phrases.append(self.memory.copy())

    def match(self, str):
        """入力した文字列にパターンマッチ
            を行う
        """
        return re.search(self.pattern, str)

    def choice(self, mood):
        choices = []
        for line in self.phrases:
            if (self.suitable(line['need'], mood)):
                choices.append(line['phrase'])
        if (len(choices) == 0):
            return None
        return random.choice(choices)

    def suitable(self, need, mood):
        """ @ptam need 必要ムード値
            @ptam mood 現在のムード値
        """
        if (need == 0):
            return True
        elif (need > 0):
            return (mood > need)
        else:
            return (mood < need)

        # 辞書データの各行をタブで切り分ける
        # regex 正規表現のパターン
        # response 応答例
        # ParseItemオブジェクトを生成(引数はregex、response）して
        # インスタンス変数pattern（リスト）に追加

        # 引数で渡された応答例を'|'で分割し、
        # 個々の要素に対してSEPARATORをパターンマッチさせる
        # self.phrases[ 'need'  : 応答例の整数部分
        #               'phrase': 応答例の文字列部分 ]