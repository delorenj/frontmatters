# Documentation Organization Analysis Report
Generated for 538 markdown files

## Executive Summary

- **Total Files Analyzed**: 538
- **Unique Tags Proposed**: 17
- **Content Types Identified**: 10

## Content Type Distribution

| Content Type | Count | Percentage |
|--------------|-------|------------|
| general | 431 | 80.1% |
| documentation | 31 | 5.8% |
| prompt | 18 | 3.3% |
| agent | 16 | 3.0% |
| blog | 11 | 2.0% |
| draft | 11 | 2.0% |
| workflow | 8 | 1.5% |
| configuration | 8 | 1.5% |
| research | 2 | 0.4% |
| thread | 2 | 0.4% |

## Proposed Tag Analysis (≥2 occurrences)

| Tag | Frequency | Related Tags |
|-----|-----------|--------------|
| programming | 92 | agent, ai, api... |
| ai | 70 | agent, agents, blog... |
| infrastructure | 31 | ai, api, documentation... |
| blog | 28 | ai, draft, programming... |
| api | 26 | agent, database, infrastructure... |
| prompt | 23 | ai, documentation, draft... |
| agent | 18 | ai, api, draft... |
| documentation | 18 | ai, infrastructure, prompt... |
| draft | 17 | agent, ai, blog... |
| workflow | 16 | ai, blog, documentation... |
| database | 14 | ai, api, programming |
| prompts | 13 | ai, documentation, infrastructure... |
| configuration | 9 | ai |
| research | 7 |  |
| agents | 6 | ai |
| thread | 4 | ai, prompt, prompts |

## Categorization Rules

These rules resolve conflicts when files could belong to multiple categories:

### Rule 1: System prompts should be organized by their primary use case, not by project
- **Condition**: `content_type == 'prompt' and 'system' in filename.lower()`
- **Category**: `AI/Prompts/System`
- **Priority**: 1

### Rule 2: Project-specific agents should live with the project, not in general agents
- **Condition**: `content_type == 'agent' and any(project in directory_context for project in ['RepRally', 'Trinote', 'specific_project'])`
- **Category**: `Projects/{project}/Agents`
- **Priority**: 2

### Rule 3: All blog content should be centralized regardless of topic
- **Condition**: `content_type == 'blog' or 'blog' in filename.lower()`
- **Category**: `AI/Blog`
- **Priority**: 1

### Rule 4: Research should be organized by topic, not by type
- **Condition**: `content_type == 'research'`
- **Category**: `AI/Research/{topic}`
- **Priority**: 3

### Rule 5: Workflows should be organized by their domain of application
- **Condition**: `content_type == 'workflow'`
- **Category**: `AI/Workflows/{domain}`
- **Priority**: 2

## Optimization Recommendations

### 1. Tag Consolidation Opportunities

- **ai** and **blog**: 27 files in common
- **ai** and **prompt**: 14 files in common
- **ai** and **prompts**: 13 files in common
- **ai** and **programming**: 12 files in common
- **prompt** and **prompts**: 11 files in common

### 2. Suggested Primary Categories

Based on content analysis, these primary categories would provide optimal organization:

- **General** (431 files)
- **Documentation** (31 files)
- **Prompt** (18 files)
- **Agent** (16 files)
- **Blog** (11 files)
- **Draft** (11 files)
- **Workflow** (8 files)
- **Configuration** (8 files)

## File-by-File Tag Recommendations

