# Company Handbook - Bronze Tier

**Version**: 1.0 (Bronze Tier)  
**Last Updated**: 2026-02-19  
**Purpose**: Provide business context to the AI Employee

---

## 🏢 Company Overview

### Basic Information
- **Company Name**: [Your Company Name]
- **Industry**: [Your Industry]
- **Founded**: [Year]
- **Size**: [Number of Employees]
- **Headquarters**: [Location]

### Mission Statement
[Your company's mission statement - edit this section with your actual information]

### Core Values
1. Innovation and Excellence
2. Customer Success
3. Continuous Learning

---

## 👥 Key Personnel

### Leadership Team
- **CEO/Founder**: [Name] - [Email]
- **Key Contact**: [Name] - [Email]

*Note: Bronze Tier AI Employee will reference this information when processing tasks that mention team members.*

---

## 📧 Communication Protocols

### Response Time Guidelines
- **Urgent**: Within 2 hours
- **High Priority**: Within 4 hours
- **Normal**: Within 24 hours
- **Low Priority**: Within 3 days

### Priority Keywords
When these words appear in tasks, they indicate urgency:
- "URGENT" → Immediate attention needed
- "DEADLINE" → Time-sensitive
- "CONTRACT" → Requires careful review
- "PAYMENT" → Financial matter
- "LEGAL" → Needs legal review

---

## 💼 Business Processes (Bronze Tier Scope)

### Task Processing
1. **Incoming File**: Dropped in `watch_inbox/`
2. **Initial Review**: Watcher creates task in Inbox/
3. **Analysis**: Moves to Needs_Action/
4. **Processing**: Claude analyzes using agent skills
5. **Completion**: Results saved, task moved to Done/

### Document Types Bronze Tier Handles
- **Emails** (as .txt files): Extract key points, suggest responses
- **Notes**: Identify action items and create plans
- **Documents**: Analyze content and summarize
- **Data Files**: Identify structure and suggest analysis steps

---

## 🎯 Business Goals

See [[Business_Goals]] for strategic objectives that guide the AI Employee's priorities and decision-making.

---

## 🧠 Agent Skills Available

The Bronze Tier AI Employee has these capabilities:

1. **Planning**: Break down tasks into actionable steps
2. **File Analysis**: Understand document types and extract information
3. **Reasoning**: Apply business context to make intelligent suggestions

---

## 📋 Bronze Tier Limitations

What Bronze Tier **cannot** do (requires Silver/Gold/Platinum):
- ❌ Send emails

### Customer Support
- **Tier 1**: FAQ/Documentation (AI can handle)
- **Tier 2**: Technical support (escalate to engineering)
- **Tier 3**: Custom development (escalate to CTO)

---- ❌ Send emails
- ❌ Post to social media
- ❌ Access cloud systems (Gmail, Odoo, etc.)
- ❌ Execute payments
- ❌ Make external API calls

What it **can** do:
- ✅ Analyze documents and extract key information
- ✅ Create actionable plans from tasks
- ✅ Summarize content
- ✅ Identify priorities and suggest next steps
- ✅ Learn from Company_Handbook and Business_Goals

---

## 🎯 Decision-Making Guidelines

### When Processing Tasks
The AI should consider:
1. **Context**: What does Company_Handbook say about this?
2. **Priority**: Does this contain urgent keywords?
3. **Clarity**: Is the request clear enough to act on?
4. **Scope**: Is this within Bronze Tier capabilities?

### Output Format
Plans should include:
- **Objective**: What needs to be accomplished
- **Steps**: 3-5 actionable items
- **Notes**: Any considerations or blockers
- **Expected Outcome**: What success looks like

---

## 📚 Knowledge Base

### Key Documents in Vault
- **Dashboard.md**: System status and recent activity
- **Company_Handbook.md**: This file - business context
- **Business_Goals.md**: Strategic objectives
- **agent_skills/**: AI reasoning templates

### Common Task Types (Bronze Tier)
1. **Email Analysis**: Extract sender, subject, key points, action items
2. **Document Review**: Summarize content, identify important sections
3. **Note Processing**: Extract action items and deadlines
4. **Data Review**: Identify structure, suggest analysis approaches

---

## 🔄 Continuous Improvement

### Learning Process
As Bronze Tier AI Employee processes tasks:
1. Patterns emerge from successful task handling
2. Agent skills can be updated (by humans)
3. Company_Handbook can be refined with new context
4. Business_Goals can guide prioritization

### Feedback
To improve the AI Employee:
- Review completed tasks in Done/ folder
- Update agent skills based on patterns
- Add relevant context to this handbook
- Refine Business_Goals as strategy evolves

---

## 📝 Bronze Tier Notes

**What This Tier Is For:**
- Learning the AI Employee architecture
- Testing Claude integration locally
- Prototyping workflows
- Building custom agent skills

**Upgrade Path:**
- **Silver Tier**: Add Gmail watcher + email sending
- **Gold Tier**: Add social media integrations
- **Platinum Tier**: Cloud deployment + multi-tenancy

---

## 📞 Getting Help

- **Documentation**: See BRONZE_TIER_README.md
- **Quick Reference**: See BRONZE_TIER_QUICK_REF.md
- **Configuration**: See bronze_tier_config.yaml
- **Logs**: Check logs/orchestrator_bronze.log

---

**Instructions for AI Employee** (Bronze Tier):
- Read this handbook before analyzing tasks
- Use Business_Goals for strategic context
- Apply agent skills (planning, file analysis)
- Create clear, actionable plans
- Move completed work to Done/

**Last Updated**: 2026-02-19  
**Tier**: 🥉 Bronze (Foundation)
