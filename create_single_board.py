#!/usr/bin/env python3
"""
Create single consolidated Trello board for DeployHelp LLC
"""

import requests
import json

API_KEY = "2ff6b8c648075cb0239fba4fa84f9e84"
TOKEN = "ATTAb1fecccb516b8eb552f43ce527aa0301a710f27416f422d145a97870550c7f5e74E8AC7E"
BASE_URL = "https://api.trello.com/1"

def get_auth_params():
    return {"key": API_KEY, "token": TOKEN}

def create_board(name, desc=""):
    url = f"{BASE_URL}/boards/"
    params = get_auth_params()
    params["name"] = name
    params["desc"] = desc
    params["prefs_permissionLevel"] = "private"
    params["prefs_background"] = "blue"
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()

def create_list(board_id, name, pos="bottom"):
    url = f"{BASE_URL}/lists"
    params = get_auth_params()
    params["name"] = name
    params["idBoard"] = board_id
    params["pos"] = pos
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()

def create_card(list_id, name, desc="", pos="bottom"):
    url = f"{BASE_URL}/cards"
    params = get_auth_params()
    params["name"] = name
    params["desc"] = desc
    params["idList"] = list_id
    params["pos"] = pos
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()

def get_structure():
    """Single board structure with all tasks"""
    return {
        "board": {
            "name": "?? DeployHelp Pre-Launch Checklist",
            "description": "Complete these tasks to ensure brand and offering consistency before business outreach. Organized by priority and phase."
        },
        "lists": [
            {
                "name": "?? PHASE 1: Foundation (Week 1-2) ??",
                "cards": [
                    {
                        "name": "Brand Voice & Tone Guidelines",
                        "desc": "**Priority: CRITICAL**\n\nDocument how we communicate:\n? Friendly but professional\n? Technical but accessible\n? Multilingual (EN, AM, RU, UA)\n? Focus on practical solutions vs. corporate speak\n\n**Deliverable:** 1-2 page brand voice guide"
                    },
                    {
                        "name": "Value Proposition & Positioning",
                        "desc": "**Priority: CRITICAL**\n\nClear statement answering:\n? What we do: Customer support & automation consulting\n? Who we serve: Small to medium businesses, SaaS companies, multilingual teams\n? Why we're different: Multilingual expertise, hands-on implementation, no-BS approach\n\n**Deliverable:** 2-3 sentence elevator pitch"
                    },
                    {
                        "name": "Target Customer Personas (2-3)",
                        "desc": "**Priority: CRITICAL**\n\nDefine ideal customer profiles:\n1. Growing SaaS startup (10-50 employees)\n2. E-commerce business expanding internationally\n3. Service business needing multilingual support\n\nFor each define:\n? Pain points\n? Goals\n? Budget range\n? Decision makers\n? Where they hang out\n\n**Deliverable:** 3 one-page persona documents"
                    },
                    {
                        "name": "Core Service Packages (3-5)",
                        "desc": "**Priority: CRITICAL**\n\nDefine packages:\n\n1. **Customer Support Setup**\n   ? Zendesk/Intercom implementation\n   ? Help center build\n   ? Agent training\n   ? Timeline: 2-4 weeks\n\n2. **Automation & AI**\n   ? Chatbot deployment\n   ? Workflow automation\n   ? AI assistant setup\n   ? Timeline: 3-6 weeks\n\n3. **Digital Growth**\n   ? Website launch\n   ? SEO optimization\n   ? Content strategy\n   ? Timeline: 4-8 weeks\n\nFor each: scope, timeline, deliverables, what's included/excluded\n\n**Deliverable:** Service packages document"
                    },
                    {
                        "name": "Pricing Strategy & Tiers",
                        "desc": "**Priority: CRITICAL**\n\nSet pricing model:\n? Project-based: Fixed price for defined scope\n? Retainer: Monthly fee for ongoing support\n? Hourly: For ad-hoc work ($100-200/hr range)\n\nDefine tiers:\n? **Starter:** Small businesses ($3K-$8K)\n? **Professional:** Growing companies ($8K-$25K)\n? **Enterprise:** Custom (>$25K)\n\nConsider: Market rates, competitor pricing, costs, margins\n\n**Deliverable:** Pricing sheet (internal)"
                    },
                    {
                        "name": "Website Content Audit & Update",
                        "desc": "**Priority: CRITICAL**\n\nReview deployhelp.com:\n? Strong visual design\n? Multilingual (4 languages)\n? Clear service categories\n\nUpdate:\n? Ensure messaging aligns with brand voice\n? Add clear pricing indicators (starting from $X)\n? Update service descriptions to match packages\n? Verify contact forms work\n? Add portfolio/case studies section\n? Check mobile responsiveness\n\n**Deliverable:** Updated website"
                    },
                    {
                        "name": "Create 2-3 Case Studies / Portfolio",
                        "desc": "**Priority: CRITICAL**\n\nDocument past projects:\n\nFor each case study:\n? Client profile (anonymize if needed)\n? Challenge/problem they faced\n? Solution you implemented\n? Results & metrics (time saved, cost reduced, etc.)\n? Client testimonial quote\n? Technologies used\n? Before/after screenshots\n\nFormat for website portfolio page\n\n**Deliverable:** 2-3 published case studies on website"
                    }
                ]
            },
            {
                "name": "?? PHASE 2: Sales Materials (Week 3-4) ?",
                "cards": [
                    {
                        "name": "Sales Pitch Deck (5-10 slides)",
                        "desc": "**Priority: HIGH**\n\nCreate presentation:\n1. Problem (customer support challenges)\n2. Solution (DeployHelp services)\n3. How it works (our process)\n4. Case studies (results)\n5. Services & pricing overview\n6. Why us (multilingual, hands-on, transparent)\n7. Next steps\n\nDesign: Match website branding (neo-brutalist style)\nFormats: PDF, PowerPoint, Google Slides\n\n**Deliverable:** Pitch deck in 3 formats"
                    },
                    {
                        "name": "One-Pager / Service Sheet",
                        "desc": "**Priority: HIGH**\n\nSingle-page PDF overview:\n? Company intro (2-3 sentences)\n? Services list with brief descriptions\n? Key benefits (multilingual, hands-on, results)\n? Client types we serve\n? Languages supported (EN, AM, RU, UA)\n? Contact info\n? Starting prices\n\nUse cases: Email attachment, LinkedIn message, quick reference\n\n**Deliverable:** Designed one-pager PDF"
                    },
                    {
                        "name": "Cold Outreach Email Templates (5)",
                        "desc": "**Priority: HIGH**\n\nCreate templates:\n\n1. **Initial contact email**\n   ? 5 subject line variations\n   ? Personalized intro\n   ? Value proposition\n   ? Social proof\n   ? Clear CTA\n\n2. **Follow-up sequence**\n   ? Follow-up #1 (3 days later)\n   ? Follow-up #2 (7 days later)\n   ? Follow-up #3 (14 days later)\n\n3. **Meeting request**\n4. **Post-meeting follow-up**\n5. **Proposal follow-up**\n\n**Deliverable:** Email template document"
                    },
                    {
                        "name": "Proposal Template",
                        "desc": "**Priority: HIGH**\n\nCreate reusable proposal:\n\nSections:\n? Executive summary\n? Understanding of client needs\n? Proposed solution & approach\n? Scope of work (detailed)\n? Timeline & milestones\n? Deliverables checklist\n? Pricing & payment terms\n? About DeployHelp\n? Terms & conditions\n? Next steps\n\nTools: Google Docs template or PandaDoc\n\n**Deliverable:** Proposal template"
                    },
                    {
                        "name": "Contract / MSA Template",
                        "desc": "**Priority: HIGH**\n\nLegal templates (get lawyer review):\n\n? **Master Services Agreement (MSA)**\n? **Statement of Work (SOW) template**\n? **Non-Disclosure Agreement (NDA)**\n\nInclude:\n? Scope & deliverables\n? Payment terms (50% upfront, 50% on completion)\n? IP ownership (client owns deliverables)\n? Confidentiality\n? Liability limits\n? Termination clause\n\nSet up e-signature (DocuSign/HelloSign)\n\n**Deliverable:** Contract templates + e-signature workflow"
                    },
                    {
                        "name": "Target Customer List (50-100 companies)",
                        "desc": "**Priority: HIGH**\n\nBuild prospect list:\n\n**Criteria:**\n? Industry: SaaS, E-commerce, Services\n? Size: 10-200 employees\n? Growth stage: Series A-B or $1M-$50M revenue\n? Needs: Expanding support, going multilingual, automation\n? Geography: US, Canada, Europe\n\n**Research sources:**\n? LinkedIn Sales Navigator\n? Crunchbase\n? AngelList\n? Industry directories\n? Competitors' clients\n\n**Fields to track:**\nCompany, contact person, title, email, LinkedIn, phone, notes, status\n\n**Deliverable:** CRM/spreadsheet with 50-100 qualified prospects"
                    }
                ]
            },
            {
                "name": "?? PHASE 3: Operations (Week 5-6) ??",
                "cards": [
                    {
                        "name": "CRM Setup & Configuration",
                        "desc": "**Priority: MEDIUM**\n\nChoose and set up CRM:\n\n**Options:**\n? HubSpot (free tier - recommended)\n? Pipedrive\n? Copper\n? Airtable (custom)\n\n**Configure:**\n? Contact fields (company, role, pain points)\n? Deal stages: Lead ? Qualified ? Proposal ? Negotiation ? Closed Won/Lost\n? Email integration\n? Task/reminder automation\n? Reporting dashboards\n? Import target customer list\n\n**Deliverable:** Working CRM with initial prospects"
                    },
                    {
                        "name": "Client Onboarding Process",
                        "desc": "**Priority: MEDIUM**\n\nStandardize new client kickoff:\n\n**Steps:**\n1. Contract signed ? Send welcome email\n2. Schedule kickoff call (60 min)\n3. Send onboarding questionnaire\n4. Get access to client systems (credentials)\n5. Set up project in PM tool\n6. Create shared Slack/email channel\n7. Schedule regular check-ins (weekly)\n\n**Create:**\n? Welcome email template\n? Onboarding checklist\n? Kickoff meeting agenda\n? Client questionnaire (goals, constraints, success metrics)\n\n**Deliverable:** Onboarding playbook"
                    },
                    {
                        "name": "Project Management System",
                        "desc": "**Priority: MEDIUM**\n\nSet up PM tool:\n\n**Options:**\n? Trello (you're here!)\n? Asana\n? ClickUp\n? Monday.com\n\n**Create templates for:**\n? Zendesk implementation project\n? Chatbot setup project\n? Website launch project\n? Ongoing support board\n\n**Define:**\n? Standard task lists per service\n? Milestone templates\n? Client access levels (view only)\n? Status reporting format\n\n**Deliverable:** PM templates for each service"
                    },
                    {
                        "name": "Invoicing & Payment Setup",
                        "desc": "**Priority: MEDIUM**\n\nSet up billing:\n\n**Invoicing tool:**\n? FreshBooks\n? Wave (free)\n? QuickBooks\n\n**Set up:**\n? Invoice template (branded)\n? Payment methods: Bank transfer, Stripe, PayPal\n? Payment terms: 50% upfront, 50% on delivery\n? Late payment reminders (auto)\n? Expense tracking\n? Financial reporting\n\n**Tax/Legal:**\n? Sales tax setup (if applicable)\n? International payment handling\n\n**Deliverable:** Invoicing system ready to use"
                    },
                    {
                        "name": "Service Delivery Playbooks",
                        "desc": "**Priority: MEDIUM**\n\nStep-by-step guides for each service:\n\n**1. Zendesk Implementation Playbook**\n   ? Pre-kickoff checklist\n   ? Discovery questions\n   ? Setup steps (routing, macros, reporting)\n   ? Testing checklist\n   ? Training outline\n   ? Handoff documentation template\n\n**2. Chatbot Setup Playbook**\n**3. Help Center Build Playbook**\n**4. Website Launch Playbook**\n\nGoal: Any team member can deliver consistent service\n\n**Deliverable:** 4 playbooks in Notion/Confluence"
                    }
                ]
            },
            {
                "name": "?? PHASE 4: Digital Optimization (Ongoing) ??",
                "cards": [
                    {
                        "name": "LinkedIn Company Page Setup",
                        "desc": "**Priority: LOW**\n\nSet up LinkedIn presence:\n? Create/optimize company page\n? Add company description (based on brand voice)\n? Add logo and banner (use website colors)\n? List services\n? Add website link\n? Post launch announcement\n\n**Content strategy:**\n? Share case studies\n? Industry insights\n? Tips & best practices (customer support)\n? Behind-the-scenes\n\nGoal: 2-3 posts per week\n\n**Deliverable:** Active LinkedIn page with 5+ posts"
                    },
                    {
                        "name": "Personal LinkedIn Profile Updates",
                        "desc": "**Priority: LOW**\n\nUpdate team profiles:\n? Add DeployHelp LLC to experience\n? Update headline to include DeployHelp\n? Add services/specialties\n? Ensure consistency with company branding\n? Connect with target customers\n? Engage with industry content\n? Ask satisfied clients for recommendations\n\n**Deliverable:** Optimized LinkedIn profiles"
                    },
                    {
                        "name": "SEO Optimization",
                        "desc": "**Priority: LOW**\n\n**Technical SEO:**\n? Meta descriptions for all pages\n? Alt text for images\n? Schema markup (LocalBusiness, Service, FAQPage)\n? XML sitemap (already exists ?)\n? Robots.txt\n? Page speed optimization\n\n**Keyword targeting:**\n? Zendesk implementation\n? Customer support consulting\n? Multilingual customer support\n? Chatbot setup\n? Business automation\n\n**Content:**\n? Add blog/resources section\n? Write 3-5 initial articles\n\n**Deliverable:** Optimized website with blog"
                    },
                    {
                        "name": "Lead Magnet / Free Resource",
                        "desc": "**Priority: LOW**\n\nCreate valuable free resource:\n\n**Options:**\n? 'Zendesk Implementation Checklist'\n? 'Chatbot Setup Guide'\n? 'Multilingual Support Playbook'\n? 'Customer Support Automation Toolkit'\n? 'Help Center Content Templates'\n\nFormat: PDF download (10-15 pages, branded)\nGate with email form (add to email list)\nPromote on website & LinkedIn\n\n**Deliverable:** Lead magnet + landing page"
                    },
                    {
                        "name": "Social Media Content Calendar",
                        "desc": "**Priority: LOW**\n\nPlan 1 month of content:\n\n**Content types:**\n? Tips & best practices (customer support)\n? Case study highlights\n? Industry news commentary\n? Behind-the-scenes\n? Client testimonials (with permission)\n? Service spotlights\n? Tool recommendations\n\n**Schedule:**\n? LinkedIn: 3x/week\n? Twitter: 5x/week (optional)\n\nUse scheduling tool: Buffer, Hootsuite, or Later\n\n**Deliverable:** 30-day content calendar"
                    },
                    {
                        "name": "Partnership & Referral Strategy",
                        "desc": "**Priority: LOW**\n\nIdentify partnership opportunities:\n\n**Potential partners:**\n? Web design agencies (we do support setup)\n? Marketing agencies (we handle customer comms)\n? Zendesk/Intercom resellers (implementation partner)\n? Business coaches/consultants (referrals)\n? Dev shops (complementary services)\n\n**Create:**\n? Partner one-pager\n? Referral incentive program (10-20% commission)\n? Co-marketing opportunities\n? Joint webinar ideas\n\n**Deliverable:** Partnership outreach plan"
                    }
                ]
            },
            {
                "name": "? COMPLETED",
                "cards": []
            },
            {
                "name": "?? BLOCKED / ON HOLD",
                "cards": []
            },
            {
                "name": "?? NOTES & IDEAS",
                "cards": []
            }
        ]
    }

