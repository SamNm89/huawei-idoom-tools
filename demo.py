#!/usr/bin/env python3
"""
Demo script for Huawei LTE Router AI Automation Agent
Showcases key features and provides examples
"""

import time
import sys
from datetime import datetime
from colorama import init, Fore, Style

from ai_agent import AIAutomationAgent
from config import ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD

# Initialize colorama
init()

def print_demo_header(title: str):
    """Print demo section header"""
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"🎬 DEMO: {title}")
    print(f"{'='*50}{Style.RESET_ALL}")

def demo_authentication():
    """Demo router authentication"""
    print_demo_header("Router Authentication")
    
    print(f"{Fore.YELLOW}Step 1: Initializing AI Agent{Style.RESET_ALL}")
    agent = AIAutomationAgent(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD)
    
    print(f"{Fore.YELLOW}Step 2: Authenticating with router{Style.RESET_ALL}")
    if agent.authenticate():
        print(f"{Fore.GREEN}✅ Authentication successful!{Style.RESET_ALL}")
        return agent
    else:
        print(f"{Fore.RED}❌ Authentication failed{Style.RESET_ALL}")
        return None

def demo_signal_monitoring(agent):
    """Demo real-time signal monitoring"""
    print_demo_header("Real-time Signal Monitoring")
    
    if not agent:
        print(f"{Fore.RED}❌ Agent not available{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}Monitoring signal metrics for 30 seconds...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Press Ctrl+C to stop early{Style.RESET_ALL}")
    
    try:
        start_time = time.time()
        while time.time() - start_time < 30:
            metrics = agent.router.get_signal_metrics()
            if metrics:
                # Calculate signal quality
                quality = agent._get_signal_quality(metrics)
                quality_color = {
                    'excellent': Fore.GREEN,
                    'good': Fore.CYAN,
                    'fair': Fore.YELLOW,
                    'poor': Fore.RED
                }.get(quality, Fore.WHITE)
                
                print(f"{Fore.CYAN}📡 {metrics.band} | "
                      f"RSRP: {metrics.rsrp:.1f} dBm | "
                      f"SINR: {metrics.sinr:.1f} dB | "
                      f"Quality: {quality_color}{quality}{Style.RESET_ALL}")
                
                # Log the metrics
                agent.data_logger.log_metrics(metrics)
            
            time.sleep(5)  # Update every 5 seconds
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 Monitoring stopped by user{Style.RESET_ALL}")

def demo_band_testing(agent):
    """Demo LTE band testing"""
    print_demo_header("LTE Band Testing")
    
    if not agent:
        print(f"{Fore.RED}❌ Agent not available{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}Testing available LTE bands...{Style.RESET_ALL}")
    
    # Get available bands
    bands = agent.router.get_available_bands()
    print(f"{Fore.CYAN}Available bands: {', '.join(bands)}{Style.RESET_ALL}")
    
    # Test first 2 bands for demo (shorter duration)
    test_bands = bands[:2] if len(bands) >= 2 else bands
    
    for band in test_bands:
        print(f"{Fore.CYAN}Testing {band}...{Style.RESET_ALL}")
        
        # Test band for 60 seconds (demo duration)
        metrics_list = agent.router.test_band_performance(band, duration=60)
        
        if metrics_list:
            # Analyze performance
            performance = agent._analyze_band_performance(band, metrics_list)
            
            print(f"{Fore.GREEN}✅ {band} Results:{Style.RESET_ALL}")
            print(f"  Avg RSRP: {performance.avg_rsrp:.1f} dBm")
            print(f"  Avg SINR: {performance.avg_sinr:.1f} dB")
            print(f"  Bandwidth Score: {performance.avg_bandwidth_score:.3f}")
            print(f"  Stability: {performance.stability_score:.3f}")
        else:
            print(f"{Fore.RED}❌ No data collected for {band}{Style.RESET_ALL}")

def demo_peak_optimization(agent):
    """Demo peak hour optimization"""
    print_demo_header("Peak Hour Optimization")
    
    if not agent:
        print(f"{Fore.RED}❌ Agent not available{Style.RESET_ALL}")
        return
    
    current_hour = datetime.now().hour
    print(f"{Fore.CYAN}Current hour: {current_hour}{Style.RESET_ALL}")
    
    # Check if we're in peak hours
    peak_hours = [7, 8, 9, 17, 18, 19]
    is_peak = current_hour in peak_hours
    
    print(f"Peak hours: {peak_hours}")
    print(f"Is peak hour: {is_peak}")
    
    print(f"{Fore.YELLOW}Running peak hour optimization...{Style.RESET_ALL}")
    agent.optimize_for_peak_hours()
    print(f"{Fore.GREEN}✅ Peak hour optimization completed{Style.RESET_ALL}")

def demo_visualization(agent):
    """Demo visualization generation"""
    print_demo_header("Data Visualization")
    
    if not agent:
        print(f"{Fore.RED}❌ Agent not available{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}Generating visualizations...{Style.RESET_ALL}")
    
    try:
        # Generate timeline plot
        timeline_plot = agent.visualizer.plot_signal_timeline(agent.data_logger.csv_file, hours=1)
        if timeline_plot:
            print(f"{Fore.GREEN}✅ Timeline plot: {timeline_plot}{Style.RESET_ALL}")
        
        # Generate band comparison
        band_plot = agent.visualizer.plot_band_comparison(agent.data_logger.csv_file)
        if band_plot:
            print(f"{Fore.GREEN}✅ Band comparison: {band_plot}{Style.RESET_ALL}")
        
        # Generate performance dashboard
        dashboard_plot = agent.visualizer.plot_performance_summary(agent.data_logger.csv_file)
        if dashboard_plot:
            print(f"{Fore.GREEN}✅ Performance dashboard: {dashboard_plot}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ All visualizations generated successfully{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Visualization failed: {e}{Style.RESET_ALL}")

