import requests
from plugin import *


class man(plugin):
    def __init__(self, bot):
        super().__init__(bot)
        self.man_url = r'http://man.he.net/?topic=%s&section=all'

    @command
    @doc('man <command>: get unix manual entry for <command> from man.he.net')
    def man(self, sender_nick, args, **kwargs):
        if not args: return
        ask = args[0].strip()
        url = self.man_url % ask
        self.logger.info(f'{sender_nick} asked for man of {ask}')

        content = requests.get(url, timeout=5).content
        start = content.find(b'DESCRIPTION\n')
        end = content.find(b'\n\n', start)
        if start == -1 or end == -1:
            self.bot.say_err(ask)
            return

        result = content[start + 19:end].replace(b'       ', b'').replace(b'-\n', b'').replace(b'\n', b' ').replace(b'  ', b' ').decode('utf-8').strip()

        if self.bot.is_msg_too_long(result):
            self.bot.say(result, sender_nick)
        else:
            self.bot.say(color.orange(f'[{ask}] ') + result)

        self.bot.say(color.orange(f'[{ask}] ') + url)
