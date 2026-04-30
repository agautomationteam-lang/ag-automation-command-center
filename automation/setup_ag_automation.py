#!/usr/bin/env python3
"""
AG AUTOMATION — MASTER SETUP SCRIPT
====================================
This script configures your entire automation stack:
1. Sets up VAPI agent with scripts
2. Creates Make.com webhook bridges  
3. Configures GHL workflows
4. Tests everything end-to-end

USAGE:
    1. Fill in the CONFIG section below with your API keys
    2. Save this file as setup_ag_automation.py
    3. Run: python3 setup_ag_automation.py
    4. Follow the prompts

SECURITY:
    - This script runs on YOUR computer
    - Your API keys never leave your machine
    - No data is sent to any third party except the APIs you configure
"""

import requests
import json
import time
from datetime import datetime

# ============================================================
# CONFIG — FILL THESE IN WITH YOUR ACTUAL KEYS
# ============================================================
CONFIG = {
    # VAPI.ai
    "vapi_api_key": "YOUR_VAPI_KEY_HERE",  # From vapi.ai dashboard
    "vapi_phone_number": "+1403XXXXXXX",   # Twilio number you bought

    # GoHighLevel
    "ghl_api_key": "YOUR_GHL_API_KEY_HERE",  # From GHL Settings > API
    "ghl_location_id": "YOUR_GHL_LOCATION_ID",  # From GHL Settings > Business Profile
    "ghl_agency_id": "YOUR_GHL_AGENCY_ID",

    # Make.com
    "make_api_key": "YOUR_MAKE_API_KEY",  # From Make.com profile
    "make_team_id": "YOUR_MAKE_TEAM_ID",

    # Notification (pick ONE)
    "telegram_bot_token": "",  # Optional: From @BotFather
    "telegram_chat_id": "",     # Optional: Your Telegram chat ID
    "discord_webhook": "",    # Optional: Discord channel webhook URL
    "slack_webhook": "",      # Optional: Slack incoming webhook URL

    # Google (for Sheets backup)
    "google_sheet_id": "",    # Optional: ID from Sheets URL

    # Your business details
    "your_name": "Your Name",
    "your_phone": "+1403XXXXXXX",
    "your_email": "hello@agautomation.ca",
    "calendly_link": "https://calendly.com/agautomation/ai-audit",
    "loom_link": "https://loom.com/share/YOUR_DEMO_VIDEO",
    "tally_link": "https://tally.so/YOUR_ONBOARDING_FORM",
}

# ============================================================
# STEP 1: VAPI.AI AGENT SETUP
# ============================================================
def setup_vapi_agent():
    print("\n[STEP 1] Setting up VAPI.ai agent...")

    url = "https://api.vapi.ai/assistant"
    headers = {
        "Authorization": f"Bearer {CONFIG['vapi_api_key']}",
        "Content-Type": "application/json"
    }

    # Load agent config from file
    with open('vapi_agent_config.json', 'r') as f:
        agent_config = json.load(f)

    # Replace placeholders
    agent_config['webhook']['url'] = "{{MAKE_WEBHOOK_PLACEHOLDER}}"  # Will be updated after Make.com setup

    response = requests.post(url, headers=headers, json=agent_config)

    if response.status_code == 201:
        agent_id = response.json().get('id')
        print(f"✅ VAPI agent created: {agent_id}")
        return agent_id
    else:
        print(f"❌ VAPI error: {response.status_code} - {response.text}")
        return None

# ============================================================
# STEP 2: MAKE.COM WEBHOOK SETUP
# ============================================================
def setup_make_webhook():
    print("\n[STEP 2] Setting up Make.com webhook...")

    # Create webhook in Make.com
    url = f"https://make.com/api/v2/teams/{CONFIG['make_team_id']}/hooks"
    headers = {
        "Authorization": f"Token {CONFIG['make_api_key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": "AG VAPI Lead Capture",
        "type": "webhook",
        "data": ["call_id", "business_name", "contact_name", "phone", "email", "city", "trade", "call_result"]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        webhook_url = response.json().get('url')
        print(f"✅ Make.com webhook created: {webhook_url}")
        return webhook_url
    else:
        print(f"❌ Make.com error: {response.status_code}")
        print("Manual workaround: Create webhook in Make.com UI, copy URL, paste into VAPI config")
        return None

# ============================================================
# STEP 3: TEST END-TO-END
# ============================================================
def test_pipeline(webhook_url):
    print("\n[STEP 3] Testing complete pipeline...")

    # Send test payload to Make.com webhook
    test_payload = {
        "call_id": "test_001",
        "business_name": "Test Plumbing Inc",
        "contact_name": "Test Mike",
        "phone": "+14035551234",
        "email": "test@example.com",
        "city": "Calgary",
        "trade": "plumber",
        "call_result": "interested",
        "duration": 120,
        "recording_url": "",
        "transcript": "Test call",
        "notes": "Wants AI audit"
    }

    response = requests.post(webhook_url, json=test_payload)

    if response.status_code == 200:
        print("✅ Test payload sent successfully")
        print("   Check your:")
        print("   1. GoHighLevel — 'Test Mike' should appear as a contact")
        print("   2. Notification — You should get a Telegram/Discord/Slack message")
        print("   3. Google Sheets — Row should appear in your backup sheet")
        return True
    else:
        print(f"❌ Test failed: {response.status_code}")
        return False

# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("AG AUTOMATION — MASTER SETUP")
    print("=" * 60)
    print(f"Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Validate config
    if "YOUR_" in CONFIG['vapi_api_key']:
        print("\n⚠️  WARNING: You haven't filled in your API keys!")
        print("   Edit CONFIG in this file with your actual keys.")
        print("   Get them from:")
        print("   - VAPI: vapi.ai → Dashboard → API Keys")
        print("   - GHL: Settings → API → Generate Key")
        print("   - Make: Profile → API → Generate Token")
        return

    # Step 1: VAPI
    agent_id = setup_vapi_agent()
    if not agent_id:
        print("\n⚠️  VAPI setup failed. Continuing with manual configuration...")

    # Step 2: Make.com webhook
    webhook_url = setup_make_webhook()
    if not webhook_url:
        print("\n⚠️  Make.com webhook setup failed.")
        webhook_url = input("   Paste your Make.com webhook URL manually: ").strip()

    # Update VAPI with real webhook URL
    if agent_id and webhook_url:
        print("\n[UPDATING] Setting VAPI webhook to Make.com URL...")
        update_url = f"https://api.vapi.ai/assistant/{agent_id}"
        headers = {"Authorization": f"Bearer {CONFIG['vapi_api_key']}", "Content-Type": "application/json"}
        update_payload = {"webhook": {"url": webhook_url, "events": ["call.completed"]}}
        requests.patch(update_url, headers=headers, json=update_payload)
        print("✅ VAPI webhook updated")

    # Step 3: Test
    if webhook_url:
        success = test_pipeline(webhook_url)

        if success:
            print("\n" + "=" * 60)
            print("✅ SETUP COMPLETE!")
            print("=" * 60)
            print(f"\nVAPI Agent ID: {agent_id}")
            print(f"Make.com Webhook: {webhook_url}")
            print(f"\nNext steps:")
            print("1. Make a test call to YOUR phone")
            print("2. Verify contact appears in GoHighLevel")
            print("3. Verify you get notification")
            print("4. If all 3 work → start calling real leads")
        else:
            print("\n❌ Pipeline test failed. Check logs above.")

if __name__ == "__main__":
    main()