def demo_report_generation(agent):
    """Demo report generation"""
    print_demo_header("Performance Report Generation")
    
    if not agent:
        print(f"{Fore.RED}❌ Agent not available{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}Generating comprehensive performance report...{Style.RESET_ALL}")
    
    try:
        report_file = agent.generate_performance_report()
        if report_file:
            print(f"{Fore.GREEN}✅ Report generated: {report_file}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ No data available for report generation{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Report generation failed: {e}{Style.RESET_ALL}")

def demo_metrics_summary(agent):
    """Demo metrics summary"""
    print_demo_header("Metrics Summary")
    
    if not agent:
        print(f"{Fore.RED}❌ Agent not available{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}Generating metrics summary...{Style.RESET_ALL}")
    
    try:
        summary = agent.data_logger.get_metrics_summary(hours=24)
        if summary:
            print(f"{Fore.CYAN}📊 Metrics Summary (Last 24 hours):{Style.RESET_ALL}")
            print(f"  Total records: {summary.get('total_records', 0)}")
            print(f"  Bands tested: {', '.join(summary.get('bands_tested', []))}")
            
            if 'average_metrics' in summary:
                avg = summary['average_metrics']
                print(f"  Average RSRP: {avg.get('rsrp', 0):.1f} dBm")
                print(f"  Average SINR: {avg.get('sinr', 0):.1f} dB")
                print(f"  Average bandwidth score: {avg.get('bandwidth_score', 0):.3f}")
            
            if 'best_performing_band' in summary:
                print(f"  Best performing band: {summary['best_performing_band']}")
            
            if 'signal_quality_distribution' in summary:
                print(f"  Signal quality distribution: {summary['signal_quality_distribution']}")
        else:
            print(f"{Fore.YELLOW}⚠️ No metrics data available{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Metrics summary failed: {e}{Style.RESET_ALL}")

def run_full_demo():
    """Run the complete demo"""
    print(f"{Fore.CYAN}🎬 Huawei LTE Router AI Agent Demo{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This demo showcases all major features of the automation agent{Style.RESET_ALL}")
    
    # Step 1: Authentication
    agent = demo_authentication()
    
    if agent:
        try:
            # Step 2: Signal Monitoring
            demo_signal_monitoring(agent)
            
            # Step 3: Band Testing
            demo_band_testing(agent)
            
            # Step 4: Peak Hour Optimization
            demo_peak_optimization(agent)
            
            # Step 5: Visualization
            demo_visualization(agent)
            
            # Step 6: Report Generation
            demo_report_generation(agent)
            
            # Step 7: Metrics Summary
            demo_metrics_summary(agent)
            
            print(f"\n{Fore.GREEN}🎉 Demo completed successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Check the generated files in the current directory:{Style.RESET_ALL}")
            print(f"  - CSV logs: {agent.data_logger.csv_file}")
            print(f"  - JSON logs: {agent.data_logger.json_file}")
            print(f"  - Plots: plots/ directory")
            print(f"  - Reports: reports/ directory")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Demo failed: {e}{Style.RESET_ALL}")
        finally:
            # Cleanup
            agent.cleanup()
    else:
        print(f"{Fore.RED}❌ Demo cannot continue without authentication{Style.RESET_ALL}")

def run_quick_demo():
    """Run a quick demo"""
    print(f"{Fore.CYAN}⚡ Quick Demo{Style.RESET_ALL}")
    
    try:
        agent = AIAutomationAgent(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD)
        
        if agent.authenticate():
            print(f"{Fore.GREEN}✅ Authentication successful{Style.RESET_ALL}")
            
            # Get current status
            metrics = agent.router.get_signal_metrics()
            if metrics:
                print(f"{Fore.CYAN}📡 Current Status:{Style.RESET_ALL}")
                print(f"  Band: {metrics.band}")
                print(f"  RSRP: {metrics.rsrp:.1f} dBm")
                print(f"  SINR: {metrics.sinr:.1f} dB")
                print(f"  Quality: {agent._get_signal_quality(metrics)}")
            
            # Get available bands
            bands = agent.router.get_available_bands()
            print(f"{Fore.CYAN}📡 Available Bands:{Style.RESET_ALL}")
            for band in bands:
                print(f"  - {band}")
            
            agent.cleanup()
            print(f"{Fore.GREEN}✅ Quick demo completed{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Authentication failed{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Quick demo failed: {e}{Style.RESET_ALL}")

def main():
    """Main demo function"""
    print(f"{Fore.CYAN}🎬 Huawei LTE Router AI Agent Demo{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Router IP: {ROUTER_IP}{Style.RESET_ALL}")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            run_quick_demo()
        elif sys.argv[1] == "--full":
            run_full_demo()
        else:
            print(f"{Fore.RED}❌ Unknown argument: {sys.argv[1]}{Style.RESET_ALL}")
            print(f"Usage: python demo.py [--quick|--full]")
    else:
        # Default to full demo
        run_full_demo()

if __name__ == "__main__":
    main() 