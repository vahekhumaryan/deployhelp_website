#!/usr/bin/env python3
"""
Trello Workspace Organizer for DeployHelp LLC
Organizes boards, lists, and cards for pre-launch brand consistency
"""

import requests
import json
from typing import Dict, List, Optional

class TrelloOrganizer:
    def __init__(self, api_key: str, token: Optional[str] = None):
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.trello.com/1"
        
    def get_auth_params(self) -> Dict[str, str]:
        """Get authentication parameters for API requests"""
        params = {"key": self.api_key}
        if self.token:
            params["token"] = self.token
        return params
    
    def get_token_url(self) -> str:
        """Generate URL for user to get token"""
        return f"https://trello.com/1/authorize?expiration=never&name=DeployHelp+Organizer&scope=read,write&response_type=token&key={self.api_key}"
    
    def get_member_info(self) -> Optional[Dict]:
        """Get current member information"""
        try:
            url = f"{self.base_url}/members/me"
            response = requests.get(url, params=self.get_auth_params())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting member info: {e}")
            return None
    
    def get_organizations(self) -> List[Dict]:
        """Get all organizations/workspaces"""
        try:
            url = f"{self.base_url}/members/me/organizations"
            response = requests.get(url, params=self.get_auth_params())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting organizations: {e}")
            return []
    
    def get_boards(self, org_id: Optional[str] = None) -> List[Dict]:
        """Get all boards (optionally filtered by organization)"""
        try:
            if org_id:
                url = f"{self.base_url}/organizations/{org_id}/boards"
            else:
                url = f"{self.base_url}/members/me/boards"
            response = requests.get(url, params=self.get_auth_params())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting boards: {e}")
            return []
    
    def get_lists(self, board_id: str) -> List[Dict]:
        """Get all lists in a board"""
        try:
            url = f"{self.base_url}/boards/{board_id}/lists"
            response = requests.get(url, params=self.get_auth_params())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting lists: {e}")
            return []
    
    def get_cards(self, board_id: str) -> List[Dict]:
        """Get all cards in a board"""
        try:
            url = f"{self.base_url}/boards/{board_id}/cards"
            response = requests.get(url, params=self.get_auth_params())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting cards: {e}")
            return []
    
    def create_board(self, name: str, desc: str = "", org_id: Optional[str] = None) -> Optional[Dict]:
        """Create a new board"""
        try:
            url = f"{self.base_url}/boards/"
            params = self.get_auth_params()
            params["name"] = name
            params["desc"] = desc
            if org_id:
                params["idOrganization"] = org_id
            response = requests.post(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating board: {e}")
            return None
    
    def create_list(self, board_id: str, name: str, pos: str = "bottom") -> Optional[Dict]:
        """Create a new list in a board"""
        try:
            url = f"{self.base_url}/lists"
            params = self.get_auth_params()
            params["name"] = name
            params["idBoard"] = board_id
            params["pos"] = pos
            response = requests.post(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating list: {e}")
            return None
    
    def create_card(self, list_id: str, name: str, desc: str = "", pos: str = "bottom") -> Optional[Dict]:
        """Create a new card in a list"""
        try:
            url = f"{self.base_url}/cards"
            params = self.get_auth_params()
            params["name"] = name
            params["desc"] = desc
            params["idList"] = list_id
            params["pos"] = pos
            response = requests.post(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating card: {e}")
            return None
    
    def analyze_workspace(self) -> Dict:
        """Analyze current workspace structure"""
        print("\n?? ANALYZING CURRENT TRELLO WORKSPACE...\n")
        
        # Get member info
        member = self.get_member_info()
        if not member:
            return {"error": "Could not authenticate. Please check your API key and token."}
        
        print(f"? Authenticated as: {member.get('fullName', 'Unknown')} (@{member.get('username', 'unknown')})")
        
        # Get organizations
        orgs = self.get_organizations()
        print(f"\n?? Organizations: {len(orgs)}")
        for org in orgs:
            print(f"  - {org['displayName']} (ID: {org['id']})")
        
        # Get all boards
        boards = self.get_boards()
        print(f"\n?? Total Boards: {len(boards)}")
        
        workspace_data = {
            "member": member,
            "organizations": orgs,
            "boards": []
        }
        
        for board in boards:
            print(f"\n  ?? {board['name']}")
            print(f"     ID: {board['id']}")
            print(f"     URL: {board['url']}")
            
            # Get lists
            lists = self.get_lists(board['id'])
            print(f"     Lists: {len(lists)}")
            
            # Get cards
            cards = self.get_cards(board['id'])
            print(f"     Cards: {len(cards)}")
            
            board_data = {
                "board": board,
                "lists": lists,
                "cards": cards
            }
            workspace_data["boards"].append(board_data)
            
            # Show list details
            for lst in lists:
                list_cards = [c for c in cards if c['idList'] == lst['id']]
                print(f"       ? {lst['name']}: {len(list_cards)} cards")
        
        return workspace_data
    
    def design_structure(self) -> Dict:
        """Design the recommended Trello structure for DeployHelp pre-launch"""
        return {
            "boards": [
                {
                    "name": "?? Brand & Positioning",
                    "description": "Define DeployHelp's brand identity, messaging, and market positioning before outreach",
                    "lists": [
                        {
                            "name": "?? To Define",
                            "cards": [
                                {"name": "Brand Voice & Tone Guidelines", "desc": "Document how we communicate: friendly but professional, technical but accessible"},
                                {"name": "Value Proposition Refinement", "desc": "Clear statement: What we do, who we serve, why we're different"},
                                {"name": "Target Customer Personas", "desc": "Define 2-3 ideal customer profiles with pain points and goals"},
                                {"name": "Competitive Positioning", "desc": "How we differentiate from other consulting/implementation services"},
                                {"name": "Brand Visual Guidelines", "desc": "Colors, fonts, logo usage, imagery style"},
                            ]
                        },
                        {
                            "name": "?? In Progress",
                            "cards": []
                        },
                        {
                            "name": "? Approved",
                            "cards": []
                        }
                    ]
                },
                {
                    "name": "?? Service Offerings",
                    "description": "Clarify and standardize what we offer, pricing, and packaging",
                    "lists": [
                        {
                            "name": "?? To Structure",
                            "cards": [
                                {"name": "Core Service Packages", "desc": "Define 3-5 clear service packages (e.g., Zendesk Implementation, Chatbot Setup, etc.)"},
                                {"name": "Pricing Strategy", "desc": "Set pricing tiers, hourly rates, or project-based pricing"},
                                {"name": "Service Descriptions", "desc": "Write clear descriptions for each offering (what's included, timeline, deliverables)"},
                                {"name": "Case Studies & Portfolio", "desc": "Document 2-3 past projects with results and testimonials"},
                                {"name": "Service Process Flow", "desc": "Map out client journey from first contact to project completion"},
                                {"name": "Add-on Services", "desc": "Define optional extras (training, ongoing support, custom integrations)"},
                            ]
                        },
                        {
                            "name": "?? In Review",
                            "cards": []
                        },
                        {
                            "name": "? Finalized",
                            "cards": []
                        }
                    ]
                },
                {
                    "name": "?? Digital Presence",
                    "description": "Website, social media, and online materials that represent the brand",
                    "lists": [
                        {
                            "name": "?? To Launch",
                            "cards": [
                                {"name": "Website Content Audit", "desc": "Review deployhelp.com - ensure messaging aligns with brand guidelines"},
                                {"name": "SEO Optimization", "desc": "Meta descriptions, keywords, schema markup for customer support consulting"},
                                {"name": "LinkedIn Company Page", "desc": "Set up and optimize company profile with consistent messaging"},
                                {"name": "LinkedIn Personal Profiles", "desc": "Update team profiles to reflect DeployHelp branding"},
                                {"name": "Portfolio Page", "desc": "Create case studies page on website"},
                                {"name": "Contact & Lead Forms", "desc": "Ensure clear CTAs and working contact forms"},
                            ]
                        },
                        {
                            "name": "?? In Progress",
                            "cards": []
                        },
                        {
                            "name": "? Live",
                            "cards": []
                        }
                    ]
                },
                {
                    "name": "?? Marketing & Outreach",
                    "description": "Prepare marketing materials and outreach strategy",
                    "lists": [
                        {
                            "name": "?? To Create",
                            "cards": [
                                {"name": "Email Templates", "desc": "Cold outreach, intro meeting follow-up, proposal, onboarding"},
                                {"name": "Pitch Deck", "desc": "5-10 slide deck for initial meetings"},
                                {"name": "One-Pager", "desc": "PDF overview of services for quick sharing"},
                                {"name": "Social Media Content Calendar", "desc": "Plan 1 month of posts about customer support best practices"},
                                {"name": "Lead Magnet", "desc": "Free guide or checklist (e.g., 'Zendesk Implementation Checklist')"},
                                {"name": "Outreach Target List", "desc": "List of 50-100 companies that match ideal customer profile"},
                            ]
                        },
                        {
                            "name": "?? Drafting",
                            "cards": []
                        },
                        {
                            "name": "? Ready to Send",
                            "cards": []
                        }
                    ]
                },
                {
                    "name": "?? Operations & Tools",
                    "description": "Internal processes and systems to support the business",
                    "lists": [
                        {
                            "name": "?? To Set Up",
                            "cards": [
                                {"name": "CRM Setup", "desc": "Configure system for tracking leads and opportunities"},
                                {"name": "Proposal Templates", "desc": "Create reusable templates for project proposals"},
                                {"name": "Contract Templates", "desc": "Legal templates for service agreements"},
                                {"name": "Onboarding Process", "desc": "Document steps for new client kickoff"},
                                {"name": "Project Management System", "desc": "Set up standard project workflows"},
                                {"name": "Time Tracking & Invoicing", "desc": "Tool selection and setup for billing"},
                            ]
                        },
                        {
                            "name": "?? In Progress",
                            "cards": []
                        },
                        {
                            "name": "? Operational",
                            "cards": []
                        }
                    ]
                },
                {
                    "name": "?? Knowledge & Training",
                    "description": "Internal knowledge base and team training",
                    "lists": [
                        {
                            "name": "?? To Document",
                            "cards": [
                                {"name": "Service Delivery Playbooks", "desc": "Step-by-step guides for each service offering"},
                                {"name": "Best Practices Library", "desc": "Collection of Zendesk, Intercom, automation best practices"},
                                {"name": "Common Objections & Responses", "desc": "Sales training document"},
                                {"name": "Client FAQ", "desc": "Anticipate and answer common client questions"},
                                {"name": "Technical Documentation", "desc": "Integration guides, API documentation, etc."},
                            ]
                        },
                        {
                            "name": "?? Writing",
                            "cards": []
                        },
                        {
                            "name": "? Complete",
                            "cards": []
                        }
                    ]
                }
            ]
        }
    
    def create_organized_structure(self, org_id: Optional[str] = None, dry_run: bool = True) -> Dict:
        """Create the organized board structure"""
        structure = self.design_structure()
        results = {"created_boards": [], "errors": []}
        
        print("\n???  CREATING ORGANIZED WORKSPACE STRUCTURE...\n")
        
        if dry_run:
            print("?? DRY RUN MODE - No actual changes will be made\n")
        
        for board_config in structure["boards"]:
            print(f"\n?? Board: {board_config['name']}")
            print(f"   Description: {board_config['description']}")
            
            if not dry_run:
                # Create board
                board = self.create_board(
                    name=board_config['name'],
                    desc=board_config['description'],
                    org_id=org_id
                )
                
                if not board:
                    results["errors"].append(f"Failed to create board: {board_config['name']}")
                    continue
                
                print(f"   ? Created board: {board['url']}")
                board_result = {"board": board, "lists": []}
                
                # Create lists
                for list_config in board_config['lists']:
                    print(f"     ? List: {list_config['name']}")
                    lst = self.create_list(board['id'], list_config['name'])
                    
                    if not lst:
                        results["errors"].append(f"Failed to create list: {list_config['name']}")
                        continue
                    
                    list_result = {"list": lst, "cards": []}
                    
                    # Create cards
                    for card_config in list_config['cards']:
                        print(f"        ? Card: {card_config['name']}")
                        card = self.create_card(
                            lst['id'],
                            card_config['name'],
                            card_config.get('desc', '')
                        )
                        
                        if card:
                            list_result["cards"].append(card)
                        else:
                            results["errors"].append(f"Failed to create card: {card_config['name']}")
                    
                    board_result["lists"].append(list_result)
                
                results["created_boards"].append(board_result)
            else:
                # Dry run - just show what would be created
                for list_config in board_config['lists']:
                    print(f"     ? List: {list_config['name']}")
                    for card_config in list_config['cards']:
                        print(f"        ? Card: {card_config['name']}")
        
        return results


def main():
    """Main function to organize Trello workspace"""
    print("=" * 80)
    print("?? DEPLOYHELP LLC - TRELLO WORKSPACE ORGANIZER")
    print("=" * 80)
    
    # Initialize with API key
    API_KEY = "2ff6b8c648075cb0239fba4fa84f9e84"
    organizer = TrelloOrganizer(API_KEY)
    
    # Check if we have a token
    print("\n??  AUTHENTICATION REQUIRED")
    print("\nTo access your Trello workspace, you need to authorize this application.")
    print(f"\n?? Please visit this URL to get your token:\n")
    print(f"{organizer.get_token_url()}\n")
    
    token = input("Enter your Trello token (or press Enter to skip): ").strip()
    
    if token:
        organizer.token = token
        
        # Analyze current workspace
        workspace_data = organizer.analyze_workspace()
        
        if "error" not in workspace_data:
            # Save analysis
            with open('/workspace/trello_analysis.json', 'w') as f:
                json.dump(workspace_data, f, indent=2)
            print("\n?? Workspace analysis saved to: trello_analysis.json")
            
            # Show recommended structure
            print("\n" + "=" * 80)
            print("?? RECOMMENDED WORKSPACE STRUCTURE")
            print("=" * 80)
            
            structure = organizer.design_structure()
            print(f"\n?? Boards to create: {len(structure['boards'])}")
            for board in structure['boards']:
                print(f"\n  ?? {board['name']}")
                print(f"     {board['description']}")
                print(f"     Lists: {len(board['lists'])}")
                total_cards = sum(len(lst['cards']) for lst in board['lists'])
                print(f"     Cards: {total_cards}")
            
            # Ask if user wants to create structure
            print("\n" + "=" * 80)
            create = input("\n?? Would you like to create this structure? (yes/no): ").strip().lower()
            
            if create in ['yes', 'y']:
                # Get organization ID if any
                org_id = None
                if workspace_data.get('organizations'):
                    print("\n?? Available Organizations:")
                    for i, org in enumerate(workspace_data['organizations']):
                        print(f"  {i+1}. {org['displayName']} (ID: {org['id']})")
                    
                    org_choice = input("\nCreate boards in organization? (enter number or skip): ").strip()
                    if org_choice.isdigit():
                        org_idx = int(org_choice) - 1
                        if 0 <= org_idx < len(workspace_data['organizations']):
                            org_id = workspace_data['organizations'][org_idx]['id']
                
                # Create structure
                results = organizer.create_organized_structure(org_id=org_id, dry_run=False)
                
                print("\n" + "=" * 80)
                print("? WORKSPACE ORGANIZATION COMPLETE!")
                print("=" * 80)
                print(f"\n?? Boards created: {len(results['created_boards'])}")
                if results['errors']:
                    print(f"\n??  Errors encountered: {len(results['errors'])}")
                    for error in results['errors']:
                        print(f"   - {error}")
                
                # Save results
                with open('/workspace/trello_results.json', 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                print("\n?? Results saved to: trello_results.json")
            else:
                print("\n?? Showing recommended structure only (dry run)")
                organizer.create_organized_structure(dry_run=True)
        else:
            print(f"\n? {workspace_data['error']}")
    else:
        print("\n??  No token provided. Showing recommended structure only:\n")
        structure = organizer.design_structure()
        
        print("=" * 80)
        print("?? RECOMMENDED PRE-LAUNCH WORKSPACE STRUCTURE")
        print("=" * 80)
        
        for board in structure['boards']:
            print(f"\n{'='*80}")
            print(f"?? {board['name']}")
            print(f"{'='*80}")
            print(f"{board['description']}\n")
            
            for lst in board['lists']:
                print(f"  ?? {lst['name']}")
                for card in lst['cards']:
                    print(f"     ? {card['name']}")
                    if card['desc']:
                        desc_lines = card['desc'].split('\n')
                        for line in desc_lines:
                            print(f"        {line}")
                print()


if __name__ == "__main__":
    main()
