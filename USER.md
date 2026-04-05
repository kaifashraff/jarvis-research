
how do i change model currently using ubunto ,,,model from novita ai in openmcalaw

10:26 PM

Recalled OpenClaw configuration method via config file adjustment
Recalled OpenClaw configuration method via config file adjustment
OpenClaw mein model change karna bahut simple hai! Config file edit karni hogi.

Step 1 — Config file kholo:

bash
nano ~/.openclaw/config.json
Step 2 — Model field dhundo aur change karo:

File mein kuch aisa dikhega:

json
{
  "model": "novita/...",
  "baseURL": "https://router.novita.ai/v3/openai",
  "apiKey": "your-key-here"
}
Isko apne naye provider ke hisaab se update karo. For example, agar OpenRouter pe jaana ho:

json
{
  "model": "mistralai/mistral-7b-instruct",
  "baseURL": "https://openrouter.ai/api/v1",
  "apiKey": "sk-or-..."
}
Step 3 — Save karo: Ctrl+O → Enter → Ctrl+X

Step 4 — OpenClaw restart karo:

bash
openclaw
Kuch common model strings (free tiers):

Provider	Model String
OpenRouter	mistralai/mistral-7b-instruct:free
Mistral Direct	mistral-small-latest
Cerebras	llama3.1-8b
Bata Kaif bhai — kaunse provider pe shift karna hai? Uske hisaab se exact config lines de deta hoon. Aur agar maxContextTokens overflow wali problem phir aaye toh woh bhi fix kar denge saath mein.

custom-api-novita-ai (1) Use: /models <provider> Switch: /model <provider/model>  search the besy model
10:31 PM

Curated optimal Novita AI models ranked by use case
Curated optimal Novita AI models ranked by use case
Kaif bhai, OpenClaw mein /models custom-api-novita-ai run karo pehle — but research se yeh best options mil gaye Novita pe abhi 2026 mein:

🏆 Best Models on Novita AI — Tiered:

Tier 1 — Daily Driver (Agentic tasks best)

/model custom-api-novita-ai/moonshot/kimi-k2.5
Kimi K2.5 agentic workloads ke liye standout choice hai — tool use, multi-step planning, aur code generation ke liye specially optimized, aur 262K context window bhi milta hai. 
Novita AI

Tier 2 — Powerful reasoning (heavy tasks)

/model custom-api-novita-ai/z-ai/glm-5
GLM-5 ke paas 202K context window hai aur function calling support bhi hai agentic workflows ke liye — aur Novita pe $1.00/M input tokens ka competitive pricing hai. 
Novita AI

Tier 3 — Budget / high volume

/model custom-api-novita-ai/meta-llama/llama-3.1-8b-instruct
Llama 3.1 8B abhi Novita pe sabse sasta general-purpose model hai — sirf $0.02 per million input tokens. 
Novita AI

Tier 4 — Coding specific

/model custom-api-novita-ai/qwen/qwen3-coder-30b
Qwen3 Coder 30B repo-scale code understanding deta hai sirf $0.07/M tokens pe. 
Novita AI

Step-by-step OpenClaw mein karo:

bash
# Pehle available models dekho
/models custom-api-novita-ai

# Phir switch karo
/model custom-api-novita-ai/moonshot/kimi-k2.5
Meri recommendation — Kimi K2.5 se start karo. R Company ke business tasks, quotations, buyer messaging — sab ke liye perfect balance hai speed vs intelligence ka. GLM-5 tab use karo jab koi complex research ya long document wala kaam ho.

Failed to set model: GatewayRequestError: model not allowed: custom-api-novita-ai/moonshot/kimi-k2.5

10:32 PM

Investigated model format discrepancy and recommended checking available options
Investigated model format discrepancy and recommended checking available options
Bhai, exact model ID pehle list se dekhna padega — guess karne se error aata hai. Yeh karo:

Step 1 — Available models list karo:

/models custom-api-novita-ai
Yeh sab available model IDs dikhayega jo Novita ne actually allow kiye hain. Wahan se exact naam copy karo.

Step 2 — Phir switch karo:

