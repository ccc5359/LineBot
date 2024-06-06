from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, MemberJoinedEvent
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 用户状态字典，用来存储每个用户的状态
user_state = {}

questions_answers = {
    '耽美': {
        "耽美是什麼": "原是日語為翻譯「aestheticism」而創的新詞（與漢語唯美主義相等），而在1970年代日本BL漫畫，引伸為代指一切美形的男性，以及兩名男性之間的戀愛感情。",
        "類型": "在漫畫、小說及影視等皆有涉略，本頻道主要介紹小說類型",
        "主角類型": "攻類型\n健氣攻：陽光、活潑開朗的攻君。\n強攻：個性強悍的攻君。\n傲嬌攻：表面上裝得強硬驕傲，其實內心容易害羞、吃醋，彆扭又可愛的攻君。\n腹黑攻：總是帶著微笑善良的外貌，其實內心充滿詭詐的攻君。\n年下攻：年紀比小受還小的攻君。\n弱氣攻：個性柔弱、被動的攻君。\n天然攻：個性單純無害、鈍感的攻君。\n誘攻：極具誘惑力，會誘惑小受的攻君。\n帝王攻：指天生有著像帝王般霸道氣質的攻君。常為總攻。\n忠犬攻：像忠犬般忠心耿耿、死心踏地的攻君。\n冷面攻：如同冰山般冷漠的攻君。\n鬼畜攻：指會使用各種方法讓小受感到羞恥難耐的攻君，有時會使用道具。常為總攻。\n渣攻：品行敗壞、對小受很差勁，或有小三，讓人直嘆簡直是個人渣的攻君。\n正太攻：可愛的小男孩攻君。\n溫柔攻：對小受非常溫柔體貼的攻君。\n知識份子攻：智力高的攻君，常有眼鏡、驕傲或冰山屬性。\n暴躁攻：個性暴躁的攻君。\n",
        "受類型": "女王受：像女王一般高高在上的小受，與帝王的差別是相對比較陰性、柔和，走高傲而非霸道路線。\n強受：個性強悍的小受。\n弱氣受：個性柔弱、被動的小受。\n誘受：極具誘惑力，會誘惑攻君的小受。\n大叔受：有點年紀的小受，常搭配年下攻使用。\n襲受：精神上是攻、肉體上是受的類型。有個性且會主動進攻的小受。比起誘受來得強勢。\n天然受：有點少根筋、單純的小受。\n傲嬌受：表面上裝得強硬驕傲，其實內心容易害羞、吃醋，彆扭又可愛的小受。\n健氣受：陽光、活潑開朗的小受。\n忠犬受：像忠犬般忠心耿耿、死心踏地的小受。\n小白受：無辜可愛但又有點無知的小受。\n平凡受：平凡的小受。\n二貨受：有點傻、缺心眼的小受。\n人妻受：賢慧體貼的小受。\n冰山受：如同冰山般冷漠的小受。\n病嬌受：精神病態、對伴侶有極強佔有慾、對愛情有強烈依存症，為了不失去愛人可以不擇手段的小受。通常是因為情感過重而角色黑化。\n貓受：擁有像貓般撒嬌、無法管束、任性等特質的小受\n", 
        "小說類型": "分為原創及同人，故事題材則分為古風/現代/穿越/重生/系統/快穿/穿書/網遊/修仙/星際/未來/末世/獸人/哨兵嚮導/abo/哥兒/人魚/種田",
        "各類型推薦": "古風：三嫁鹹魚\n現代：刺青\n娛樂圈：職業替身\n校園：偽裝學渣\n穿越重生：重生之將軍總把自己當替身\n系統：別在垃圾桶撿男友\n快穿：我真的是渣受\n穿書：反派他過分美麗\n電競：AWM絕地求生\n修仙：天官賜福\n星際：湯家七個O\n無限流：子夜鴞、子夜十\n靈異：死亡萬花筒\n現代靈異：我五行缺你\n魔幻：最後的守衛\n玄幻：判官\nABO：裝A的O怎麼可能再找A\n破鏡重圓：離婚之後\n人魚：人魚陷落\n短篇：我在知乎回答問題被男友發現了\n虐：二哈與他的白貓師尊\n甜寵：妖怪公寓\n",
    }
}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text.strip()

    if user_id not in user_state:
        user_state[user_id] = None

    if msg == '耽美介紹':
        user_state[user_id] = '耽美'
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入想查詢的球員背號"))
    else:
        current_state = user_state[user_id]
        if current_state and msg in questions_answers[current_state]:
            reply = questions_answers[current_state][msg]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(reply))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("未找到相關答案，請重新輸入相對應的關鍵字"))

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
