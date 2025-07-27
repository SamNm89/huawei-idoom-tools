#!/usr/bin/env python3
"""
Quick script to apply your specific LTE band configuration
"""

from ai_agent import AIAutomationAgent
from config import ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD
from colorama import init, Fore, Style

# Initialize colorama
init()

def apply_your_band_config():
    """Apply your specific band configuration"""
    print(f"{Fore.CYAN}🚀 Applying your LTE band configuration...{Style.RESET_ALL}")
    
    # Your specific configuration
    your_config = {
        'Band3': True,
        'Band7': False,
        'Band20': False,
        'Band8': False
    }
    
    print(f"{Fore.YELLOW}Configuration to apply: {your_config}{Style.RESET_ALL}")
    
    try:
        # Initialize agent
        agent = AIAutomationAgent(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD)
        print(f"{Fore.GREEN}✅ Agent initialized{Style.RESET_ALL}")
        
        # Authenticate
        if agent.authenticate():
            print(f"{Fore.GREEN}✅ Authentication successful{Style.RESET_ALL}")
            
            # Apply your configuration
            success = agent.set_band_configuration(your_config)
            
            if success:
                print(f"{Fore.GREEN}🎉 Your band configuration applied successfully!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Enabled bands: Band3{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Disabled bands: Band7, Band20, Band8{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Failed to apply band configuration{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Authentication failed{Style.RESET_ALL}")
        
        # Cleanup
        agent.cleanup()
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    apply_your_band_config() 