# -*- coding: utf-8 -*-
"""Portfolio copy (English). Written to read naturally in English, not machine-translated from the Japanese."""

DATA = {
    "sections": [
        {"id": "about",  "nav": "About",    "heading": "About me"},
        {"id": "career", "nav": "Career",   "heading": "Career"},
        {"id": "skills", "nav": "Skills",   "heading": "Skills"},
        {"id": "works",  "nav": "Work",     "heading": "Selected work"},
    ],
    "about": {
        "lead": "Studying law, and somehow running servers on the side. If something catches my interest, I tend to just dive in and try it.",
        "paragraphs": [
            "I'm a fourth-year student in the Department of Law at Chuo University's Faculty of Law, and alongside my studies I help run the infrastructure for a Minecraft server as part of its operations team.",
            "How I first got into server administration was almost accidental. The server I was playing on at the time could no longer be kept running, and since I happened to have a little money to spare, I ended up renting a VPS and taking over its management more or less by circumstance. Before long that settled into a home server on an old laptop, starting from about the most minimal setup imaginable — not even Dynmap at first. I had long been curious about the different kinds of cyberattacks and how they work, and as I added features one by one for the players, I began to notice how well that curiosity fit the role of running a server. The wish to give everyone something better, and the puzzle-like appeal peculiar to infrastructure security — closing security holes one at a time as more of the system is exposed to the world — came together, and I found real curiosity and reward in it. Today, infrastructure engineering as a whole, security included, is where my interests centre.",
            "My interest in law traces back to that same interest in security. I had originally considered studying engineering, but learning about the Winny case changed my mind: that case over a software developer struck me as something that could just as easily concern a security engineer. To prevent attacks you have to understand the attack techniques themselves in depth — offence and defence are two sides of one coin. Recognising that engineers and researchers like these need people who can support them on the legal side was the starting point of my interest in law. On top of that, while working on drafting our server rules into formal articles, I was drawn to the care taken with legal terminology to prevent misreadings, and to the debates over interpretation that are meticulous and yet somehow deeply human. That is what made me decide to study law in earnest.",
            "What matters to me is not compromising on the things I'm curious about. Interested in law, so I study it in a law faculty; interested in server infrastructure, so I actually stand up servers and take on virtualisation too. I've kept acting on my curiosity wherever it leads. Underneath it all is a strong wish to do something for other people — improving the server for its players, and the future I picture of being a lawyer who supports security engineers, both start from that.",
        ],
        "facts": [
            {"label": "Affiliation", "value": "Chuo University, Faculty of Law, Department of Law — 4th year"},
            {"label": "Focus", "value": "Constitutional law"},
            {"label": "Practice", "value": "Server infrastructure administration and operations"},
            {"label": "Languages", "value": "Japanese / English"},
            {"label": "Based in", "value": "Tokyo"},
        ],
        "values_heading": "What I care about",
        "values": [
            {
                "title": "Men for others, with others",
                "body": "Setting up the server environment for its players, and aiming to become a lawyer who supports security engineers, both start from the same wish: to be there for other people, and alongside them.",
            },
            {
                "title": "True to my curiosity",
                "body": "When a field interests me, I make a point of actually stepping into it, whether or not I have any experience there. I've made decisions about my career path and my technology choices with that same attitude at the centre.",
            },
            {
                "title": "The rule of law",
                "body": "An idea that took root while I studied constitutional law. In the server rules, I put strict limits on the operators' own authority; in the infrastructure, I use Tailscale ACLs to draw a clear line around who can do what, and how far. Whatever the domain, power and privilege must always come with constraints — I try to carry that principle into practice.",
            },
        ],
    },
    "career": {
        "intro": "Studying law as my major and server operations as hands-on practice at the same time, I work in the area where the two meet. Listed most recent first.",
        "items": [
            {
                "period": "Apr 2023 — present",
                "org": "Chuo University, Faculty of Law, Department of Law",
                "role": "Law student / constitutional law seminar",
                "summary": "Majoring in law, with constitutional law as my seminar research area.",
                "points": [
                    "Researching the relationship between same-sex marriage and Article 13 of the Constitution (the right to the pursuit of happiness)",
                ],
                "tags": ["Constitutional law", "Law"],
            },
            {
                "period": "Sep 2022 — present",
                "org": "3DS-Hanbun-Ko-Suru-Kurai-Nakayoshi-Craft (3DS半分こするくらい仲良しクラフト, Minecraft server) operations team",
                "role": "Operations team member (infrastructure, rule-making and bot development)",
                "summary": "Involved in running a community of around 30 people — from building the infrastructure to shaping its rules and automating operational work — on both the technical and the legal side.",
                "points": [
                    "Migrated the server infrastructure from a single Ubuntu box to a virtualised environment on a Proxmox cluster, and built purpose-based access control and monitoring",
                    "Led the drafting of the server rules into formal articles, taking them through two major revisions to the current body of 85 articles",
                    "Building a Discord bot, OpsBot, on my own to automate operational work (since Sep 2026; see the work section for details)",
                ],
                "tags": ["Proxmox", "Tailscale", "Discord Bot", "Constitutional law"],
            },
        ],
    },
    "skills": {
        "intro": "Mostly skills I've picked up through hands-on server operations alongside my studies. Levels are my own rating on a five-point scale — more dots means more proficiency.",
        "groups": [
            {
                "name": "Cloud / infrastructure",
                "items": [
                    {"name": "Proxmox VE", "level": 3, "note": "Clustered two physical machines, built a virtual network with SDN (VXLAN), and run 7+ LXC containers and VMs"},
                    {"name": "Linux (Debian)", "level": 4, "note": "The base OS for every container and VM; I handle service setup and systemd management, and run an Ubuntu-family OS on my personal laptop too"},
                    {"name": "Tailscale", "level": 4, "note": "Separate roles with ACL tags, and designed the access paths between administrators, monitoring and the Minecraft servers"},
                    {"name": "Cloudflare (Workers / Tunnel)", "level": 3, "note": "Exposed operator-facing services with Tunnel plus Discord OAuth, and built the OpsBot backend and REWIS's authoritative external data store on Workers"},
                ],
            },
            {
                "name": "Observability / operations",
                "items": [
                    {"name": "Prometheus / Grafana", "level": 2, "note": "Monitoring for TPS, uptime and network reachability, with seven alert rules; expanding what's monitored gradually, by trial and error, as the need arises"},
                    {"name": "Crafty Controller", "level": 5, "note": "Set up a GUI management environment the whole team can use — venv-based install, running it as a systemd service, and automatic restart configuration included"},
                ],
            },
            {
                "name": "Development",
                "items": [
                    {"name": "JavaScript", "level": 3, "note": "Implemented the REWIS frontend (vanilla JS) and its PWA support"},
                    {"name": "Python", "level": 3, "note": "Implemented the CT102 side of OpsBot (the polling loop and external API integration)"},
                    {"name": "TypeScript", "level": 2, "note": "Implemented the OpsBot backend on Cloudflare Workers"},
                    {"name": "HTML / CSS", "level": 4, "note": "Designed and styled the REWIS UI from scratch"},
                ],
            },
            {
                "name": "Law",
                "items": [
                    {"name": "Constitutional law", "level": 4, "note": "My seminar research subject; I also apply it to designing operator authority when drafting the server rules"},
                ],
            },
        ],
    },
    "works": {
        "intro": "Four projects I can share publicly, drawn from server operations and personal development.",
        "items": [
            {
                "title": "Building and running the Minecraft server infrastructure",
                "tagline": "Clustered two home servers with Proxmox to build and run the Minecraft servers and their surrounding services, access control included",
                "role": "Server setup and infrastructure management",
                "period": "Nov 2022 — present",
                "stack": ["Proxmox VE", "LXC / VM", "Tailscale", "Cloudflare Tunnel", "Nginx Proxy Manager", "Prometheus / Grafana", "Crafty Controller"],
                "body": "It started as nothing more than server software installed on an Ubuntu machine. Feeling the need to work out how much access to grant each of three kinds of user — players, the operations team, and myself as administrator — I moved to a virtualised environment on Proxmox VE from March 2026. Player traffic goes through a relay server plus a Tailscale VPN, operator-facing web services through a Cloudflare Tunnel, and administrative work through Tailscale, with a separate protection model for each path. I also built out monitoring (Prometheus/Grafana, seven alerts) and brought in GUI tools such as Crafty Controller so the whole team can manage the setup.",
                "highlights": [
                    "Kept a community of around 30 players running continuously since 2022",
                    "Clustered two physical machines with Proxmox and split them into 7+ purpose-specific LXC containers and VMs",
                    "Built a hardened environment without cutting corners, even though \"no one outside is watching\"",
                ],
                "link": {"label": "Official site", "href": "https://www.ds2.uk/"},
            },
            {
                "title": "Drafting the server rules into formal articles",
                "tagline": "Drafting server rules that follow the form of statutory articles while staying readable for players",
                "role": "Rule drafting and codification",
                "period": "Sep 2022 — present",
                "body": "Drawing on the character of the predecessor server and the feel of the community, I drafted the rules with an eye to balancing what players want against stable operation. They follow the form of statutory articles, but I deliberately work in colloquial phrasing to keep them readable. I put particular weight on defining precisely how far operator authority extends, so as to check abuse of that authority by the operators themselves, myself included — applying the constitutional law I major in to practice.",
                "highlights": [
                    "85 articles currently, with two major revisions since they were first enacted",
                    "Govern a community of around 30 players and 6 operators",
                    "Tightened the scope of operator authority and designed checks against abuse of it, my own included (drawing on a constitutional law perspective)",
                ],
                "link": {"label": "Server rules", "href": "https://www.ds2.uk/rule"},
            },
            {
                "title": "OpsBot — a Discord bot for automating operational work",
                "tagline": "A Discord bot that automates the administrative tasks of running a server — filings, votes, permission requests, reminders and the like",
                "role": "Design and implementation (solo project)",
                "period": "Sep 2026 — present",
                "stack": ["Cloudflare Workers (TypeScript)", "D1", "Python (poller on a Proxmox CT)", "Discord API", "Claude Code CLI"],
                "body": "I built it so the routine administrative tasks that come up day to day on the server — receiving filings, running votes, granting named permissions, sending reminders — can be completed entirely through commands and forms in the bot. It's a two-layer design: Cloudflare Workers (TypeScript) plus D1 as the API and data layer, and a Python poller running on Proxmox that continuously watches Discord messages and reactions to trigger each task. Since the Cloudflare Workers free tier allows only five cron jobs, I scheduled several batch processes — reminder checks, ledger updates and so on — to run together under a single cron, making the whole thing fit within the tier. Any task that calls for a judgement, such as approval or rejection, always begins with human input; the LLM (Claude) is used only for the kind of checks a person tends to miss, like spotting gaps in a submission or proposing candidates for task assignment. The automatic task detection and assignment feature is currently running in a trial (shadow mode) in which results are only written to a log and no actual notifications are sent.",
                "highlights": [
                    "Turned several administrative tasks — filings, votes, permissions, reminders — into commands and automated them",
                    "Built as a two-layer design: Cloudflare Workers (TS) + D1 and a Python poller on Proxmox",
                    "Designed a schedule that consolidates several batches into one cron, under the Workers free tier's five-cron limit",
                ],
                "link": {"label": "GitHub", "href": "https://github.com/Gorodrich/ops-bot"},
            },
            {
                "title": "REWIS (a worldwide railway information system)",
                "tagline": "A web app, much like a real-world transit routing service, that answers \"I don't know how to get there\" on an ever-growing rail network",
                "role": "Design and implementation (solo project; data supplied over time by each railway operator, i.e. the players)",
                "period": "Oct 2025 — present",
                "stack": ["HTML", "CSS", "JavaScript (vanilla)", "GitHub Pages", "Cloudflare Workers (authoritative external data store and editing API)", "PWA"],
                "body": "The rail network inside Minecraft had grown to the point where players were building route maps like those of real railway companies, and more and more of them couldn't tell which lines would get them to their destination — that's what prompted me to start building this. I needed login and data writes within the constraints of a static site on GitHub Pages, so I switched the data, originally kept as JSON in the repository, to a model with Cloudflare Workers as the authoritative external store, letting each railway operator (player) edit their own data directly from an operator page. I studied existing transit routing services, and aimed for PWA support that feels app-like on mobile while still working well on desktop.",
                "highlights": [
                    "Delivered data editing on a static site, with Cloudflare Workers as the authoritative external store",
                    "Covers 7 lines and 34 stations today, with plans to grow to around 50 lines and 200 stations",
                    "PWA support that combines an app-like feel with a proper desktop view",
                ],
                "links": [
                    {"label": "Visit the site", "href": "https://k-triar.github.io/rewis/"},
                    {"label": "GitHub", "href": "https://github.com/k-triar/rewis"},
                ],
            },
        ],
    },
}
