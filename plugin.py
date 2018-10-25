###
# Copyright (c) 2018, Matthias Meusburger
# All rights reserved.
# Based on the Mantis/Bugzilla plugins
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.utils.structures import TimeoutQueue

import simplejson as json
import urllib.request
import urllib.parse
import sys
import random



class GithubSnarfer(callbacks.PluginRegexp):
    """
    Displays informations about a Github Issue or Pull Request
    """
    threaded = True
    unaddressedRegexps = ['snarfBug']


    def __init__(self, irc):

        self.__parent = super(GithubSnarfer, self)
        self.__parent.__init__(irc)

        self.saidBugs = ircutils.IrcDict()
        sayTimeout = self.registryValue('bugSnarferTimeout')
        for k in list(irc.state.channels.keys()):
            self.saidBugs[k] = TimeoutQueue(sayTimeout)
     

    def snarfBug(self, irc, msg, match):
        r"""\b(PR|Issue)\b[\s#]*(?P<id>\d+)"""
        channel = msg.args[0]
        if not self.registryValue('bugSnarfer', channel): return

        id_matches = match.group('id').split()
        ids = []
        self.log.debug('Snarfed ID(s): ' + ' '.join(id_matches))

        # Check if the bug has been already snarfed in the last X seconds
        for id in id_matches:
            should_say = self._shouldSayBug(id, channel)
            if should_say:
                ids.append(id)
        if not ids: return

        strings = self.getBugs(ids)
        for s in strings:
            irc.reply(s, prefixNick=False)


    def _shouldSayBug(self, bug_id, channel):
        if channel not in self.saidBugs:
            sayTimeout = self.registryValue('bugSnarferTimeout')
            self.saidBugs[channel] = TimeoutQueue(sayTimeout)
        if bug_id in self.saidBugs[channel]:
            return False

        self.saidBugs[channel].enqueue(bug_id)
        self.log.info('After checking bug %s queue is %r' \
                        % (bug_id, self.saidBugs[channel]))
        return True



    def getBugs(self, ids):
        strings = [];
        for id in ids:

            # Getting response
            try:
                url = self.registryValue('urlbase') + '/issues/' + str(id);
                f = urllib.request.urlopen(url)
                data = f.read().decode('utf-8')
                result = json.loads(data)
                
                strings.append(str(result['number']) + ': ' + result['title'] + " - " + result['state'])
                strings.append(result['html_url'])

            except Exception as e:
                strings.append("An error occured when trying to query Github: " + str(e))

        return strings


    def bug(self, irc, msg, args, bugNumber):
        """
	<bug number>
        
	Expand bug # to a full URI
        """
        strings = self.getBugs( [ bugNumber ] )

        if strings == []:
            irc.reply( "sorry, bug %s was not found" % bugNumber )
        else:
            for s in strings:
                irc.reply(s, prefixNick=False)

    bug = wrap(bug, ['int'])



Class = GithubSnarfer


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
