from mastodon import Mastodon
from datetime import datetime, timezone, timedelta
from lxml import html
from pn_predictor.predict_pns import predict_pns
import os, dotenv, random

class MastodonReply:
    def __init__(self) -> None:
        self.mastodon = self.__login()
    
    def __login(self) -> Mastodon:
        dotenv.load_dotenv()
        instance = os.environ['MT_INSTANCE']
        token = os.environ['MT_TOKEN']

        mastodon = Mastodon(
            api_base_url = instance,
            access_token = token
        )

        return mastodon

    @staticmethod
    def __remove_timeout_notification(notifications: list) -> list:
        before_a_minute_time = (datetime.now(tz=timezone.utc) - timedelta(minutes=1)).replace(second=0, microsecond=0)
        output = []
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
    
    def __predict_reply_message(self, reply_to_status, message: str, limit: int = 20):
        toot_list = self.__get_any_day_toot(7)
        predict_sentence_list = []
        sentence = message.replace(' ', '').replace('　', '').replace('\n', '')
        for t in toot_list:
            if sentence in t:
                if len(predict_sentence_list) >= limit:
                    break
                predict_sentence_list.append(t)

        print(predict_sentence_list)
        if predict_sentence_list != []:
            f= predict_pns(predict_sentence_list, './pn_predictor/misc/count_vectorizer.pickle', './pn_predictor/misc/model.pickle')
            print(f'mastodon_bot : (word){sentence} {str(f)}')

            positive_rate = f.count(1) / len(f)
            if positive_rate > 0.85:
                sentence += 'のことはみんな大好きみたいだよ！'
            elif positive_rate > 0.50:
                sentence += 'のことは結構よく思われてるみたい！'
            else:
                sentence += 'のことはあんまり良く思われてないみたい……'
        else:
            sentence += 'について話してる人はいなかったみたい……'

        self.mastodon.status_reply(reply_to_status, sentence)
        
    def __predict_reply_user(self, reply_to_status, account_id: str, account_name: str, limit: int = 20):
        toot_list = self.__get_oneday_toot_user(account_id)
        toot_list[:limit]
        sentence = account_name
        print(toot_list)
        if toot_list != []:
            f = predict_pns(toot_list, './pn_predictor/misc/count_vectorizer.pickle', './pn_predictor/misc/model.pickle')
            print(f'mastodon_bot : (user){account_name} {str(f)}')

            positive_sentences = ['は今日一日楽しそうだったね！いぇいいぇい！', 'は今日一日楽しそうだったね！明日もいい日になあれ！', 'は今日を満喫できたね！']
            negative_sentences = ['はネガティブがーーん', 'はなんだか元気がないね……。がが～ん', 'はなんだか元気がないね……。明日がいい日になりますように！']
            non_toot_sentences = ['は今日忙しかったのかな？しっかり休もう！', 'はリアルが充実してるんだね！']
            if f.count(1) >= f.count(-1):
                sentence += positive_sentences[random.randrange(len(positive_sentences))]
            else :
                sentence += negative_sentences[random.randrange(len(negative_sentences))]
        else:
            sentence += non_toot_sentences[random.randrange(len(non_toot_sentences))]

        self.mastodon.status_reply(reply_to_status, sentence)

    def check_reply(self):
        mentions = self.__get_reply()
        for m in mentions:
            if '調子を教えて' in m['text']:
                self.__predict_reply_user(m['status'], m['account_id'], m['account_name'])
            else:
                self.__predict_reply_message(m['status'], m['text'])