| File | Current Tags | Proposed Tags | Content Type |
|------|--------------|---------------|--------------|
| docs/33GOD.md | None | api | general |
| docs/AI/AI.md | None | infrastructure, ai | general |
| docs/AI/Agents/Agents.md | None | agent, agents, ai | agent |
| docs/AI/Agents/README.md | None | agents, ai | documentation |
| .../A Farewell to Developers We Had a Good Run..md | None | blog, ai | general |
| ...t - And neither are you, so whats your point.md | None | blog, ai | blog |
| ...og, Introducing the Common Project Framework.md | None | blog, ai | blog |
| ...ng Problem-Solving for the Next Generation 1.md | None | blog, ai | blog |
| ...ning Problem-Solving for the Next Generation.md | None | blog, programming, ai | blog |
| docs/AI/Blog/Blog, The equation for hotness 1.md | None | blog, ai | blog |
| docs/AI/Blog/Blog, The equation for hotness.md | None | blog, ai | blog |
| docs/AI/Blog/Blog.md | None | blog, programming, ai | blog |
| docs/AI/Blog/Draft, Claude Flow.md | None | blog, draft, ai | draft |
| ..., It's Time to Rethink the Interview Process.md | None | blog, draft, workflow, ai | draft |
| ...no replacement (yet) for Software Architects.md | None | blog, draft, ai | draft |
| ... LLMs to Respect your Weird-Ass Architecture.md | None | blog, draft, ai | draft |
| ...ft, The AI Paradox More Solutions, Less Time.md | None | blog, programming, draft, ai | draft |
| ...aft, The Paradox of AI Workflow Optimization.md | None | blog, draft, workflow, ai | workflow |
| .../AI/Blog/Draft, The Solution Space Explosion.md | None | blog, programming, draft, ai | draft |
| docs/AI/Blog/Draft, The Tinder Effect.md | None | blog, draft, ai | draft |
| docs/AI/Blog/Hots.md | None | blog, ai | general |
| ... a comment on my Farewell to Developers post.md | None | blog, ai | blog |
| docs/AI/Blog/Post, Draft, The New Rockstar Dev.md | None | blog, programming, draft, ai | blog |
| ... A Farewell to Developers We Had a Good Run..md | None | blog, ai | general |
| ...nterview Process is Selecting for Extinction.md | None | blog, workflow, ai | general |
| ... a comment on my Farewell to Developers post.md | None | blog, ai | blog |
| ...no replacement (yet) for Software Architects.md | None | blog, programming, ai | general |
| ...ning Problem-Solving for the Next Generation.md | None | blog, ai | general |
| ...ing, The Paradox of AI Workflow Optimization.md | None | blog, programming, workflow, ai | workflow |
| ...LMs to Respect your Weird-Ass Architecture 1.md | None | blog, ai | general |
| ... the latest overhyped misguided garbage tool.md | None | documentation, blog, workflow, ai | documentation |
| docs/AI/Context/Context.md | None | ai | general |
| docs/AI/Context/JQ_Cheatsheet.md | None | ai | general |
| docs/AI/Model Optimization - 2025-04-17.md | None | ai | general |
| docs/AI/Prompts/Implement MCP Client in gptme.md | None | programming, prompts, ai | general |
| ...ompt, Coding, Port Collision and Remediation.md | None | infrastructure, prompt, prompts, ai | prompt |
| ...nal, Cover Letter, Technical Leadership Role.md | None | prompt, prompts, ai | prompt |
| ... that analyzes technical meeting transcripts.md | None | prompt, prompts, ai | prompt |
| ...prompt that generates optimal system prompts.md | None | prompt, prompts, ai | prompt |
| ...ompt, RepRally, Vaultwarden, Ticket Creation.md | None | infrastructure, prompt, prompts, ai | prompt |
| ...sted git server for automated backups## Goal.md | None | prompt, documentation, prompts, ai, infrastructure | prompt |
| ...fra, How to set up a self-hosted script repo.md | None | prompt, documentation, prompts, ai, infrastructure | prompt |
| ...on as a participant in a transcribed meeting.md | None | prompt, prompts, thread, ai | prompt |
| ...pt to Architectural Design Document (legacy).md | None | prompt, prompts, ai | prompt |
| ...low, Trello and Thread Log with Optional TDD.md | None | prompt, workflow, prompts, thread, ai | prompt |
| docs/AI/Prompts/Prompts.md | None | programming, prompt, prompts, ai | prompt |
| ...mpts/RepRally Typescript Dependency Injector.md | None | programming, prompts, ai | general |
| docs/AI/README.md | None | ai | documentation |
| docs/AI/Research/Research.md | None | ai, research | research |
| docs/AI/Teams/Agent Forge.md | None | agent, ai | agent |
| docs/AI/Teams/Trello_Management_Team.md | None | ai | general |
| docs/AI/Things to Look Into.md | None | database, ai | general |
| ...-04-11 Trinote 2.0 Dev Environment Debugging.md | None | database, ai | general |
| .../AI/Threads/2025-04-22_Fixing_AppImage_Icons.md | None | ai | general |
| ...hreads/2025-04-23_Graphiti_Neo4j_Integration.md | None | infrastructure, ai | general |
| docs/AI/Threads/Claude Notification.md | None | ai | general |
| docs/AI/Threads/Codifying_a_worktree_strategy.md | None | ai | general |
| docs/AI/Threads/Git Bit me in the ass.md | None | ai | general |
| ...Prompt, Help configuring my audio on wet-ham.md | None | prompt, ai, configuration | prompt |
| ...o a new AI-focused team or role at Justworks.md | None | prompt, ai | prompt |
| ...reads/Screenshot Hosting for LLM Consumption.md | None | ai | general |
| ...AI/Threads/Sync Tailscale Files to Downloads.md | None | ai | general |
| ...reads/Thread, Gitfluence Implementation Plan.md | None | thread, ai | thread |
| ...AI/Threads/Unexpected Linode Billing Dispute.md | None | ai | general |
| ...ds/Video Prompt for AI Doomers and Dumbheads.md | None | prompt, ai | prompt |
| docs/AI/Threads/Zellij SSH Window Size Problem.md | None | ai | general |
| docs/AI/Threads/dub-c.ue-phase1.md | None | ai | general |
| docs/AI/Threads/dub-c.ue-phase2.md | None | programming, ai | general |
| docs/AI/Threads/mcpme-20250710.md | None | ai | general |
| docs/AI/Workflows/Workflows.md | None | workflows, programming, workflow, ai | workflow |
| docs/AI/pluggedin_mcp_server_configs.md | None | ai, configuration | configuration |
| docs/Amazon is a pile of horseshit.md | None | infrastructure | general |
| docs/Anatomy of Murder.md | None | None | general |
| docs/Assets/Hubs/DeLoDash.md | None | None | general |
| docs/Assets/Hubs/My Social Hubs.md | None | None | general |
| docs/BMO/Profiles/BMO.md | None | None | general |
| docs/Bon Iver - Complete Song List.md | None | None | general |
| docs/Bugs.md | None | programming | general |
| docs/CLAUDE.md | None | None | general |
| docs/CalendarTasks-2025-09-03.md | None | None | general |
| ...-09-03.sync-conflict-20250903-120306-DSLLPB2.md | None | None | general |
| docs/ChasesRocketAdventure.md | None | programming | general |
| docs/Citi Dispute with Trivago.md | None | None | general |
| docs/ClaudeFlowPrimer-step-by-step.md | None | programming | general |
| docs/ClaudeFlowPrimer.md | None | None | general |
| ...Primer.sync-conflict-20250904-110211-DSLLPB2.md | None | None | general |
| docs/Client PhoneLog Quality Questions.md | None | None | general |
| docs/Common Product Framework.md | None | None | general |
| docs/DEPLOY_README.md | None | None | documentation |
| docs/Dailies/2024-11-01.md | None | programming | general |
| docs/Dailies/2025-01-23.md | None | None | general |
| docs/Dailies/2025-04-08.md | None | None | general |
| docs/Dailies/2025-04-09.md | None | None | general |
| docs/Dailies/2025-04-25.md | None | None | general |
| docs/Dailies/2025-05-03.md | None | None | general |
| docs/Dailies/2025-05-05.md | None | None | general |
| docs/Dailies/2025-05-07.md | None | None | general |
| docs/Dailies/2025-05-12.md | None | None | general |
| docs/Daily News - 2025-07-21.md | None | None | general |
| docs/Daily News - 2025-07-22.md | None | None | general |
| docs/Daily News - 2025-07-23.md | None | None | general |
| docs/DeployAnimation.md | None | api, database | general |
| docs/DeployScriptFix-InitialPrompt.md | None | prompt | prompt |
| docs/Development/Zellij Custom Features Guide.md | None | documentation | documentation |
| .../Development/ruv-swarm-architecture-research.md | None | research | research |
| docs/Development/ruv-swarm-build-process.md | None | programming, workflow | general |
| ...evelopment/ruv-swarm-mcp-integration-journey.md | None | programming | general |
| ...Business Case and Developer Experience Guide.md | None | infrastructure, documentation | documentation |
| ...idraw/Drawing 2025-05-21 07.01.32.excalidraw.md | None | None | general |
| docs/Finance/FinanceDash.md | None | None | general |
| docs/Finance/Ledgers/2022.md | None | None | general |
| docs/Finance/Ledgers/2023.md | None | None | general |
| docs/Finance/Ledgers/2024.md | None | None | general |
| docs/Finance/Ledgers/2025.md | None | programming | general |
| ...ance/Purchases/Whirlpool Dishwasher Warranty.md | None | None | general |
| docs/Finance/Purchases/Whirlpool Fridge.md | None | None | general |
| docs/Finance/Tax Info.md | None | None | general |
| docs/Fuck you, Uber.md | None | None | general |
| docs/Funny_Bloodbank_README.md | None | None | documentation |
| ...rammVDNAForScienceAndReplication/orig/CLAUDE.md | None | None | general |
| ...enceAndReplication/orig/Family Tree Analysis.md | None | research | general |
| ...cienceAndReplication/orig/Migration Analysis.md | None | research | general |
| ...NAForScienceAndReplication/orig/claude-notes.md | None | None | general |
| ...n/orig/comprehensive_genetic_analysis_report.md | None | research | general |
| docs/Guitar Tabs/S P E Y S I D E.md | None | None | general |
| docs/Home/Appliances/Refrigerator.md | None | programming | general |
| docs/Home/Finance/Finance.md | None | None | general |
| docs/Home/Home.md | None | None | general |
| ...ppet, 1337x qBittorrent Search Engine Plugin.md | None | programming | general |
| ...nfrastructure/VS Code Tunnel Systemd Service.md | None | prompt, api | general |
| docs/Home/Infrastructure/index_Infrastructure.md | None | infrastructure | general |
| docs/Home/Tasks/Fix broken fridge drawer.md | None | None | general |
| docs/How_To_Properly_Use_Pnpm.md | None | None | general |
| docs/Hubs/Dashboard, My Social Hubs.md | None | None | general |
| docs/Hubs/FinanceDash.md | None | programming | general |
| docs/Ideas/2024-11-05.md | None | infrastructure | general |
| ...cept http oauth headers as env in mcp config.md | None | configuration | configuration |
| ...ablement will affect the entire RepRally org.md | None | None | general |
| docs/Ideas/Idea, Claude Project Manager.md | None | programming | general |
| docs/Ideas/Idea, Gitfluence.md | None | None | general |
| ...deas/Idea, Personal Customer Support Liaison.md | None | None | general |
| docs/Ideas/Idea, Personal MCP Prompt Server.md | None | prompt | prompt |
| docs/Ideas/Idea, PooperDeduper.md | None | programming | general |
| .../Idea, Stop Everything and Go Make Something.md | None | None | general |
| ...dea, Teach Kids AI Skills for the Future App.md | None | None | general |
| docs/Ideas/Ideas.md | None | None | general |
| docs/Ideas/MPC Video Tools.md | None | api | general |
| docs/Ideas/Slack Channel Chatter.md | None | api | general |
| docs/Ideas/TODAY.md | None | None | general |
| ... way to describe problem is the new problem .md | None | None | general |
| ...t way to describe problem is the new problem.md | None | None | general |
| ...ow much free time I have. It's called Irony..md | None | None | general |
| docs/Ideas/Thought, The Paradox of AI Workflows.md | None | api, workflow | workflow |
| docs/Ideas/Thought, optimizing your workflow.md | None | workflow | workflow |
| ... the latest overhyped misguided garbage tool.md | None | documentation, workflow | documentation |
| docs/Ideas/Trinote MCP Migration Toolkit.md | None | database | general |
| docs/Ideas/Watercooler.md | None | None | general |
| docs/Ideas/repo-tools.md | None | programming | general |
| ...Response to Rifat's Questions on Claude Code.md | None | None | general |
| ...o Rifat's question about poorly defined bugs.md | None | None | general |
| docs/Inbox/Thought, optimizing your workflow.md | None | workflow | workflow |
| ...liforia/ABA Tool Integration - Original Plan.md | None | None | general |
| docs/Intelliforia/DesktopApp/ImplementationPlan.md | None | None | general |
| docs/Intelliforia/DesktopApp/PRD.md | None | None | general |
| docs/Intelliforia/DesktopApp/Strategy.md | None | programming | general |
| docs/Intelliforia/DesktopApp/SystemPrompt.md | None | programming, prompt, draft | prompt |
| docs/Intelliforia/DesktopApp/note-improve-curl.md | None | None | general |
| docs/Intelliforia/Teammates.md | None | None | general |
| docs/Job Hunting/AmexResy/AmexResy.md | None | None | general |
| .../Job Hunting/AmexResy/Cover Letter, AmexResy.md | None | None | general |
| ...tral/Central, Interview, Payroll System Arch.md | None | prompt, database | general |
| docs/Job Hunting/Lattice/Cover Letter, Lattice.md | None | None | general |
| docs/Job Hunting/Lattice/Prospect, Lattice.md | None | None | general |
| docs/Just some fixes !.md | None | database | general |
| ... Update Async Issue/Current ShiftUpdate Flow.md | None | None | general |
| docs/Justworks/Meeting, 1on1, Wolf.md | None | None | general |
| ...at with Mike about how much everything sucks.md | None | None | general |
| ...works/Reassessing Our Documentation Strategy.md | None | programming | documentation |
| ...story/Archive/Task, Fix broken fridge drawer.md | None | None | general |
| docs/Logs and History/Infra/Initial AWS setup.md | None | infrastructure | general |
| docs/Mock Usage.md | None | None | general |
| docs/Music/Akai Fire Script Demo Manual.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-16.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-17.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-18.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-19.md | None | programming | general |
| docs/News Archive/Daily News - 2025-06-20.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-21.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-22.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-23.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-25.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-28.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-29.md | None | None | general |
| docs/News Archive/Daily News - 2025-06-30.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-01.md | None | programming | general |
| docs/News Archive/Daily News - 2025-07-02.md | None | programming | general |
| docs/News Archive/Daily News - 2025-07-03.md | None | programming | general |
| docs/News Archive/Daily News - 2025-07-04.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-05.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-06.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-07.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-08.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-09.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-10.md | None | programming | general |
| docs/News Archive/Daily News - 2025-07-11.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-12.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-13.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-14.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-16.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-17.md | None | programming | general |
| docs/News Archive/Daily News - 2025-07-19.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-20.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-21.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-24.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-26.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-27.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-28.md | None | programming | general |
| docs/News Archive/Daily News - 2025-07-29.md | None | None | general |
| docs/News Archive/Daily News - 2025-07-30.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-01.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-02.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-03.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-04.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-05.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-06.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-07.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-08.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-09.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-10.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-11.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-12.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-13.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-14.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-15.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-16.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-17.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-18.md | None | programming | general |
| ...-08-18.sync-conflict-20250818-080022-3WZFAYA.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-19.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-20.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-21.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-22.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-23.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-24.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-26.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-27.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-28.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-29.md | None | programming | general |
| docs/News Archive/Daily News - 2025-08-30.md | None | None | general |
| docs/News Archive/Daily News - 2025-08-31.md | None | None | general |
| ...-08-31.sync-conflict-20250831-081553-DSLLPB2.md | None | None | general |
| docs/News Archive/Daily News - 2025-09-01.md | None | None | general |
| docs/News Archive/Daily News - 2025-09-02.md | None | None | general |
| docs/News Archive/Daily News - 2025-09-03.md | None | None | general |
| docs/News Archive/Daily News - 2025-09-04.md | None | None | general |
| docs/News Archive/Daily News - 2025-09-05.md | None | None | general |
| docs/News Archive/Daily News - 2025-09-06.md | None | None | general |
| docs/News Archive/Daily News - 2025-09-07.md | None | None | general |
| docs/News Archive/Daily News - 2025-09-08.md | None | None | general |
| ...ianWorkflow/Agent Frontmatter Implementation.md | None | programming, agent | agent |
| docs/ObsidianWorkflow/Property Strategy.md | None | programming | general |
| .../ObsidianWorkflow/n8n-obsidian-vault-cleanup.md | None | None | general |
| .../ObsidianWorkflow/session/implementationPlan.md | None | None | general |
| docs/ObsidianWorkflow/session/sessionGoal.md | None | None | general |
| docs/PKM-Organization-Plan.md | None | programming | general |
| docs/PR-deploy-via-cli.md | None | infrastructure | general |
| docs/PR_Extraction_Plan_Client_Phone_Log_Page.md | None | None | general |
| docs/Postman/trello.postman.json.md | None | blog | blog |
| ...resentation Visual Assets - Generation Guide.md | None | documentation | documentation |
| docs/Projects/33GOD/Agent-Template.md | None | agent, draft | agent |
| docs/Projects/33GOD/Braindump.md | None | None | general |
| docs/Projects/33GOD/How I Envision It v1.md | None | None | general |
| docs/Projects/33GOD/How I Envision It v2.md | None | None | general |
| ...cts/33GOD/ImplementationPlan-WalkingSkeleton.md | None | programming | general |
| docs/Projects/33GOD/Initial Ideation.md | None | None | general |
| docs/Projects/33GOD/Overview.md | None | None | general |
| docs/Projects/33GOD/PRD-Agent.md | None | agent | agent |
| docs/Projects/33GOD/PRD.md | None | programming, api | general |
| docs/Projects/33GOD/System-Architecture.md | None | prompt | general |
| docs/Projects/33GOD/TechStack-v1.md | None | programming, database, api | general |
| docs/Projects/33GOD/WalkingSkeleton.md | None | programming, database, api | general |
| docs/Projects/33GOD/prd-and-plan.md | None | None | general |
| docs/Projects/ACD Web Proposals.md | None | None | general |
| docs/Projects/ACD.Consulting.md | None | None | general |
| docs/Projects/ACD_Consulting_Services.md | None | None | general |
| docs/Projects/AI Workflow CoP.md | None | workflow | workflow |
| docs/Projects/Advanced DNS Troubleshooting.md | None | None | general |
| docs/Projects/AgentForge/PRD.md | None | programming | general |
| docs/Projects/AgentForge/Task-v1.md | None | None | general |
| docs/Projects/AgentForge/Task-v2.md | None | None | general |
| docs/Projects/AmazonQ Full Context.md | None | infrastructure | general |
| docs/Projects/Castagram/Castagram.md | None | None | general |
| ...cts/Castagram/Zed suggestions for smolagents.md | None | agent | agent |
| docs/Projects/Castagram/attempt-1.md | None | draft | draft |
| ...cts/ChoreScore/DeLo Chores and Points System.md | None | programming, prompt | general |
| docs/Projects/ChoreScore/Monetization-Strategy.md | None | None | general |
| docs/Projects/ChoreScore/PRD.md | None | None | general |
| docs/Projects/ChoreScore/README.md | None | api | documentation |
| docs/Projects/ChoreScore/goal.md | None | None | general |
| docs/Projects/Company Animation.md | None | None | general |
| docs/Projects/Concierge/PRD.md | None | infrastructure | general |
| docs/Projects/Core_Philosophy_And_Frameworks.md | None | None | general |
| docs/Projects/Curi/Brainstorm, Agentic Strategy.md | None | agent | agent |
| ...ri/Github vs. Gitlab vs. Gitea (Open Source).md | None | None | general |
| docs/Projects/DNS Fix Summary - April 2025.md | None | None | general |
| docs/Projects/DNS Resolution Troubleshooting.md | None | None | general |
| docs/Projects/DNS Troubleshooting.md | None | None | general |
| docs/Projects/DeLoNET Configuration.md | None | infrastructure, configuration | configuration |
| docs/Projects/DeLoProxy Deployment Guide.md | None | documentation | documentation |
| ...tteAgents/chief-memory-officer-specification.md | None | None | general |
| ...Projects/DeepPaletteAgents/qa-engineer-agent.md | None | programming, agent | agent |
| docs/Projects/DeepPaletteAgents/qa-protocols.md | None | None | general |
| ...eAgents/senior-python-engineer-specification.md | None | programming | general |
| ...rojects/DeepPaletteAgents/testing-frameworks.md | None | None | general |
| docs/Projects/Directory.md | None | infrastructure | general |
| .../FLStudioProducerAgent/FLStudioProducerAgent.md | None | agent, api | agent |
| ...tfluence/Implementation Plan, Gitfluence, v2.md | None | programming | general |
| docs/Projects/How to invoice clients.md | None | None | general |
| docs/Projects/Idea, DocJangler.md | None | None | documentation |
| ...Projects/Implementation Plan, Gitfluence, v1.md | None | programming | general |
| docs/Projects/Infrastructure.md | None | infrastructure | general |
| docs/Projects/JobJangler/Tech Radar.md | None | None | general |
| docs/Projects/Neo's Problems/Screenplay.md | None | None | general |
| docs/Projects/PRD.md | None | None | general |
| docs/Projects/Project Kickoff and Ideation.md | None | programming | general |
| docs/Projects/Project, Wingbot.md | None | agent | general |
| ...ects/RepRally/AI Workflow Onboarding Runbook.md | None | documentation, workflow | workflow |
| docs/Projects/RepRally/Candidate Eval.md | None | None | general |
| docs/Projects/RepRally/GPTMe Agent Framework.md | None | agent | agent |
| docs/Projects/RepRally/Ideas.md | None | programming | general |
| docs/Projects/RepRally/Jan Plan.md | None | programming | general |
| docs/Projects/RepRally/Kanban.md | None | None | general |
| docs/Projects/RepRally/Things I Need.md | None | None | general |
| ...e to Unemployment Insurance Benefits Online!.md | None | None | general |
| docs/Projects/RepRally/max_llm_paper.md | None | None | general |
| docs/Projects/Server, Synology NAS (Emma).md | None | None | general |
| docs/Projects/Success Metrics Framework.md | None | programming | general |
| docs/Projects/Tech Debt Callout.md | None | None | general |
| docs/Projects/Untitled 1.md | None | None | general |
| docs/Projects/WeanPRD.md | None | None | general |
| ...cts/Web Scraping tool qdrant index add to kb.md | None | programming, database, api | general |
| docs/Projects/Wet-Ham, CPU.md | None | None | general |
| docs/Projects/Wet-Ham, GPU.md | None | None | general |
| docs/Projects/Wingbot.md | None | agent, api | general |
| docs/Projects/agent-project-workflow.md | None | agent, workflow | agent |
| docs/Projects/bAIos/INVENTORY.md | None | None | general |
| docs/Projects/bAIos/PRD.md | None | None | general |
| docs/Projects/bAIos/architecture.md | None | None | general |
| docs/Projects/bAIos/outline.md | None | None | general |
| docs/Projects/bAIos/provisioner.md | None | None | general |
| docs/Projects/bAIos/voice-notes-requirements.md | None | programming | general |
| docs/Projects/config_environments_mise_en_place.md | None | configuration | configuration |
| docs/Projects/configuration_mise_en_place.md | None | configuration | configuration |
| docs/Projects/delo.sh/Run Book.md | None | infrastructure | general |
| docs/Projects/docker-compose, Dashy.md | None | infrastructure, api | documentation |
| docs/Projects/docker-compose, Dify.md | None | infrastructure, database | documentation |
| ...ects/docker-compose, Lego SSL Cert Container.md | None | infrastructure, programming | documentation |
| docs/Projects/docker-compose, OpenGist,.md | None | database | documentation |
| docs/Projects/docker-compose, Wet-Ham Traefik.md | None | infrastructure | documentation |
| ...ojects/docker-compose, config.yml, OpenGist,.md | None | database, configuration | configuration |
| docs/Projects/docker-compose, traefik.md | None | infrastructure | documentation |
| docs/Projects/file_tasks_mise_en_place.md | None | None | general |
| docs/Projects/gptme-mcp-client-plan.md | None | None | general |
| docs/Projects/imi-init.md | None | None | general |
| docs/Projects/index_ACD.Consulting.md | None | None | general |
| docs/Projects/index_Agents.md | None | infrastructure, agent | agent |
| docs/Projects/index_Bruh.md | None | None | general |
| docs/Projects/index_Docker Stacks.md | None | infrastructure, api | documentation |
| docs/Projects/index_Hot Bagels.md | None | None | general |
| docs/Projects/index_Web Proposals.md | None | None | general |
| docs/Projects/index_attachments.md | None | infrastructure, api | general |
| docs/Projects/index_images.md | None | None | general |
| docs/Projects/index_process.md | None | workflow | general |
| docs/Projects/index_reachouts.md | None | None | general |
| docs/Projects/index_website.md | None | None | general |
| docs/Projects/kickoff.md | None | None | general |
| docs/Projects/mise-task-tools/bootstrap.md | None | None | general |
| docs/Projects/mise_tasks_add_mise_en_place.md | None | None | general |
| docs/Projects/mise_tasks_deps_mise_en_place.md | None | None | general |
| docs/Projects/mise_tasks_edit_mise_en_place.md | None | None | general |
| docs/Projects/mise_tasks_info_mise_en_place.md | None | None | general |
| docs/Projects/mise_tasks_ls_mise_en_place.md | None | None | general |
| docs/Projects/mise_tasks_mise_en_place.md | None | None | general |
| docs/Projects/mise_tasks_run_mise_en_place.md | None | None | general |
| docs/Projects/motherboard.md | None | None | general |
| ...tion-pfluff/Dossier, Mike and the Toxic Team.md | None | None | general |
| docs/Projects/operation-pfluff/Formal Complaint.md | None | None | general |
| docs/Projects/operation-pfluff/ProjectOverview.md | None | programming | general |
| ...ects/operation-pfluff/Teaching Journal Buddy.md | None | None | general |
| docs/Projects/reachouts.md | None | None | general |
| docs/Projects/running_tasks_mise_en_place.md | None | None | general |
| docs/Projects/schema.md | None | None | general |
| docs/Projects/settings_mise_en_place.md | None | configuration | configuration |
| docs/Projects/task_configuration_mise_en_place.md | None | configuration | configuration |
| docs/Projects/tasks_mise_en_place.md | None | None | general |
| docs/Projects/templates_mise_en_place.md | None | draft | draft |
| docs/Projects/toml_based_tasks_mise_en_place.md | None | None | general |
| docs/Projects/zailux/VISION.md | None | None | general |
| ...VISION.sync-conflict-20250904-155154-DSLLPB2.md | None | None | general |
| docs/README.md | None | None | documentation |
| docs/Rabbithole Log.md | None | None | general |
| docs/Reply to Ruben.md | None | None | general |
| ... Ruben.sync-conflict-20250908-005453-AS7FB6D.md | None | None | general |
| docs/Roblox-is-Garbage.md | None | None | general |
| docs/SPIKE_VERIFICATION_GUIDE.md | None | documentation, programming | documentation |
| docs/Settings/Preferred DateTime Format.md | None | None | general |
| docs/ShitHotelScam.md | None | None | general |
| docs/Skateboard Birthday Party Planning.md | None | None | general |
| docs/SoundsOfBrainRot.md | None | None | general |
| docs/Spawn OpenCode in a Zellij Session.md | None | programming | general |
| docs/Strategic-Overview-Dashboard.md | None | programming | general |
| docs/Stupid CLient Page.md | None | None | general |
| docs/Swarm vs Hive - ClaudeFlow Tip.md | None | programming | general |
| docs/TASKS.md | None | infrastructure | general |
| docs/TODAY.md | None | None | general |
| docs/Tag-Taxonomy.md | None | programming | general |
| ... and check your Statuses 2025-07-03 12-24-57.md | None | None | general |
| ... and check your Statuses 2025-07-20 13-12-02.md | None | programming | general |
| ... and check your Statuses 2025-07-20 13-34-49.md | None | None | general |
| ... and check your Statuses 2025-07-20 13-35-30.md | None | None | general |
| ... and check your Statuses 2025-07-20 13-37-41.md | None | None | general |
| ... and check your Statuses 2025-07-20 18-52-21.md | None | None | general |
| ... and check your Statuses 2025-07-25 09-24-28.md | None | None | general |
| ... and check your Statuses 2025-08-11 11-03-03.md | None | None | general |
| ...Tasks and Time Management/Dailies/2024-11-01.md | None | programming | general |
| ...Tasks and Time Management/Dailies/2024-11-04.md | None | None | general |
| ...Tasks and Time Management/Dailies/2024-11-05.md | None | infrastructure | general |
| ...Tasks and Time Management/Dailies/2024-11-06.md | None | None | general |
| ...Tasks and Time Management/Dailies/2024-11-07.md | None | None | general |
| docs/Teaching Bink AI.md | None | None | general |
| docs/Tech/Bloodbank Wayland Clipboard Solution.md | None | programming | general |
| docs/Tech/Chrome Remote Debugging Setup.md | None | infrastructure | general |
| docs/Tech/Local to Remote Screenshot Sync.md | None | None | general |
| docs/Tech/Shell/ZSH-Oh-My-Zsh-Optimization-2025.md | None | programming | general |
| docs/Tech/Syncthing Speed Optimization.md | None | api | general |
| docs/Tech/Terminal-Mouse-Corruption-Fix.md | None | None | general |
| docs/Tech/UV-gptme-Management-Guide.md | None | documentation | documentation |
| docs/Templater/CHANGELOG.md | None | None | general |
| docs/Templater/README.md | None | programming | documentation |
| ...n - From Code Writers to Agent Orchestrators.md | None | programming, agent | agent |
| ...h/AIWorkflowWorkshop/Agent_Personality_Guide.md | None | documentation, agent | agent |
| ...AIWorkflowWorkshop/Agent_Templates_Tech_Spec.md | None | agent, draft | agent |
| docs/Triumph/AIWorkflowWorkshop/CLAUDE.md | None | programming | general |
| ...iumph/AIWorkflowWorkshop/Challenge_Scenarios.md | None | None | general |
| ...mph/AIWorkflowWorkshop/Preparation_Checklist.md | None | None | general |
| docs/Triumph/AIWorkflowWorkshop/Takeaways.md | None | None | general |
| ...rkflowWorkshop/Task_Master_Integration_Guide.md | None | documentation | documentation |
| docs/Triumph/AIWorkflowWorkshop/Timeline.md | None | None | general |
| ...iumph/AIWorkflowWorkshop/Workshop_Invitation.md | None | programming | general |
| docs/Triumph/AIWorkflowWorkshop/Workshop_Plan.md | None | None | general |
| docs/Triumph/AIWorkflowWorkshop/survey_results.md | None | None | general |
| docs/Triumph/CalendarOverhaul.md | None | None | general |
| ...eDashboard/Client PhoneLog Quality Questions.md | None | None | general |
| ...Triumph/TrinoteDashboard/DOCKER_ARCHITECTURE.md | None | None | documentation |
| ...noteDashboard/Dashboard Project Requirements.md | None | None | general |
| ...inoteDashboard/Efficient Lookup of PhoneLogs.md | None | database | general |
| docs/Triumph/TrinoteDashboard/Fixes.md | None | None | general |
| docs/Triumph/TrinoteDashboard/Milestone.md | None | api | general |
| docs/Triumph/TrinoteDashboard/Milestone1.md | None | api | general |
| ...h/TrinoteDashboard/Phone Log Requirements v2.md | None | None | general |
| ...umph/TrinoteDashboard/Phone Log Requirements.md | None | None | general |
| .../TrinoteDashboard/Phone Log Task List (Demo).md | None | api | general |
| ...dar_overhaul/CALENDAR_IMPLEMENTATION_SUMMARY.md | None | None | general |
| ...h/calendar_overhaul/CalendarTasks-2025-09-03.md | None | None | general |
| ...lendar_overhaul/calendar-accessibility-guide.md | None | documentation | documentation |
| .../calendar_overhaul/calendar-animation-system.md | None | prompt | general |
| ...endar_overhaul/calendar-color-specifications.md | None | None | general |
| ...ndar_overhaul/calendar-design-specifications.md | None | None | general |
| ...dar_overhaul/calendar-implementation-roadmap.md | None | api | general |
| ...verhaul/calendar-interaction-design-patterns.md | None | None | general |
| ..._overhaul/calendar-keyboard-navigation-guide.md | None | documentation | documentation |
| ...endar_overhaul/calendar-magic-ui-integration.md | None | None | general |
| ...calendar_overhaul/calendar-overhaul-complete.md | None | programming | general |
| ...r_overhaul/calendar-performance-optimization.md | None | None | general |
| ...iumph/calendar_overhaul/calendar-qa-strategy.md | None | None | general |
| ...alendar_overhaul/calendar-ux-analysis-report.md | None | research | general |
| ...h/calendar_overhaul/calendar_analysis_report.md | None | research | general |
| ...rstanding MCP - From Conversation to Clarity.md | None | api, thread | thread |
| docs/Untitled 7.md | None | None | general |
| docs/Untitled 8.md | None | None | general |
| ...tled 8.sync-conflict-20250826-130809-DSLLPB2.md | None | None | general |
| docs/Untitled 9.md | None | None | general |
| docs/Untitled.md | None | None | general |
| docs/acd style guide.md | None | documentation | documentation |
| docs/claude flow contributions.md | None | None | general |
| docs/code/debug-mcp-connection.md | None | programming | general |
| docs/deployment-visualization-guide.md | None | documentation | documentation |
| docs/get_session_goals_complexity.md | None | programming | general |
| docs/gists/Snippet, generate-license.sh.md | None | api | general |
| docs/index_services.md | None | None | general |
| docs/me/Agentics Profile.md | None | agent | agent |
| docs/me/Cover Letter, EliseAI.md | None | api | general |
| docs/me/Cover Letter, ServicesNow.md | None | programming | general |
| docs/me/Cover Letter, Spotify.md | None | api | general |
| docs/me/Eng Leadership Bio.md | None | None | general |
| docs/me/Letter requesting to connect.md | None | None | general |
| docs/me/List of ME tags.md | None | None | general |
| docs/me/Little blurb about me and how I think.md | None | None | general |
| docs/me/My Ideal Company and Role.md | None | None | general |
| docs/me/MyAuthoritalVoice.md | None | None | general |
| docs/me/Project I'm proud of.md | None | database | general |
| docs/me/Resume, Generic.md | None | None | general |
| docs/me/Resume, Serverless.md | None | infrastructure | general |
| ...What am I working on in my career in general.md | None | None | general |
| docs/me/coding_style.md | None | None | general |
| docs/me/me.md | None | None | general |
| docs/no-explicit-any.md | None | programming | general |
| docs/no-regex-spaces.md | None | None | general |
| docs/no-this-before-super.md | None | programming | general |
| docs/palette-search-mcp.md | None | programming | general |
| docs/plan.sync-conflict-20250818-045048-DSLLPB2.md | None | None | general |
| docs/prefer-const.md | None | programming | general |
| docs/q.md | None | None | general |
| docs/scratch.md | None | None | general |
| docs/smart-templates/default/overview.md | None | None | general |
| docs/smart-templates/default/tags.md | None | None | general |
| docs/social/Forum, Dev.to.md | None | None | general |
| docs/social/Tweet, WatchMeSpin.md | None | None | general |
| docs/social/social.md | None | programming | general |
| docs/ssbnk-frontend-bootstrap.md | None | api | general |
| docs/stuff.md | None | None | general |
| docs/tech-debt-callouts.md | None | None | general |
| docs/templates/Agents/AmazonQ.md | None | infrastructure, agents | general |
| docs/templates/Agents/ClaudeCode.md | None | agents | general |
| docs/templates/Agents/General.md | None | programming, agents | general |
| docs/templates/Agents/OpenCode.md | None | agents | general |
| docs/templates/Simple.md | None | None | general |
| docs/templates/Tag-Based Properties Template.md | None | draft | draft |
| docs/templates/Template, Formatting, Callout.md | None | draft | draft |
| docs/templates/Template, Props, Prompt.md | None | prompt, draft | prompt |
| ...dlebars/Fireflies CSV Transcript to Markdown.md | None | None | general |
| docs/templates/handlebars/handlebars.md | None | None | general |
| docs/templates/scripts/scripts.md | None | None | general |
| ...minal-optimization/iterm2-optimization-guide.md | None | documentation | documentation |
| docs/threads/UNTITLED CHAT 2024-12-01 15 18 32.md | None | None | general |
| docs/threads/UNTITLED CHAT 2024-12-13 11 35 15.md | None | None | general |
| docs/tmp.md | None | None | general |
| docs/transcripts/2025-06-23_1_2025-06-25.md | None | None | general |