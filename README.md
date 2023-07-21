# steam-account-check
Intended to login and check the chats and friend requests of a large set of steam accounts and output information to console and chats to a discord webhook

# Usage
Edit config.example.json with details (steam api key and discord webhook, accounts seperated by commas \[json format\]) and rename to config.json then run main.py with ```python main.py```

# Known Issues
This uses the python steam library from here[https://github.com/ValvePython/steam]

Unfortunately, the library is in the process of implementing Steam's changes to saving authentication to the servers, so if you need to check accounts with two-factor authentication you need to authenticate everytime.

# To-dos/Roadmap
- Add a setting to allow for autoaccepting all friend requests (for some reason, the add function was not working)
- Greater error checking and diagnostics for exception handling
- Optionally use an alternative method of checking account names/avatar details
- Allow all features to be optional (checking chats, using discord webhook, etc)
- Easy-to-use account adding option (as opposed to editing config json)
- Easy-to-use setup for config options
- Implement checks for necessary config options
- Automation (seperate commands for manual check and routine checks)
- Beautify (proper PEP, seperate objects/functions/seperate files)
- Find and identify rate limits to implement speed limitations to avoid hitting
- Implement 2FA when possible
- Check further chats/messages on request (Steam only sends a couple but tells us that there is more, honestly shouldn't be an issue unless you get a lot of messages)