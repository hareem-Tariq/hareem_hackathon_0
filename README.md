# Personal AI Employee - Bronze Tier 🥉

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/hareem-Tariq/hareem_hackathon_0)

**Version**: 1.0 (Bronze Tier - Foundation)  
**Status**: ✅ Ready to Use  
**Hackathon 0 Compliant**

A local-first AI automation system that uses Claude Sonnet 4.5 to process files, analyze tasks, and create actionable plans. This is the **Bronze Tier** (MVP) implementation as specified in the Hackathon 0 requirements.

---

## 🎯 What is Bronze Tier?

Bronze Tier is the **minimum viable deliverable** for building an autonomous AI employee:

✅ **Required Features (All Implemented)**
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working watcher (filesystem monitoring)
- Claude Code reading from and writing to the vault
- Basic folder structure: /Inbox, /Needs_Action, /Done
- All AI functionality implemented as Agent Skills

⏱️ **Estimated Build Time**: 8-12 hours (from scratch)  
🔧 **Setup Time**: 5 minutes (this repo)

---

## 🏗️ Architecture

```
┌─────────────────┐
│  watch_inbox/   │  ← Drop files here
└────────┬────────┘
         │
         ▼
┌───────────────────────┐
│ watcher_filesystem.py │  Monitors folder
└────────┬──────────────┘
         │ Creates tasks
         ▼
┌─────────────────────┐
│  Inbox/             │  ← New tasks
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Needs_Action/       │  ← Ready for processing
└────────┬────────────┘
         │
         ▼
┌────────────────────────┐
│ orchestrator_claude.py │  Claude Sonnet 4.5
└────────┬───────────────┘
         │
         ├─→ Reads: Company_Handbook.md, Business_Goals.md
         ├─→ Applies: Agent Skills (planning, file analysis)
         ├─→ Writes: Task plans and analysis
         └─→ Archives: Done/
```

**Data Flow:**
1. User drops file in `watch_inbox/`
2. Watcher creates Markdown task in `vault/Inbox/`
3. Task moves to `vault/Needs_Action/`
4. Orchestrator processes with Claude API
5. Results saved in vault, original moved to `vault/Done/`

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Anthropic API key
- Windows (PowerShell) or Linux/Mac

### Installation

```bash
# 1. Install dependencies
pip install anthropic watchdog python-dotenv

# 2. Create .env file
copy .env.bronze.example .env
# Edit .env and add: ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# 3. Run Bronze Tier
.\start_local.ps1    # Windows
```

### Linux/Mac

```bash
# Terminal 1: Start watcher
python watcher_filesystem.py

# Terminal 2: Start orchestrator
python orchestrator_claude.py
```

---

## 📁 Project Structure

```
hackathon 0/
├── start_local.ps1                  ← Start script (Windows)
├── orchestrator_claude.py           ← Claude orchestrator (280 lines)
├── watcher_filesystem.py            ← File watcher (150 lines)
├── .env                             ← API keys (create this)
├── .env.bronze.example              ← Template
├── bronze_tier_config.yaml          ← Configuration
├── BRONZE_TIER_README.md            ← Full guide
├── BRONZE_TIER_QUICK_REF.md         ← Quick reference
├── README.md                        ← This file
├── watch_inbox/                     ← Drop files here
├── logs/                            ← Application logs
└── obsidian_vault/                  ← Knowledge base
    ├── Inbox/                       ← New tasks
    ├── Needs_Action/                ← Ready to process
    ├── Done/                        ← Completed tasks
    ├── agent_skills/                ← AI reasoning templates
    │   ├── planning_skills.md       ← Task decomposition
    │   └── file_analysis_skill.md   ← Document analysis
    ├── Dashboard.md                 ← System status
    ├── Company_Handbook.md          ← Business context
    └── Business_Goals.md            ← Strategic objectives
```

---

## 💡 Usage Example

```bash
# 1. Drop a text file
echo "Schedule team meeting for next Tuesday at 2pm to discuss Q1 results" > watch_inbox/meeting_request.txt

# 2. Watch the magic happen
# - Watcher detects file
# - Creates task in Inbox/
# - Orchestrator picks it up
# - Claude analyzes content
# - Plan created in vault
# - Original moved to Done/

# 3. Check results
cat obsidian_vault/Needs_Action/meeting_request_*_plan.md
```

---

## 🧠 Agent Skills (Bronze Tier)

### planning_skills.md
- Task decomposition strategies
- Step-by-step planning templates
- Success criteria definition
- Dependency identification

### file_analysis_skill.md
- Document type detection (email, invoice, note, etc.)
- Content extraction patterns
- Intent recognition
- Action item identification

