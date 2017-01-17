This is a Slack integration that posts in a channel when people join a TeamSpeak server.

# Requirements

* Python 3.4
* [basedir](https://github.com/fenhl/python-xdg-basedir)
* [slacker](https://pypi.python.org/pypi/slacker)
* [ts3](https://github.com/nikdoof/python-ts3) (GitHub master, not the version on PyPI)

# Configuration

* Obtain a username and password for the ServerQuery API of the Teamspeak server.
* [Create a bot user](https://my.slack.com/apps/A0F7YS25R-bots) on your Slack team and invite it to the channel.
* Create a [JSON](http://json.org/) file named `slack-teamspeak.json` in `$XDG_CONFIG_DIRS` (e.g. `~/.config/slack-teamspeak.json` or `/etc/xdg/slack-teamspeak.json`) with the following key pairs:
    * `"apiToken"`: the bot user's Slack API token (required)
    * `"channel"`: the name of the Slack channel where the bot will post, including the `#` prefix (optional, defaults to `"#teamspeak"`)
    * `"checkInterval"`: the integration will re-check the client list periodically after this many seconds (optional, defaults to `5`)
    * `"hostname"`: the TeamSpeak server's hostname or IP address (required)
    * `"message"`: the message template, including `{}` as a placeholder where the nicknames who joined are inserted (optional, defaults to `"{} joined"`)
    * `"password"`: the ServerQuery password (required)
    * `"port"`: the TeamSpeak server's ServerQuery port (optional, defaults to `10011`)
    * `"username"`: the ServerQuery username (optional, defaults to `"serveradmin"`)
* Run the integration and keep it running.
