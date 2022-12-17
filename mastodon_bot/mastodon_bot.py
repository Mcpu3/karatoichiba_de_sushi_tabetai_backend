from mastodon import Mastodon
from mastodon_bot.secret import secret
from datetime import datetime, timezone, timedelta
from lxml import html
from pn_predictor.predict_pns import predict

class MastodonReply:
    def __init__(self) -> None:
        self.mastodon = self.__login()
    
    def __login(self) -> Mastodon:
        mastodon = Mastodon(
            api_base_url = secret.instance,
            access_token = secret.token
        )

        return mastodon

    @staticmethod
    def __remove_timeout_notification(notifications: list) -> list:
        before_a_minute_time = (datetime.now(tz=timezone.utc) - timedelta(minutes=1)).replace(second=0, microsecond=0)
        output = []
        # print(notifications[0])
        for n in notifications:
            if n['created_at'] > before_a_minute_time and n['type'] == 'mention' and not n['account']['username'] == 'karatoichiba_sushi':
                output.append(n)
        return output

    def __get_reply(self) -> list:
        notifications = self.mastodon.notifications()
        notifications = self.__remove_timeout_notification(notifications)

        output = [self.__extract_notification_information(n) for n in notifications]

        return output
    
    @staticmethod
    def __extract_notification_information(notification) -> list:
        def __extract_content_text(content: str) -> str:
            if content == '':
                return ''
            t = html.fromstring(content)
            text = t.text_content().strip()
            text = text.replace('@karatoichiba_sushi', '')

            return text

        status = notification['status']
        text = status['content']
        account_id = status['account']['id']
        account_name = status['account']['display_name'] if status['account']['display_name'] != '' else status['account']['username']

        output = {
            'status' : status,
            'text' : __extract_content_text(text),
            'account_id' : account_id,
            'account_name' : account_name
        }

        return output

    @staticmethod
    def __extract_content_text(content: str) -> str:
            if content == '':
                return ''
            t = html.fromstring(content)
            text = t.text_content().strip()

            return text

    def __get_oneday_toot_user(self, account_id: str = None) -> list:
        before_a_day_time = datetime.now(tz=timezone.utc) - timedelta(days=1)
        stop_bool = False
        oneday_toot_list = []
        next_id = None
        while not stop_bool:
            toot_list = self.mastodon.timeline_local(limit=40, max_id=next_id)
            for toot in toot_list:
                if toot['created_at'] > before_a_day_time:
                    if toot['account']['id'] == account_id:
                        toot_temp = self.__extract_content_text(toot['content'])
                        oneday_toot_list.append(toot_temp)
                else:
                    stop_bool = True
                    break
            next_id = toot_list[39]['id']
        
        return oneday_toot_list

    def __get_any_day_toot(self, day: int) -> list:
        before_any_day_time = datetime.now(tz=timezone.utc) - timedelta(days=day)
        stop_bool = False
        oneday_toot_list = []
        next_id = None
        while not stop_bool:
            toot_list = self.mastodon.timeline_local(limit=40, max_id=next_id)
            for toot in toot_list:
                if toot['created_at'] > before_any_day_time:
                    if not toot['account']['bot']:
                        toot_temp = self.__extract_content_text(toot['content'])
                        oneday_toot_list.append(toot_temp)
                else:
                    stop_bool = True
                    break
            next_id = toot_list[39]['id']
        
        return oneday_toot_list
    
    def __predict_reply_message(self, reply_to_status, message: str):
        toot_list = self.__get_any_day_toot(7)
        predict_sentence_list = []
        sentence = message.replace(' ', '').replace('　', '').replace('\n', '')
        # print(sentence)
        for t in toot_list:
            # print(t)
            if sentence in t:
                print(t)
                predict_sentence_list.append(t)

        if predict_sentence_list != []:
            f= predict(predict_sentence_list, './pn_predictor/misc/count_vectorizer.pickle', './pn_predictor/misc/model.pickle')
            print(f)

            if f.count(1) >= f.count(-1):
                sentence += "のことはみんな大好きみたいだよ！"
            else :
                sentence += "のことはあんまり良く思われてないみたい……"
        else:
            sentence += "について話してる人はいなかったみたい……"

        self.mastodon.status_reply(reply_to_status, sentence)
        
    def __predict_reply_user(self, reply_to_status, account_id: str, account_name: str):
        toot_list = self.__get_oneday_toot_user(account_id)
        sentence = account_name
        if toot_list != []:
            f = predict(toot_list, './pn_predictor/misc/count_vectorizer.pickle', './pn_predictor/misc/model.pickle')
            print(f)

            if f.count(1) >= f.count(-1):
                sentence += "は今日一日はっぴーいぇいいぇい"
            else :
                sentence += "はネガティブがー－ん"
        else:
            sentence += "今日はトゥートしてないね！"

        self.mastodon.status_reply(reply_to_status, sentence)

    def check_reply(self):
        mentions = self.__get_reply()
        for m in mentions:
            if '調子を教えて' in m['text']:
                self.__predict_reply_user(m['status'], m['account_id'], m['account_name'])
            else:
                self.__predict_reply_message(m['status'], m['text'])