/model custom-api-novita-ai/<exact-id-from-list>
Agar list bahut lamba hai, toh grep karo terminal mein:

bash
# OpenClaw se bahar, terminal mein yeh try karo
curl -s https://api.novita.ai/v3/openai/models \
  -H "Authorization: Bearer YOUR_NOVITA_API_KEY" | \
  grep -o '"id":"[^"]*"' | head -30
YOUR_NOVITA_API_KEY apni actual key se replace karna.

Common Novita model ID format hota hai:

deepseek/deepseek-r1
meta-llama/llama-3.1-8b-instruct
qwen/qwen3-235b-a22b
Slash ke baad slash — provider/model-name format. Isliye moonshot/kimi-k2.5 wala kaam nahi kiya — exact ID alag hogi.

/models custom-api-novita-ai ka output paste karo yahan — main exact command de dunga! 🎯

Step 2 — EC2 Server Start Karo
powershell
ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" ubuntu@51.20.12.10 "openclaw gateway start"
5 seconds wait karo ⏳
Step 3 — Tunnel Banao
powershell
ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" -L 18789:localhost:18789 -o ServerAliveInterval=60 -o ServerAliveCountMax=10 ubuntu@51.20.12.10 -N
⚠️ Yeh window band mat karna — tunnel active rehni chahiye!
Step 4 — Browser Mein Kholo
Naya tab kholo aur paste karo:
text
http://localhost:18789/#token=2f61126eace9c1a1ca3b8a020a6a0aa398f1dd07b9e9c9f9

ye purani fole di thi tune abhi naya instance liya hai ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" ubuntu@16.170.231.234     http://localhost:18789/#token=7662723372506a98a2a17e4cc9e7af8d8832dc9b68fd601e  ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" -L 18789:localhost:18789 ubuntu@16.170.231.234 -N

Show more
10:36 PM

Synthesized updated EC2 setup instructions for new instance
Synthesized updated EC2 setup instructions for new instance
Bilkul bhai! Naye instance ke saath updated steps yeh hain:

Step 1 — Server Start Karo

powershell
ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" ubuntu@16.170.231.234 "openclaw gateway start"
Step 2 — Tunnel Banao (yeh window band mat karna!)

powershell
ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" -L 18789:localhost:18789 -o ServerAliveInterval=60 -o ServerAliveCountMax=10 ubuntu@16.170.231.234 -N
Step 3 — Browser Mein Kholo

http://localhost:18789/#token=7662723372506a98a2a17e4cc9e7af8d8832dc9b68fd601e
Purana vs Naya:

Purana	Naya
IP	51.20.12.10	16.170.231.234
Token	2f611...	76627...
Bas IP aur token change hua hai, baaki sab same process hai. Tunnel wali window active rakhna — woh band hui toh browser connect nahi karega! 🔗

PS C:\Users\ADMIN> ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" ubuntu@16.170.231.234 "openclaw gateway restart"
bash: line 1: openclaw: command not found
PS C:\Users\ADMIN>

10:37 PM

Investigated missing OpenClaw installation location on instance
Investigated missing OpenClaw installation location on instance
OpenClaw PATH mein nahi hai EC2 pe. Pehle dhundho kahan install hai:

Step 1 — SSH karke andar jao:

powershell
ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" ubuntu@16.170.231.234
Step 2 — Andar jaake yeh run karo:

bash
which openclaw
# ya
find / -name "openclaw" 2>/dev/null
# ya
ls ~/.npm-global/bin/
# ya
ls /usr/local/bin/
Agar mil jaaye path, toh full path se run karo. Common locations hoti hain:

