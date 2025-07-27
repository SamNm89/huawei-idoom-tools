#!/usr/bin/env python3
"""
Main entry point for Huawei LTE Router AI Automation Agent
Provides command-line interface and interactive menu
"""

import sys
import os
import signal
import argparse
from datetime import datetime
import time
from colorama import init, Fore, Style, Back

from ai_agent import AIAutomationAgent
from config import ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD

# Initialize colorama
init()

class LTEAutomationApp:
    """Main application class for LTE automation"""
    
    def __init__(self):
        self.agent = None
        self.running = False
        
    def print_banner(self):
        """Print application banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    Huawei LTE Router AI Agent                        ║
║                    Signal Optimization & Monitoring                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def print_menu(self):
        """Print main menu options"""
        menu = f"""
{Fore.YELLOW}📡 LTE Automation Menu:{Style.RESET_ALL}

{Fore.CYAN}1.{Style.RESET_ALL}  Authenticate with router
{Fore.CYAN}2.{Style.RESET_ALL}  Test all LTE bands
{Fore.CYAN}3.{Style.RESET_ALL}  Start continuous monitoring
{Fore.CYAN}4.{Style.RESET_ALL}  Stop monitoring
{Fore.CYAN}5.{Style.RESET_ALL}  Generate performance report
{Fore.CYAN}6.{Style.RESET_ALL}  Optimize for peak hours
{Fore.CYAN}7.{Style.RESET_ALL}  Schedule automatic optimization
{Fore.CYAN}8.{Style.RESET_ALL}  View current status
{Fore.CYAN}9.{Style.RESET_ALL}  Manual band switch
{Fore.CYAN}10.{Style.RESET_ALL} Band configuration (client.net.set_lte_band)
{Fore.CYAN}11.{Style.RESET_ALL} View metrics summary
{Fore.CYAN}12.{Style.RESET_ALL} Export band comparison
{Fore.CYAN}13.{Style.RESET_ALL} Cleanup and exit

