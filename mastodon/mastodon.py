from mastodon import Mastodon
from secret import secret
from datetime import datetime, timezone, timedelta
from lxml import html

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
        for n in notifications:
            if n['created_at'] > before_a_minute_time and n['type'] == 'mention':
                output.append(n)
        return output

    def __get_reply(self) -> list:
        notifications = self.mastodon.notifications(limit=5)
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

        output = {
            'status' : status,
            'text' : __extract_content_text(text),
            'account_id' : account_id
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

    def get_oneday_toot(self) -> list:
        before_a_day_time = datetime.now(tz=timezone.utc) - timedelta(days=1)
        stop_bool = False
        oneday_toot_list = []
        next_id = None
        while not stop_bool:
            toot_list = self.mastodon.timeline_local(limit=40, max_id=next_id)
            for toot in toot_list:
                if toot['created_at'] > before_a_day_time:
                    if not toot['account']['bot']:
                        toot_temp = self.__extract_content_text(toot['content'])
                        oneday_toot_list.append(toot_temp)
                else:
                    stop_bool = True
                    break
            next_id = toot_list[39]['id']
        
        return oneday_toot_list

    def check_reply(self):
        mentions = self.__get_reply()
        for m in mentions:
            account_id = m['account_id']
            toot_list = self.__get_oneday_toot_user(account_id)
            self.mastodon.status_reply(m['status'], f'君は今日{str(len(toot_list))}件のトゥートをしたよ！！')