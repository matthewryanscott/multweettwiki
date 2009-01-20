import datetime
import urllib, urllib2

from pyquery import PyQuery as pq

from multweettwiki.logger import log, ERROR, INFO


WEEKDAYS = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun',
}


class TwikiPlugin(object):
    """Twiki plugin."""

    max_message_length = None

    def __init__(self, account):
        self.account = account

    def post_message(self, message):
        options = self.account.options
        # Prepare authentication.
        log(INFO, 'Preparing authentication.')
        self.setup_urllib2_auth()
        # Retrieve edit page.
        edit_uri = options['edituri'] + options['page']
        log(INFO, 'Retrieving edit page %r...', edit_uri)
        pqdoc = pq(url=edit_uri)
        pqform = pqdoc('form[name="main"]')
        form = pqform[0]
        # Update page text.
        text = form.fields['text']
        text = self.update_text(text, message)
        form.fields['text'] = text
        # Post form.
        action = options['baseuri'] + form.action
        log(INFO, 'Posting update to %r...', action)
        data = urllib.urlencode(form.form_values())
        resp = urllib2.urlopen(action, data)
        # Done.
        log(INFO, 'Success!')

    def setup_urllib2_auth(self):
        options = self.account.options
        baseuri = options['baseuri']
        username = options['username']
        password = options['password']
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(
            realm=None,
            uri=baseuri,
            user=username,
            passwd=password,
        )
        auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener_director = urllib2.build_opener(auth_handler)
        urllib2.install_opener(opener_director)

    def update_text(self, text, message):
        today = datetime.date.today()
        weekday = WEEKDAYS[today.weekday()]
        datestamp = '%s %04d-%02d-%02d' % (
            weekday, today.year, today.month, today.day)
        heading_text = self.account.options['heading'] % datestamp
        # Split text into lines.
        lines = text.split('\n')
        heading_lineno = None
        # Look for existing heading for today.
        for (lineno, line) in enumerate(lines):
            if line.startswith('---+'):
                this_heading = line[4:]
                if this_heading == heading_text:
                    heading_lineno = lineno
                    break
        if heading_lineno is None:
            # No heading for today; look for first heading and insert
            # a new one.
            for (lineno, line) in enumerate(lines):
                if line.startswith('---+'):
                    lines.insert(lineno, '---+' + heading_text)
                    heading_lineno = lineno
                    break
        # Prefix message.
        now = datetime.datetime.now()
        prefix = '   * %02d:%02d:%02d ' % (now.hour, now.minute, now.second)
        message = prefix + message
        # Insert message into lines.
        lines.insert(heading_lineno + 1, message)
        # Join with newlines.
        return '\n'.join(lines)