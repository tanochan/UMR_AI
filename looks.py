from person import *
from datetime import datetime
import tkinter as tk
import tkinter.messagebox

entry1 = None   
entry2 = None        
response_area = None   
listbox = None             
umr = Umr('UMR')
umr_canvas = None       
moji_canvas = None
umr_images = []         #感情画像リスト
moji_images = []        #文字画像リスト
log = []             

def putLog(str):
    listbox.insert(tk.END, str)
    log.append(str + '\n')

def partition():
    return umr.name + ' > '


def setUmrImg(img):
    canvas1.itemconfig(
        umr_canvas,
        image = umr_images[img]
    )

def setMojiImg(img):
    canvas2.itemconfig(
        moji_canvas,
        image = moji_images[img]
    )

def changeLooks():
    em =umr.emotion.mood
    #喜
    if 10 <= em <= 20:
        setUmrImg(0)
        setMojiImg(0)
    #楽
    elif 0 <= em < 10:
        setUmrImg(1)
        setMojiImg(1)
    #怒
    elif -10 <= em < 0:
        setUmrImg(2)
        setMojiImg(2)
    #哀
    elif -20 < em <= -10:
        setUmrImg(3)
        setMojiImg(3)


def talk():
    """ 会話をする
    """
    statement = entry1.get()
    name = entry2.get()
    #名前が未入力の場合
    if(name == "たいへい" or name == "お兄ちゃん"):
        # 入力エリアが未入力の場合
        if not statement:
            response_area.configure(text="どったのー？")
        else:
            # 応答フレーズを取得
            response = umr.getPhrase(statement)
            response_area.configure(text=response)
            putLog('> ' + statement)
            putLog(partition() + response)
            # 入力エリアをクリア
            entry1.delete(0, tk.END)

    changeLooks() #画像チェンジ

def writeLog():
    """ ログファイルに辞書を更新した日時を記録
    """
    # ログを作成
    now = 'Phrase Log: ' + datetime.now().strftime(
                                   '%Y-%m-%d' + '\n')
    print(log)
    log.insert(0, now)
    print(log)
    # ログファイルへの書き込み
    with open('PhraseLog.txt', 'a', encoding = 'utf_8') as f:
        f.writelines(log)

# UI形成
def create():
    # グローバル変数を使用するための記述
    global entry1, entry2, response_area, listbox, canvas1, canvas2, umr_canvas, umr_images, moji_canvas, moji_images, judge

    root = tk.Tk()
    root.geometry('1100x800')
    root.title('Umaru AI : ')
    font=('Helevetica', 14)
    font_log=('Helevetica', 14)

    def callback():
        """ 終了時の処理
        """
        # メッセージボックスの[OK]ボタンクリック時の処理
        if tkinter.messagebox.askyesno(
            'Quit?', '記憶しますか?'):
            umr.memorize() 
            writeLog()  # ログの保存
            root.destroy()
	    # [キャンセル]ボタンクリック
        else:
            root.destroy()

    root.protocol('WM_DELETE_WINDOW', callback)
    
    #たいへい以外受け付けない
    def judgeName():
        name = entry2.get()
        if not (name == "たいへい" or name == "お兄ちゃん"):
            root.quit()
        else:
            response_area.configure(text="うっひょーーーーう！!")

    # メニューバーの作成
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    #「ファイル」メニュー
    filemenu = tk.Menu(menubar)
    menubar.add_cascade(label='ファイル', menu=filemenu)
    filemenu.add_command(label='閉じる', command=callback)
    
    canvas1 = tk.Canvas(
                root,
                width = 300,
                height = 400,
             )
    canvas1.place(x=600, y=90)
    
    # 感情イメージを準備
    umr_images.append(tk.PhotoImage(file = 'picture/happy.png'))
    umr_images.append(tk.PhotoImage(file = 'picture/normal.png'))
    umr_images.append(tk.PhotoImage(file = 'picture/angry.png'))
    umr_images.append(tk.PhotoImage(file = 'picture/sad.png'))

    # 感情イメージを配置
    umr_canvas = canvas1.create_image(
        0,
        0,
        image = umr_images[1],
        anchor = tk.NW,
    )
    
    canvas2 = tk.Canvas(
                root,
                width = 480,
                height = 80,
                relief=tk.RAISED,
                bd=3,
            )
    canvas2.place(x=510, y=25)

    #文字イメージを準備
    moji_images.append(tk.PhotoImage(file = 'picture/喜.png'))
    moji_images.append(tk.PhotoImage(file = 'picture/楽.png'))
    moji_images.append(tk.PhotoImage(file = 'picture/怒.png'))
    moji_images.append(tk.PhotoImage(file = 'picture/悲.png'))

    #文字イメージを配置
    moji_canvas = canvas2.create_image(
        10,
        15,
        image = moji_images[1],
        anchor = tk.NW
    )
    

    # 応答エリア作成
    response_area = tk.Label(
                        root,
                        width=45,
                        height=5,
                        font=('',20),
                        relief=tk.RIDGE,
                        bd=5
                    )
    response_area.configure(text="だれっ！？")
    response_area.place(x=450, y=500)

    frame1 = tk.Frame(
                root,
                relief=tk.RIDGE,
                borderwidth=4
            )
    # 入力ボックスの作成
    entry1 = tk.Entry(
                frame1,
                width=50,
                font=font
            )
    entry1.pack(side = tk.LEFT)    
    entry1.focus_set()           
    
    button1 = tk.Button(
                frame1,
                width=10,
                text='話す',
                font=('',20),
                command=talk
             )
    button1.pack(side = tk.LEFT)
    frame1.place(x=450, y=700)
    
    frame2 = tk.Frame(
                      root,
                      relief=tk.RIDGE,
                      borderwidth=4
                      )
    
    #名前入力ボックスの作成
    entry2 = tk.Entry(
                frame2,
                width=25,
                font=font
            )
    entry2.pack(side = tk.LEFT)
    entry2.focus_set()
    
    button2 = tk.Button(
                frame2,
                width=8,
                text='名前？',
                font=('',20),
                command=judgeName
            )
    button2.pack(side = tk.LEFT)
    frame2.place(x=20, y=700)


    # リストボックスを作成
    listbox = tk.Listbox(
            root,               
            width=42,
            height=34,
            font=font_log,
            relief=tk.SUNKEN,
            bd=7,
            bg='burlywood1'
         )
    # 縦のスクロールバーを生成
    sb_length = tk.Scrollbar(
            root,
            orient = tk.VERTICAL,   
            command = listbox.yview      
      )
    # 横のスクロールバーを生成
    sb_side = tk.Scrollbar(
            root,
            orient = tk.HORIZONTAL,
            command = listbox.xview     
          )
    # リストボックスとスクロールバーを連動させる
    listbox.configure(yscrollcommand = sb_length.set)
    listbox.configure(xscrollcommand = sb_side.set)
    
    listbox.grid(row = 0, column = 0)
    sb_length.grid(row = 0, column = 1, sticky = tk.NS)
    sb_side.grid(row = 1, column = 0, sticky = tk.EW)

    root.mainloop()


# 創造
if __name__  == '__main__':
    create()