{Fore.GREEN}Enter your choice (1-13):{Style.RESET_ALL} """
        return input(menu)
    
    def initialize_agent(self, router_ip: str = None, username: str = None, password: str = None):
        """Initialize the AI agent"""
        try:
            self.agent = AIAutomationAgent(
                router_ip or ROUTER_IP,
                username or ROUTER_USERNAME,
                password or ROUTER_PASSWORD
            )
            print(f"{Fore.GREEN}✅ AI Agent initialized successfully{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to initialize AI Agent: {e}{Style.RESET_ALL}")
            return False
    
    def handle_authentication(self):
        """Handle router authentication"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}🔐 Attempting to authenticate with router...{Style.RESET_ALL}")
        success = self.agent.authenticate()
        
        if success:
            print(f"{Fore.GREEN}✅ Authentication successful!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Authentication failed. Check credentials and network connection.{Style.RESET_ALL}")
    
    def handle_band_testing(self):
        """Handle LTE band testing"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        try:
            duration = input(f"{Fore.CYAN}Enter test duration per band in seconds (default 300):{Style.RESET_ALL} ")
            duration = int(duration) if duration.strip() else 300
            
            print(f"{Fore.YELLOW}⚠️ This will test all available bands for {duration} seconds each.{Style.RESET_ALL}")
            confirm = input(f"{Fore.CYAN}Continue? (y/N):{Style.RESET_ALL} ")
            
            if confirm.lower() == 'y':
                results = self.agent.test_all_bands(duration)
                
                if results:
                    print(f"\n{Fore.GREEN}📊 Band Testing Results:{Style.RESET_ALL}")
                    for band, performance in results.items():
                        print(f"{Fore.CYAN}{band}:{Style.RESET_ALL}")
                        print(f"  Avg RSRP: {performance.avg_rsrp:.1f} dBm")
                        print(f"  Avg SINR: {performance.avg_sinr:.1f} dB")
                        print(f"  Bandwidth Score: {performance.avg_bandwidth_score:.3f}")
                        print(f"  Stability: {performance.stability_score:.3f}")
                        print()
                else:
                    print(f"{Fore.RED}❌ No band testing results available{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Band testing cancelled{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}❌ Invalid duration value{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error during band testing: {e}{Style.RESET_ALL}")
    
    def handle_monitoring(self, start: bool = True):
        """Handle monitoring start/stop"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        if start:
            try:
                interval = input(f"{Fore.CYAN}Enter monitoring interval in seconds (default 30):{Style.RESET_ALL} ")
                interval = int(interval) if interval.strip() else 30
                
                print(f"{Fore.CYAN}📊 Starting continuous monitoring...{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Press Ctrl+C to stop monitoring{Style.RESET_ALL}")
                
                self.agent.start_continuous_monitoring(interval)
                self.running = True
                
                # Keep the monitoring running
                try:
                    while self.running:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}🛑 Stopping monitoring...{Style.RESET_ALL}")
                    self.agent.stop_continuous_monitoring()
                    self.running = False
                    
            except ValueError:
                print(f"{Fore.RED}❌ Invalid interval value{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Error starting monitoring: {e}{Style.RESET_ALL}")
        else:
            self.agent.stop_continuous_monitoring()
            self.running = False
            print(f"{Fore.GREEN}✅ Monitoring stopped{Style.RESET_ALL}")
    
    def handle_report_generation(self):
        """Handle performance report generation"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        try:
            print(f"{Fore.CYAN}📊 Generating performance report...{Style.RESET_ALL}")
            report_file = self.agent.generate_performance_report()
            
            if report_file:
                print(f"{Fore.GREEN}✅ Report generated: {report_file}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Failed to generate report{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error generating report: {e}{Style.RESET_ALL}")
    
    def handle_peak_optimization(self):
        """Handle peak hour optimization"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        try:
            print(f"{Fore.CYAN}⏰ Running peak hour optimization...{Style.RESET_ALL}")
            self.agent.optimize_for_peak_hours()
            print(f"{Fore.GREEN}✅ Peak hour optimization completed{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error during peak optimization: {e}{Style.RESET_ALL}")
    
    def handle_scheduling(self):
        """Handle automatic scheduling"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        try:
            print(f"{Fore.CYAN}⏰ Setting up automatic optimization schedule...{Style.RESET_ALL}")
            self.agent.schedule_optimization()
            self.agent.run_scheduler()
            print(f"{Fore.GREEN}✅ Automatic optimization scheduled{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error setting up scheduling: {e}{Style.RESET_ALL}")
    
    def handle_status_view(self):
        """Handle current status view"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        try:
            metrics = self.agent.router.get_signal_metrics()
            if metrics:
                print(f"\n{Fore.GREEN}📡 Current Status:{Style.RESET_ALL}")
                print(f"Band: {metrics.band}")
                print(f"RSRP: {metrics.rsrp:.1f} dBm")
                print(f"RSRQ: {metrics.rsrq:.1f} dB")
                print(f"SINR: {metrics.sinr:.1f} dB")
                print(f"RSSI: {metrics.rssi:.1f} dBm")
                print(f"Cell ID: {metrics.cell_id}")
                print(f"PLMN: {metrics.plmn}")
                print(f"Timestamp: {metrics.timestamp}")
            else:
                print(f"{Fore.RED}❌ Unable to retrieve current status{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error getting status: {e}{Style.RESET_ALL}")
    
    def handle_manual_band_switch(self):
        """Handle manual band switching"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        try:
            print(f"{Fore.CYAN}Band switching options:{Style.RESET_ALL}")
            print(f"1. Switch to single band")
            print(f"2. Set band configuration (like client.net.set_lte_band)")
            
            choice = input(f"\n{Fore.CYAN}Select option (1-2):{Style.RESET_ALL} ")
            
            if choice == "1":
                # Single band switch
                available_bands = self.agent.router.get_available_bands()
                print(f"\n{Fore.CYAN}Available bands:{Style.RESET_ALL}")
                for i, band in enumerate(available_bands, 1):
                    print(f"{i}. {band}")
                
                band_choice = input(f"\n{Fore.CYAN}Select band number to switch to:{Style.RESET_ALL} ")
                try:
                    band_index = int(band_choice) - 1
                    if 0 <= band_index < len(available_bands):
                        selected_band = available_bands[band_index]
                        print(f"{Fore.CYAN}🔄 Switching to {selected_band}...{Style.RESET_ALL}")
                        
                        if self.agent.router.set_lte_band(selected_band):
                            print(f"{Fore.GREEN}✅ Successfully switched to {selected_band}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}❌ Failed to switch to {selected_band}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Invalid band selection{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}❌ Invalid input{Style.RESET_ALL}")
            
            elif choice == "2":
                # Band configuration
                print(f"\n{Fore.CYAN}Enter band configuration (True/False for each band):{Style.RESET_ALL}")
                print(f"Example: {{'Band3': True, 'Band7': False, 'Band20': False, 'Band8': False}}")
                
                config_input = input(f"\n{Fore.CYAN}Band configuration:{Style.RESET_ALL} ")
                try:
                    # Parse the configuration
                    import ast
                    band_config = ast.literal_eval(config_input)
                    
                    if isinstance(band_config, dict):
                        success = self.agent.set_band_configuration(band_config)
                        if success:
                            print(f"{Fore.GREEN}✅ Band configuration applied successfully{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}❌ Failed to apply band configuration{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ Invalid configuration format{Style.RESET_ALL}")
                except (ValueError, SyntaxError):
                    print(f"{Fore.RED}❌ Invalid configuration syntax{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Invalid choice{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error during band switch: {e}{Style.RESET_ALL}")
    
    def handle_band_configuration(self):
        """Handle band configuration operations"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        try:
            print(f"\n{Fore.CYAN}Band Configuration Options:{Style.RESET_ALL}")
            print(f"1. Get current band configuration")
            print(f"2. Set band configuration")
            print(f"3. Apply your specific configuration")
            
            choice = input(f"\n{Fore.CYAN}Select option (1-3):{Style.RESET_ALL} ")
            
            if choice == "1":
                # Get current configuration
                config = self.agent.get_current_band_config()
                if config:
                    print(f"{Fore.GREEN}✅ Current configuration retrieved{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}⚠️ No configuration data available{Style.RESET_ALL}")
            
            elif choice == "2":
                # Set custom configuration
                print(f"\n{Fore.CYAN}Enter band configuration:{Style.RESET_ALL}")
                config_input = input(f"Format: {{'Band3': True, 'Band7': False}}: ")
                try:
                    import ast
                    band_config = ast.literal_eval(config_input)
                    success = self.agent.set_band_configuration(band_config)
                except (ValueError, SyntaxError):
                    print(f"{Fore.RED}❌ Invalid configuration syntax{Style.RESET_ALL}")
            
            elif choice == "3":
                # Apply your specific configuration
                your_config = {
                    'Band3': True,
                    'Band7': False,
                    'Band20': False,
                    'Band8': False
                }
                print(f"{Fore.CYAN}Applying your specific configuration: {your_config}{Style.RESET_ALL}")
                success = self.agent.set_band_configuration(your_config)
                if success:
                    print(f"{Fore.GREEN}✅ Your configuration applied successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Failed to apply your configuration{Style.RESET_ALL}")
            
            else:
                print(f"{Fore.RED}❌ Invalid choice{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error during band configuration: {e}{Style.RESET_ALL}")
    
    def handle_metrics_summary(self):
        """Handle metrics summary view"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        try:
            hours = input(f"{Fore.CYAN}Enter hours to look back (default 24):{Style.RESET_ALL} ")
            hours = int(hours) if hours.strip() else 24
            
            summary = self.agent.data_logger.get_metrics_summary(hours)
            
            if summary:
                print(f"\n{Fore.GREEN}📊 Metrics Summary (Last {hours} hours):{Style.RESET_ALL}")
                print(f"Total records: {summary.get('total_records', 0)}")
                print(f"Bands tested: {', '.join(summary.get('bands_tested', []))}")
                
                if 'average_metrics' in summary:
                    avg = summary['average_metrics']
                    print(f"Average RSRP: {avg.get('rsrp', 0):.1f} dBm")
                    print(f"Average SINR: {avg.get('sinr', 0):.1f} dB")
                    print(f"Average bandwidth score: {avg.get('bandwidth_score', 0):.3f}")
                
                if 'best_performing_band' in summary:
                    print(f"Best performing band: {summary['best_performing_band']}")
                
                if 'signal_quality_distribution' in summary:
                    print(f"Signal quality distribution: {summary['signal_quality_distribution']}")
            else:
                print(f"{Fore.RED}❌ No metrics data available{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}❌ Invalid hours value{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error getting metrics summary: {e}{Style.RESET_ALL}")
    
    def handle_band_comparison_export(self):
        """Handle band comparison export"""
        if not self.agent:
            print(f"{Fore.RED}❌ Agent not initialized. Please initialize first.{Style.RESET_ALL}")
            return
        
        try:
            output_file = input(f"{Fore.CYAN}Enter output filename (default: band_comparison.csv):{Style.RESET_ALL} ")
            output_file = output_file if output_file.strip() else "band_comparison.csv"
            
            print(f"{Fore.CYAN}📊 Exporting band comparison data...{Style.RESET_ALL}")
            result = self.agent.data_logger.export_band_comparison(output_file)
            
            if result is not None:
                print(f"{Fore.GREEN}✅ Band comparison exported to {output_file}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Failed to export band comparison{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error exporting band comparison: {e}{Style.RESET_ALL}")
    
    def handle_cleanup(self):
        """Handle cleanup and exit"""
        if self.agent:
            print(f"{Fore.YELLOW}🧹 Cleaning up resources...{Style.RESET_ALL}")
            self.agent.cleanup()
        
        print(f"{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    
    def run_interactive(self):
        """Run the interactive menu"""
        self.print_banner()
        
        # Initialize agent
        print(f"{Fore.CYAN}🔧 Initializing AI Agent...{Style.RESET_ALL}")
        if not self.initialize_agent():
            print(f"{Fore.RED}❌ Failed to initialize. Exiting.{Style.RESET_ALL}")
            return
        
        # Main menu loop
        while True:
            try:
                choice = self.print_menu()
                
                if choice == '1':
                    self.handle_authentication()
                elif choice == '2':
                    self.handle_band_testing()
                elif choice == '3':
                    self.handle_monitoring(start=True)
                elif choice == '4':
                    self.handle_monitoring(start=False)
                elif choice == '5':
                    self.handle_report_generation()
                elif choice == '6':
                    self.handle_peak_optimization()
                elif choice == '7':
                    self.handle_scheduling()
                elif choice == '8':
                    self.handle_status_view()
                elif choice == '9':
                    self.handle_manual_band_switch()
                elif choice == '10':
                    self.handle_band_configuration()
                elif choice == '11':
                    self.handle_metrics_summary()
                elif choice == '12':
                    self.handle_band_comparison_export()
                elif choice == '13':
                    self.handle_cleanup()
                else:
                    print(f"{Fore.RED}❌ Invalid choice. Please try again.{Style.RESET_ALL}")
                
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}🛑 Interrupted by user{Style.RESET_ALL}")
                self.handle_cleanup()
            except Exception as e:
                print(f"{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
    
    def run_automated(self, test_bands: bool = False, monitor: bool = False, 
                     generate_report: bool = False, optimize: bool = False):
        """Run automated mode with specified operations"""
        self.print_banner()
        
        print(f"{Fore.CYAN}🤖 Running in automated mode...{Style.RESET_ALL}")
        
        # Initialize agent
        if not self.initialize_agent():
            print(f"{Fore.RED}❌ Failed to initialize. Exiting.{Style.RESET_ALL}")
            return
        
        # Authenticate
        if not self.agent.authenticate():
            print(f"{Fore.RED}❌ Authentication failed. Exiting.{Style.RESET_ALL}")
            return
        
        try:
            # Test bands if requested
            if test_bands:
                print(f"{Fore.CYAN}📡 Testing all bands...{Style.RESET_ALL}")
                self.agent.test_all_bands()
            
            # Start monitoring if requested
            if monitor:
                print(f"{Fore.CYAN}📊 Starting monitoring...{Style.RESET_ALL}")
                self.agent.start_continuous_monitoring()
                
                # Keep running for a while
                time.sleep(300)  # 5 minutes
                self.agent.stop_continuous_monitoring()
            
            # Generate report if requested
            if generate_report:
                print(f"{Fore.CYAN}📊 Generating report...{Style.RESET_ALL}")
                self.agent.generate_performance_report()
            
            # Optimize if requested
            if optimize:
                print(f"{Fore.CYAN}⏰ Running optimization...{Style.RESET_ALL}")
                self.agent.optimize_for_peak_hours()
            
            print(f"{Fore.GREEN}✅ Automated operations completed{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error in automated mode: {e}{Style.RESET_ALL}")
        finally:
            self.handle_cleanup()

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    print(f"\n{Fore.YELLOW}🛑 Received interrupt signal. Cleaning up...{Style.RESET_ALL}")
    sys.exit(0)

def main():
    """Main entry point"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Huawei LTE Router AI Automation Agent')
    parser.add_argument('--ip', help='Router IP address')
    parser.add_argument('--username', help='Router username')
    parser.add_argument('--password', help='Router password')
    parser.add_argument('--test-bands', action='store_true', help='Test all bands')
    parser.add_argument('--monitor', action='store_true', help='Start monitoring')
    parser.add_argument('--report', action='store_true', help='Generate report')
    parser.add_argument('--optimize', action='store_true', help='Run optimization')
    parser.add_argument('--automated', action='store_true', help='Run in automated mode')
    
    args = parser.parse_args()
    
    # Create and run application
    app = LTEAutomationApp()
    
    if args.automated or any([args.test_bands, args.monitor, args.report, args.optimize]):
        # Run in automated mode
        app.run_automated(
            test_bands=args.test_bands,
            monitor=args.monitor,
            generate_report=args.report,
            optimize=args.optimize
        )
    else:
        # Run in interactive mode
        app.run_interactive()

if __name__ == "__main__":
    main() 