**How It Works**: Claude reads these skills before processing each task, using them as reasoning templates to create better plans.

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Required
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# Optional (defaults shown)
VAULT_PATH=./obsidian_vault
WATCH_PATH=./watch_inbox
```

### Bronze Tier Settings

- **Check Interval**: 15 seconds
- **Claude Model**: `claude-sonnet-4-20250514` (Sonnet 4.5)
- **Max Tokens**: 2000 per request
- **Max File Size**: 50KB (larger files truncated)
- **Supported Files**: Text files (.txt, .md, etc.)

---

## 📚 Documentation

- **[BRONZE_TIER_README.md](BRONZE_TIER_README.md)** - Complete guide
- **[BRONZE_TIER_QUICK_REF.md](BRONZE_TIER_QUICK_REF.md)** - Quick reference
- **[BRONZE_TIER_CONVERSION_SUMMARY.md](BRONZE_TIER_CONVERSION_SUMMARY.md)** - Technical details
- **[bronze_tier_config.yaml](bronze_tier_config.yaml)** - Configuration reference

---

## 🎓 What Bronze Tier Teaches

1. **AI Agent Architecture**: Watcher → Orchestrator → LLM pattern
2. **Local-First Design**: File-based workflows, no cloud dependencies
3. **Agent Skills**: How to guide AI reasoning with templates
4. **Obsidian Integration**: Vault as knowledge base

Perfect for:
- Learning AI automation
- Prototyping workflows
- Testing Claude integration
- Building custom skills

---

## 🚫 Bronze Tier Limitations

What it **cannot** do (requires higher tiers):
- ❌ Send emails (no Gmail integration)
- ❌ Post to social media (no Twitter/LinkedIn)
- ❌ Access cloud systems (no Odoo/Slack)
- ❌ Execute actions (planning only)
- ❌ Human-in-the-loop approvals
- ❌ Task prioritization/queuing
- ❌ Cloud deployment

What it **can** do:
- ✅ Monitor filesystem for new files
- ✅ Analyze documents with Claude
- ✅ Create actionable plans (3-5 steps)
- ✅ Learn from company handbook
- ✅ Apply agent skills
- ✅ Archive completed work

---

## 🔧 Troubleshooting

### "ANTHROPIC_API_KEY not found"
Create `.env` file with your Anthropic API key

### No tasks being created
1. Check watcher is running (separate window)
2. Verify `watch_inbox/` folder exists
3. Check logs: `cat logs/orchestrator_bronze.log`

### Plans not generating
1. Verify Claude API key
2. Check orchestrator logs
3. Ensure agent skills exist in `obsidian_vault/agent_skills/`

### File encoding errors
Bronze Tier expects UTF-8 text files. Binary files will be marked as "cannot display" but won't crash.

---

## 🚀 Upgrade Path

### Silver Tier (Next Level)
**Time**: +20 hours  
**Adds**:
- Gmail watcher
- Email MCP server (send replies)
- HITL approval workflow

### Gold Tier
**Time**: +40 hours  
**Adds**:
- Social media watchers (Twitter, LinkedIn)
- Odoo ERP integration
- Task queue with prioritization

### Platinum Tier
**Time**: +60 hours  
**Adds**:
- Cloud deployment (GKE/Docker)
- Multi-tenant support
- Compliance audit logging
- API server

---

## 📊 Hackathon 0 Compliance

✅ **All Bronze Tier Requirements Met:**
- [x] Obsidian vault with Dashboard.md ✅
- [x] Company_Handbook.md ✅
- [x] Working filesystem watcher ✅
- [x] Claude reading from vault ✅
- [x] Claude writing to vault ✅
- [x] Folder structure: Inbox, Needs_Action, Done ✅
- [x] Agent Skills implementation ✅

**Estimated Build**: 8-12 hours (from scratch)  
**Actual Setup**: 5 minutes (this repo)

---

## 🤝 Contributing

This is a Bronze Tier implementation for learning and prototyping. To customize:

1. **Edit Agent Skills**: Modify `obsidian_vault/agent_skills/*.md`
2. **Update Handbook**: Add business context to `Company_Handbook.md`
3. **Customize Watcher**: Edit `watcher_filesystem.py` for specific file types
4. **Extend Orchestrator**: Add custom logic to `orchestrator_claude.py`

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- Anthropic (Claude Sonnet 4.5 API)
- Obsidian.md (Knowledge base inspiration)
- Hackathon 0 Specification (Architecture guidelines)

---

## 📞 Support

- **Check logs**: `logs/orchestrator_bronze.log`
- **Read docs**: `BRONZE_TIER_README.md`
- **Review config**: `bronze_tier_config.yaml`
- **Check vault**: `obsidian_vault/Dashboard.md`

---

**Bronze Tier Status**: 🥉 Foundation Complete  
**Ready for**: Learning, Prototyping, Local Automation  
**Next Step**: Try it! Drop a file in `watch_inbox/` and watch it work.

---

*Built for Hackathon 0 - Personal AI Employee Challenge*
