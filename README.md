GithubSnarfer plugin for Supybot/Limnoria
=========================================

This Supybot/Limnoria plugin allows to display informations about Github issues/pull requests and direct links to them.

How to install
--------------

The informations are fetched from [Github](https://www.github.com/) through it's [Rest API](https://developer.github.com/v3/).


How to configure
----------------

It is based on the Mantis/Bugzilla plugins, so it uses the same command and more or less the same configuration variables:

 * urlbase: The base URL for the Github repository this plugin will retrieve informations from, like https://api.github.com/repos/:owner/:repo

 * bugSnarfer: Determines whether the bug snarfer will be enabled, such that any PR ### or Issue ### seen in the channel will have its information reported into the channel. Channel Specific variable.

 * bugSnarferTimeout: Users often say "PR XXX" several times in a row, in a channel. If "PR XXX" has been said in the last (this many) seconds, don't fetch its data again. If you change the value of this variable, you must reload this plugin for the change to take effect.


How to use
----------

Once the plugin is loaded and (at least) urlbase is set, you can display informations about a Github issue/pull request with the "bug #" command, where # is the issue/pull request number.
If you enable the bugSnarfer variable for a given channel, you won't need using the "bug" command anymore, just write "PR #" or "Issue #", and the bot will automatically display informations about the issue.


Update
------
Get latest version at : https://github.com/veggiematts/supybot-github