def main():
    print("=" * 80)
    print("?? CREATING DEPLOYHELP LLC TRELLO BOARD")
    print("=" * 80)
    
    structure = get_structure()
    
    # Create board
    print(f"\n?? Creating board: {structure['board']['name']}")
    board = create_board(structure['board']['name'], structure['board']['description'])
    print(f"? Board created: {board['url']}")
    print(f"   ID: {board['id']}")
    
    # Delete default lists
    print("\n???  Removing default lists...")
    url = f"{BASE_URL}/boards/{board['id']}/lists"
    response = requests.get(url, params=get_auth_params())
    default_lists = response.json()
    for lst in default_lists:
        requests.put(f"{BASE_URL}/lists/{lst['id']}/closed", params={**get_auth_params(), "value": "true"})
    
    # Create lists and cards
    total_cards = 0
    for list_config in structure['lists']:
        print(f"\n?? Creating list: {list_config['name']}")
        lst = create_list(board['id'], list_config['name'])
        print(f"   ? List created")
        
        for card_config in list_config['cards']:
            print(f"      ? {card_config['name']}")
            create_card(lst['id'], card_config['name'], card_config.get('desc', ''))
            total_cards += 1
    
    print("\n" + "=" * 80)
    print("? BOARD CREATION COMPLETE!")
    print("=" * 80)
    print(f"\n?? Summary:")
    print(f"   ? Board: {structure['board']['name']}")
    print(f"   ? Lists: {len(structure['lists'])}")
    print(f"   ? Cards: {total_cards}")
    print(f"\n?? Open your board:")
    print(f"   {board['url']}")
    print("\n?? Start with PHASE 1 tasks (first 7 cards)")
    print("   Complete those before moving to Phase 2!")
    print("\n" + "=" * 80)
    
    # Save result
    result = {
        "board": board,
        "url": board['url'],
        "lists": len(structure['lists']),
        "cards": total_cards
    }
    
    with open('/workspace/trello_board_created.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("?? Details saved to: trello_board_created.json")

if __name__ == "__main__":
    main()
