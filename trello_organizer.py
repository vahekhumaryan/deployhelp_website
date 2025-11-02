#!/usr/bin/env python3
"""
Trello Workspace Organizer for DeployHelp LLC
Organizes Trello workspace for brand consistency and pre-launch preparation
"""

import requests
import json
import sys
from typing import Dict, List, Optional

class TrelloOrganizer:
    def __init__(self, api_key: str, api_token: str):
        self.api_key = api_key
        self.api_token = api_token
        self.base_url = "https://api.trello.com/1"
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make API request to Trello"""
        url = f"{self.base_url}{endpoint}"
        params = kwargs.get('params', {})
        params.update({
            'key': self.api_key,
            'token': self.api_token
        })
        
        response = requests.request(method, url, params=params, json=kwargs.get('json'))
        response.raise_for_status()
        return response.json()
    
    def get_boards(self) -> List[Dict]:
        """Get all boards"""
        return self._make_request('GET', '/members/me/boards')
    
    def create_board(self, name: str, description: str = "", default_lists: bool = True) -> Dict:
        """Create a new board"""
        params = {
            'name': name,
            'desc': description,
            'defaultLists': 'true' if default_lists else 'false'
        }
        return self._make_request('POST', '/boards', params=params)
    
    def get_lists(self, board_id: str) -> List[Dict]:
        """Get all lists in a board"""
        return self._make_request('GET', f'/boards/{board_id}/lists')
    
    def create_list(self, board_id: str, name: str, pos: str = 'bottom') -> Dict:
        """Create a new list"""
        params = {
            'name': name,
            'idBoard': board_id,
            'pos': pos
        }
        return self._make_request('POST', '/lists', params=params)
    
    def create_card(self, list_id: str, name: str, desc: str = "", pos: str = 'bottom') -> Dict:
        """Create a new card"""
        params = {
            'name': name,
            'idList': list_id,
            'desc': desc,
            'pos': pos
        }
        return self._make_request('POST', '/cards', params=params)
    
    def add_checklist(self, card_id: str, name: str, items: List[str]) -> Dict:
        """Add a checklist to a card"""
        # Create checklist
        params = {'name': name, 'idCard': card_id}
        checklist = self._make_request('POST', '/checklists', params=params)
        
        # Add items
        checklist_id = checklist['id']
        for item in items:
            self._make_request('POST', f'/checklists/{checklist_id}/checkItems', 
                             params={'name': item})
        
        return checklist
    
    def find_or_create_board(self, name: str, description: str = "") -> Dict:
        """Find existing board or create new one"""
        boards = self.get_boards()
        for board in boards:
            if board['name'] == name:
                print(f"Found existing board: {name}")
                return board
        
        print(f"Creating new board: {name}")
        return self.create_board(name, description, default_lists=False)
    
    def find_or_create_list(self, board_id: str, name: str) -> Dict:
        """Find existing list or create new one"""
        lists = self.get_lists(board_id)
        for lst in lists:
            if lst['name'] == name:
                return lst
        
        return self.create_list(board_id, name)
    
    def organize_deployhelp_workspace(self):
        """Main method to organize DeployHelp workspace"""
        print("?? Organizing DeployHelp LLC Trello Workspace...")
        
        # Main workspace board
        main_board = self.find_or_create_board(
            "DeployHelp LLC - Brand & Launch Prep",
            "Organized workspace for brand consistency and pre-launch tasks before reaching out to businesses"
        )
        board_id = main_board['id']
        
        # Define the organization structure
        lists_structure = {
            "?? Brand Consistency & Identity": {
                "position": "top",
                "cards": [
                    {
                        "name": "Brand Guidelines Documentation",
                        "desc": "Create comprehensive brand guidelines document covering:\n- Logo usage and variations\n- Color palette (#ff5a3c, #2233ff, #ffe347, etc.)\n- Typography (Space Grotesk, IBM Plex Mono)\n- Voice and tone guidelines\n- Visual style guide",
                        "checklist": [
                            "Document primary brand colors",
                            "Document accent colors",
                            "Create logo usage guidelines",
                            "Define typography hierarchy",
                            "Document voice and tone",
                            "Create brand asset library",
                            "Review website for consistency"
                        ]
                    },
                    {
                        "name": "Messaging & Value Proposition Review",
                        "desc": "Ensure consistent messaging across all touchpoints:\n- Website copy consistency\n- Service descriptions alignment\n- Value proposition clarity\n- Multi-language consistency (EN, AM, RU, UA)",
                        "checklist": [
                            "Review hero section messaging",
                            "Verify service descriptions match offerings",
                            "Check value proposition clarity",
                            "Review multilingual translations",
                            "Audit call-to-action consistency",
                            "Ensure tagline consistency"
                        ]
                    },
                    {
                        "name": "Service Offering Consistency",
                        "desc": "Verify all service offerings are clearly defined and consistent:\n- Customer Support services\n- Automation & AI services\n- Digital Growth services",
                        "checklist": [
                            "Document Customer Support offerings",
                            "Document Automation & AI offerings",
                            "Document Digital Growth offerings",
                            "Create service packages/pricing structure",
                            "Ensure service descriptions are clear",
                            "Review website service sections"
                        ]
                    },
                    {
                        "name": "Legal & Compliance Review",
                        "desc": "Ensure all legal and compliance requirements are met",
                        "checklist": [
                            "Review LLC formation documents",
                            "Verify business registration",
                            "Check email domain (deployhelp.com) setup",
                            "Review privacy policy needs",
                            "Check terms of service requirements",
                            "Verify trademark usage"
                        ]
                    }
                ]
            },
            "?? Content & Website": {
                "cards": [
                    {
                        "name": "Website Content Audit",
                        "desc": "Review and optimize website content for consistency",
                        "checklist": [
                            "Review all service descriptions",
                            "Check FAQ consistency across languages",
                            "Verify contact information accuracy",
                            "Review meta descriptions and SEO tags",
                            "Check schema markup accuracy",
                            "Verify all links work correctly"
                        ]
                    },
                    {
                        "name": "SEO Optimization",
                        "desc": "Ensure website is optimized for search engines",
                        "checklist": [
                            "Review meta tags consistency",
                            "Check structured data (JSON-LD)",
                            "Verify sitemap.xml",
                            "Review canonical URLs",
                            "Check page speed optimization",
                            "Review keyword strategy"
                        ]
                    },
                    {
                        "name": "Multi-language Content Review",
                        "desc": "Ensure content quality across all languages (EN, AM, RU, UA)",
                        "checklist": [
                            "Review English content",
                            "Review Armenian translations",
                            "Review Russian translations",
                            "Review Ukrainian translations",
                            "Verify cultural appropriateness",
                            "Check terminology consistency"
                        ]
                    },
                    {
                        "name": "Case Studies & Portfolio",
                        "desc": "Prepare case studies and portfolio examples",
                        "checklist": [
                            "Identify client stories to feature",
                            "Create case study templates",
                            "Gather project screenshots/examples",
                            "Document success metrics",
                            "Prepare anonymized examples"
                        ]
                    }
                ]
            },
            "?? Pre-Launch Business Prep": {
                "cards": [
                    {
                        "name": "Sales Process Definition",
                        "desc": "Define and document sales process",
                        "checklist": [
                            "Create discovery call script",
                            "Define qualification criteria",
                            "Create proposal templates",
                            "Set up CRM or tracking system",
                            "Define follow-up process",
                            "Create pricing documentation"
                        ]
                    },
                    {
                        "name": "Lead Generation Strategy",
                        "desc": "Plan how to reach out to potential clients",
                        "checklist": [
                            "Identify target market segments",
                            "Create ideal customer profile (ICP)",
                            "Research potential clients",
                            "Prepare outreach templates",
                            "Define referral program",
                            "Set up LinkedIn strategy"
                        ]
                    },
                    {
                        "name": "Contract & Legal Templates",
                        "desc": "Prepare legal templates for client engagements",
                        "checklist": [
                            "Create service agreement template",
                            "Prepare statement of work (SOW) template",
                            "Define payment terms",
                            "Create NDA template",
                            "Prepare project scope templates",
                            "Review with legal counsel"
                        ]
                    },
                    {
                        "name": "Pricing & Packages",
                        "desc": "Define service packages and pricing",
                        "checklist": [
                            "Research competitor pricing",
                            "Define service tiers",
                            "Create pricing documentation",
                            "Set up payment processing",
                            "Define package inclusions",
                            "Prepare pricing presentation"
                        ]
                    }
                ]
            },
            "??? Operations Setup": {
                "cards": [
                    {
                        "name": "Tools & Systems Setup",
                        "desc": "Set up necessary tools and systems",
                        "checklist": [
                            "Set up project management tool",
                            "Configure email system (contact@deployhelp.com)",
                            "Set up time tracking",
                            "Configure invoicing system",
                            "Set up file storage/sharing",
                            "Configure communication tools"
                        ]
                    },
                    {
                        "name": "Support Desk Templates",
                        "desc": "Prepare templates for Zendesk/Intercom implementations",
                        "checklist": [
                            "Create Zendesk setup checklist",
                            "Create Intercom setup checklist",
                            "Prepare macro templates",
                            "Create routing templates",
                            "Document best practices",
                            "Create handoff documentation"
                        ]
                    },
                    {
                        "name": "Automation Templates",
                        "desc": "Prepare automation templates and documentation",
                        "checklist": [
                            "Document automation use cases",
                            "Create automation templates",
                            "Prepare integration documentation",
                            "Create workflow diagrams",
                            "Document best practices"
                        ]
                    },
                    {
                        "name": "Knowledge Base & Documentation",
                        "desc": "Create internal knowledge base",
                        "checklist": [
                            "Set up documentation system",
                            "Create service documentation templates",
                            "Document internal processes",
                            "Create client onboarding materials",
                            "Prepare training materials"
                        ]
                    }
                ]
            },
            "?? Marketing & Outreach": {
                "cards": [
                    {
                        "name": "Marketing Materials",
                        "desc": "Create marketing materials for outreach",
                        "checklist": [
                            "Create company one-pager",
                            "Design service brochures",
                            "Prepare email signature",
                            "Create LinkedIn company page",
                            "Prepare social media content",
                            "Create presentation deck"
                        ]
                    },
                    {
                        "name": "Content Marketing Strategy",
                        "desc": "Plan content marketing approach",
                        "checklist": [
                            "Define content calendar",
                            "Identify blog topics",
                            "Plan case study releases",
                            "Create social media strategy",
                            "Plan newsletter content",
                            "Define content distribution"
                        ]
                    },
                    {
                        "name": "Networking & Partnerships",
                        "desc": "Build network and partnerships",
                        "checklist": [
                            "Identify partner opportunities",
                            "Join relevant communities",
                            "Plan conference attendance",
                            "Identify speaking opportunities",
                            "Build referral network",
                            "Connect with complementary services"
                        ]
                    },
                    {
                        "name": "Testimonials & Social Proof",
                        "desc": "Gather testimonials and social proof",
                        "checklist": [
                            "Request testimonials from past clients",
                            "Gather LinkedIn recommendations",
                            "Create client success stories",
                            "Prepare testimonial page",
                            "Collect case study metrics"
                        ]
                    }
                ]
            },
            "? Ready to Launch": {
                "cards": [
                    {
                        "name": "Final Review Checklist",
                        "desc": "Complete final review before reaching out to businesses",
                        "checklist": [
                            "Brand consistency verified",
                            "All service offerings documented",
                            "Website content reviewed",
                            "Legal documents prepared",
                            "Sales process defined",
                            "Pricing finalized",
                            "Tools and systems configured",
                            "Marketing materials ready",
                            "Team briefed and ready"
                        ]
                    },
                    {
                        "name": "Launch Day Prep",
                        "desc": "Prepare for launch day activities",
                        "checklist": [
                            "Prepare outreach list",
                            "Schedule launch day activities",
                            "Prepare announcement content",
                            "Set up tracking/analytics",
                            "Prepare FAQ responses",
                            "Set up lead capture system"
                        ]
                    }
                ]
            }
        }
        
        # Create lists and cards
        print("\n?? Creating lists and cards...")
        for list_name, list_data in lists_structure.items():
            print(f"\n  Creating list: {list_name}")
            lst = self.find_or_create_list(board_id, list_name)
            list_id = lst['id']
            
            # Position the list if specified
            if 'position' in list_data:
                pos = 'top' if list_data['position'] == 'top' else 'bottom'
            
            # Create cards
            for card_data in list_data['cards']:
                print(f"    Creating card: {card_data['name']}")
                card = self.create_card(
                    list_id,
                    card_data['name'],
                    card_data.get('desc', ''),
                    pos='bottom'
                )
                
                # Add checklist if specified
                if 'checklist' in card_data:
                    print(f"      Adding checklist with {len(card_data['checklist'])} items")
                    self.add_checklist(card['id'], "Checklist", card_data['checklist'])
        
        print(f"\n? Workspace organized successfully!")
        print(f"?? Board URL: {main_board['url']}")
        return main_board


def main():
    """Main entry point"""
    api_key = "2ff6b8c648075cb0239fba4fa84f9e84"
    
    # Check if token is provided
    if len(sys.argv) > 1:
        api_token = sys.argv[1]
    else:
        print("? Trello API Token required!")
        print("\nTo get your token:")
        print("1. Visit: https://trello.com/app-key")
        print("2. Click 'Token' link")
        print("3. Authorize and copy the token")
        print(f"\nUsage: python trello_organizer.py <YOUR_API_TOKEN>")
        sys.exit(1)
    
    organizer = TrelloOrganizer(api_key, api_token)
    
    try:
        organizer.organize_deployhelp_workspace()
    except requests.exceptions.HTTPError as e:
        print(f"\n? Error: {e}")
        if e.response.status_code == 401:
            print("Authentication failed. Please check your API key and token.")
        sys.exit(1)
    except Exception as e:
        print(f"\n? Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