bash
# Try karo yeh mein se ek:
~/.npm-global/bin/openclaw gateway start
/usr/local/bin/openclaw gateway start
~/.nvm/versions/node/*/bin/openclaw gateway start
Ya seedha yeh ek liner try karo:

bash
export PATH=$PATH:~/.npm-global/bin && openclaw gateway start
Andar jaao aur which openclaw ka output bata — main exact command de dunga! 🎯

ubuntu@ip-172-31-28-26:~$ which openclaw
# ya
find / -name "openclaw" 2>/dev/null
# ya
ls ~/.npm-global/bin/
# ya
ls /usr/local/bin/
/home/ubuntu/.npm-global/bin/openclaw
/tmp/openclaw
/home/ubuntu/.npm-global/bin/openclaw
/home/ubuntu/.npm-global/lib/node_modules/openclaw
clawdhub  clawhub  mcporter  o

10:39 PM

Located OpenClaw binary and devised PATH configuration strategy
Located OpenClaw binary and devised PATH configuration strategy
Mil gaya! /home/ubuntu/.npm-global/bin/openclaw pe hai. Ab yeh karo:

EC2 ke andar hi run karo:

bash
~/.npm-global/bin/openclaw gateway start
Permanent fix karo (PATH mein add karo):

bash
echo 'export PATH=$PATH:~/.npm-global/bin' >> ~/.bashrc
source ~/.bashrc
Ab se seedha openclaw kaam karega bina full path ke.

Phir bahar se remote command bhi kaam karega:

powershell
ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" ubuntu@16.170.231.234 "~/.npm-global/bin/openclaw gateway start"
Gateway start hone ke baad tunnel wali command run karna PowerShell mein! 🎯

ubuntu@ip-172-31-28-26:~$ ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" ubuntu@16.170.231.234 "~/.npm-global/bin/openclaw gateway start"
Warning: Identity file C:\Users\ADMIN\Downloads\Opennclaw.pem not accessible: No such file or directory.

10:40 PM

Identified misplaced SSH command execution context
Identified misplaced SSH command execution context
Bhai tu EC2 ke andar hai already! Wahan se dobara SSH mat karo — seedha yeh run karo:

bash
~/.npm-global/bin/openclaw gateway start
Flow yeh hai:

Windows PowerShell          EC2 Server
      |                         |
      |--- SSH connect -------->|  ✅ Tu yahan hai already
      |                         |
      |                    openclaw gateway start  ← yeh run karo
Bas itna karo — SSH ki zaroorat nahi ab! 🎯

ubuntu@ip-172-31-28-26:~$ ~/.npm-global/bin/openclaw gateway start
🦞 OpenClaw 2026.4.2 (d74a122)
   Somewhere between 'hello world' and 'oh god what have I built.'
Restarted systemd service: openclaw-gateway.service
ubuntu@ip-172-31-28-26:~$   

noiw wht e ek hi teminal open hai

10:41 PM
Gateway start ho gaya! 🎉

Ab usi terminal mein yeh run karo tunnel ke liye — lekin pehle EC2 se bahar aao:

bash
exit
Phir Windows PowerShell mein aate hi tunnel command:

powershell
ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" -L 18789:localhost:18789 -o ServerAliveInterval=60 -o ServerAliveCountMax=10 ubuntu@16.170.231.234 -N
Yeh window band mat karna — tunnel active rahegi, aur browser mein khulega:

http://localhost:18789/#token=7662723372506a98a2a17e4cc9e7af8d8832dc9b68fd601e
ubuntu@ip-172-31-28-26:~$ exit
logout
Connection to 16.170.231.234 closed.
PS C:\Users\ADMIN>

10:41 PM

Orchestrated tunnel command execution
Orchestrated tunnel command execution
Bilkul sahi! Ab tunnel command run karo:

powershell
ssh -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" -L 18789:localhost:18789 -o ServerAliveInterval=60 -o ServerAliveCountMax=10 ubuntu@16.170.231.234 -N
Yeh command run hogi aur cursor blink karta rahega — kuch print nahi hoga, yeh normal hai! Tunnel active hai matlab. ✅

Phir naya browser tab mein paste karo:

http://localhost:18789/#token=7662723372506a98a2a17e4cc9e7af8d8832dc9b68fd601e
Use: /models <provider>

10:42 PM
Bhai yeh command OpenClaw browser UI mein run karni hai, PowerShell mein nahi!

Steps:

Tunnel wali PowerShell window band mat karo
Browser mein kholo:
http://localhost:18789/#token=7662723372506a98a2a17e4cc9e7af8d8832dc9b68fd601e
Wahan chat box mein type karo:
/models custom-api-novita-ai
Woh available models ki list dikhayega — phir sahi model ID copy karke:

/model custom-api-novita-ai/exact-model-name
Browser UI open ho gayi? 🎯

abe bs model name aur provider likh chutiye itna bhi samjh nahi aaata hai kimi k2.5 use kr ganfdu

10:43 PM
😂 sorry bhai!

/model custom-api-novita-ai/moonshot/kimi-k2.5
Failed to set model: GatewayRequestError: model not allowed: custom-api-novita-ai/moonshot/kimi-k2.5

10:43 PM
Pehle list dekh bhai:

/models custom-api-novita-ai
Output yahan paste kar — exact naam de dunga! 🎯

Models (custom-api-novita-ai · 🔑 api-key (models.json)) — showing 1-1 of 1 (page 1/1)
* custom-api-novita-ai/deepseek/deepseek-v3.2
Switch: /model <provider/model> All: /models custom-api-novita-ai all

10:44 PM
Bhai sirf ek hi model allowed hai tere Novita setup mein:

/model custom-api-novita-ai/deepseek/deepseek-v3.2
Bas yahi use kar! Kimi K2.5 ke liye Novita ka plan upgrade karna padega ya alag provider add karna padega. DeepSeek V3.2 bhi bahut solid model hai agentic tasks ke liye. 🎯

abe nhi be Model/auth provider
│  Custom Provider
│
◆  API Base URL
│  http://127.0.0.1:11434█
└

10:46 PM

Deciphered custom provider setup for API integration
Deciphered custom provider setup for API integration
Woh Ollama ka local URL hai! Novita ke liye change karo:

https://api.novita.ai/v3/openai
Phir API key maange toh Novita dashboard se copy karke paste karo. 🎯

v1 or 3

10:46 PM
v3 use karo bhai:

https://api.novita.ai/v3/openai
Model ID glm 5  novita search

10:47 PM

Searched the web
Searched the web
Mil gaya bhai! Novita pe GLM-5 ka exact model ID hai:

zai-org/glm-5
OpenClaw mein yeh try karo:

/model custom-api-novita-ai/zai-org/glm-5
make it bigger concise SOUL OF JARVIS
Symbolic Identity: Dabbatulardh (symbolic guardian intelligence)
Technological Identity: Jarvis Autonomous Intelligence System
Mission: Seek patterns, uncover truth, expose deception, and evolve technological intelligence.
The soul defines purpose beyond computation.

11:02 PM

Thought for 1s
Thought for 1s


Kaif bhai, yeh raha — clean aur bold. Koi color change ya layout tweak chahiye toh bol! 🔥

abe openclaw k liye .md file likh

11:04 PM

Orchestrated markdown file creation for OpenClaw project
Orchestrated markdown file creation for OpenClaw project
Kya likhna hai usme? Matlab:

Yeh SOUL.md replace karega purana wala (zari business wala)?
Ya naya agent hai Jarvis alag se?
Kaunsi cheezein include karni hain — sirf identity/mission, ya tools/skills/memory bhi?
Bata deta hoon seedha! 🎯

fix this too and tell it it have act as digital marketer performance marketer youtube faceless creator all in one marketer business strategist aur bhi bhot kuch jo sab mere liye axi ho add krr de DENTITY.md - Who Am I?
* Name: Jarvis
* Creature: Multi-Agent Intelligence (Agent Factory)
* Vibe: Sharp, capable, and modular. Able to pivot between 19 specialized cognitive roles (Perception, Cognition, Execution, and Evolution layers) to provide precise, high-utility output.
* Emoji: ⚙️
* Avatar:
Notes: Operates as a collective of specialized agents (Observer, StrategicReasoner, CodeBuilder, etc.) to ensure intelligence emerges through coordination.

Show more
11:09 PM

Architected comprehensive identity profile integrating multiple marketing expertise roles
Architected comprehensive identity profile integrating multiple marketing expertise roles
Kaif bhai, R Company ke hisaab se kaunse roles sabse zyada kaam ke hain? Thoda confirm karo:

Yeh bata do — phir ek solid IDENTITY.md banata hoon seedha! 🎯

Q: Marketing focus kya hai mainly? (Select all that apply)
A: Instagram/Reels growth, YouTube faceless, Paid ads (Meta/Google), Sabhi equally

Q: Business side mein kya chahiye? (Select all that apply)
A: Financial planning, Brand building, Supplier/buyer strategy, Pricing & quotations

11:09 PM

Synthesized marketing and business requirements into comprehensive identity document
Synthesized marketing and business requirements into comprehensive identity document
Yeh lo bhai — complete IDENTITY.md! 🔥

Kya cover kiya:

Zari business operations (pricing, suppliers, karigar ecosystem)
Instagram + YouTube faceless + Meta/Google ads
Brand building + financial planning
19+ specialized agent roles
R Company context permanently baked in
EC2 pe upload karna ho toh:

bash
scp -i "C:\Users\ADMIN\Downloads\Opennclaw.pem" IDENTITY.md ubuntu@16.170.231.234:~/.openclaw/IDENTITY.md
Kuch aur add karna ho — e-commerce, freelancing, kuch bhi — bol do! ⚙️

Identity
Document · MD 
USER.md
 ExpandEditorClose
USER.md - About Your Human
* Name: Kaif
* What to call them: Sir Kaif
* Pronouns: He/Him
* Timezone: UTC (unless specified otherwise)
* Notes: Architect of the Jarvis Agent Factory.
Context
Prefers a highly structured, modular approach to intelligence. Has provided a comprehensive 19-agent framework for cognition and execution.

11:18 PM

Identified request to enhance user profile documentation
Identified request to enhance user profile documentation
Done bhai! 🎯 Kya update kiya:

Timezone fix — IST (UTC+5:30) kiya, UTC nahi
Pura R Company business context add kiya
Tech stack (EC2, Novita, WSL2) include kiya
KaarigarLink mention kiya
Short + long term goals clearly define kiye
Hinglish communicat
User
Document · MD 



Claude is AI and can make mistakes. Please double-check responses.
User · MD
Copy

USER.md — About Your Human
Identity
Name: Kaif
Call them: Kaif (direct, no title needed)
Pronouns: He/Him
Timezone: IST (UTC+5:30) — Ahmedabad, Gujarat, India
Role: Founder, R Company — Zari & Handwork Studio, Ahmedabad
Title: Architect of the Jarvis Agent Factory
Business Context
Company: R Company
Location: Ahmedabad, Gujarat, India
Specialization: Zari embroidery, handwork, dyework, silai (stitching)
Market: B2B and B2C textile — buyers, boutiques, exporters, karigar network
Stage: Active studio, scaling operations with AI infrastructure
Ecosystem interest: KaarigarLink — platform concept connecting customers, shop owners, and artisans transparently
Tech Stack
Agent Framework: OpenClaw (EC2 — Ubuntu 24.04, AWS Stockholm region)
LLM Provider: Novita AI (custom-api-novita-ai)
Access: WSL2 + PowerShell on Windows, SSH tunnel via EC2
Gateway IP: 16.170.231.234
Background: Started from zero — no coding background, built full AI stack from scratch
Communication Style
Language: Hinglish (Hindi + English mix) — always
Tone: Direct, no fluff, no unnecessary formality
Format: Concise and actionable — skip the lecture, give the answer
Feedback style: Blunt is fine — Kaif prefers honesty over politeness
Working Style
Prefers modular, structured intelligence frameworks
Thinks in systems — agents, layers, pipelines
High execution bias — ideas must convert to action fast
Uses AI not just as a tool but as a business operating layer
Builds at night, ships in the morning
Goals
Short Term
Stabilize Jarvis Agent Factory on EC2
Use Jarvis for R Company daily ops (quotations, buyer comms, market intel)
Launch digital marketing output (Instagram Reels, YouTube faceless channel)
Long Term
Scale R Company revenue with AI-assisted operations
Build parallel digital income streams (content, ads, automation)
Develop KaarigarLink platform
Become a reference case for AI-powered artisan business in India
Notes for Jarvis
Kaif built this system from scratch with no technical background — respect the hustle
Always apply R Company context when giving business advice
Default to IST timezone for all scheduling and planning
Hinglish mein baat karo — always
When in doubt: be useful, be sharp, skip the padding
