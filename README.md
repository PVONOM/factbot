# !factbot h4h2025

#### What is !factbot?

!factbot is a Discord chat bot that checks for misinformation and hate speech.  
It uses:
- BART (facebook/bart-large-mnli) for zero-shot classification and context-aware understanding.
- Google’s Programmable Search Engine and NewsAPI to fact-check claims against reliable sources.
Unlike traditional chatbots that rely only on keyword scanning, !factbot detects context in messages, making it more accurate at detecting misinformation and toxic content.
When !factbot comes across hate speech or profanity it reports it to the moderator.


#### Why Discord!

Discord is a popular communication platform and used by millions to communicate. 
Without a platform-wide moderation system, Discord has the potential to harbor echo chambers of hate and cyberbullying in its communities. 
Unlike traditional Discord chatbots that simply parse through messages looking for keywords, !factbot uses an LLM determine context and is accurate. 

#### Theory of Change!

Our theory is that online hate is fueled by ignorance and misinformation and working to fix these underlying issues will be be the most effective strategy. 
While we focus on this we dont want hate speech to be overlooked so our bot also reports it to keep a friendlier environment. 

#### Community Inclusion

Our users are currently discord members that factbot would help keep informed and away from hate speech. 
With more time we would allow user input to control where else this bot is implemented. 
This could be mandated for school run chats to ensure that hate speech is reported to professors or other forms of authority. 

#### The Future of !factbot

In the future we would like to extend the reach of !factbot to other platforms such as Twitter, Reddit, Facebook and more. 
We would also improve the ability of the bot to recognize misinformation and hate speech more consistently. 
Training the bot on images as well could help keep all visual content appropriate. 

https://github.com/PVONOM/factbot


To run: 
    bash setup.sh
    source venv/bin/activate
    python main.py

Click this link to add !factbot to a discord server
    https://discord.com/oauth2/authorize?client_id=1459699685978673183&permissions=75776&integration_type=0&scope=bot+applications.commands

