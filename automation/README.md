# AG Automation — Complete Automation Package

## What's Inside

| File | Purpose |
|------|---------|
| `vapi_agent_config.json` | Complete VAPI agent with all scripts, webhooks, voicemail |
| `make_com_scenarios.json` | 3 Make.com scenario blueprints (import-ready) |
| `ghl_workflows.json` | GHL nurture sequences, onboarding, monthly reports |
| `setup_ag_automation.py` | Master Python script — fills in your API keys, runs everything |
| `ghl_manual_steps.txt` | Step-by-step GHL setup (phone, email, fields, pipeline) |
| `test_checklist.txt` | 8-step test checklist before going live |

## How to Use

### Option A: Push-Button Setup (Recommended)
1. Copy `setup_ag_automation.py` to your computer
2. Fill in the CONFIG section with your API keys
3. Run: `python3 setup_ag_automation.py`
4. Script configures everything automatically

### Option B: Manual Import
1. **VAPI**: Copy JSON from `vapi_agent_config.json` → paste into VAPI dashboard
2. **Make.com**: Import scenarios from `make_com_scenarios.json`
3. **GHL**: Follow `ghl_manual_steps.txt` for web interface setup
4. **Test**: Run through `test_checklist.txt` before going live

## Your URLs
- **Agent Board**: https://agautomationteam-lang.github.io/ag-automation-command-center/agent-os.html
- **May Dashboard**: https://agautomationteam-lang.github.io/ag-automation-command-center/may-dashboard.html

## Support
Each tool has its own support:
- VAPI: https://docs.vapi.ai
- Make.com: https://make.com/help
- GHL: https://help.gohighlevel.com
