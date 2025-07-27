#!/usr/bin/env python3
"""
Test script for Huawei LTE Router AI Automation Agent
Demonstrates key features and validates functionality
"""

import sys
import time
import logging
from datetime import datetime
from colorama import init, Fore, Style

from ai_agent import AIAutomationAgent
from config import ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD

# Initialize colorama
init()

def print_test_header(test_name: str):
    """Print test header with formatting"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"🧪 TESTING: {test_name}")
    print(f"{'='*60}{Style.RESET_ALL}")

def print_test_result(success: bool, message: str):
    """Print test result with appropriate color"""
    if success:
        print(f"{Fore.GREEN}✅ PASS: {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ FAIL: {message}{Style.RESET_ALL}")

def test_agent_initialization():
    """Test agent initialization"""
    print_test_header("Agent Initialization")
    
    try:
        agent = AIAutomationAgent(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD)
        print_test_result(True, "Agent initialized successfully")
        return agent
    except Exception as e:
        print_test_result(False, f"Agent initialization failed: {e}")
        return None

def test_router_authentication(agent):
    """Test router authentication"""
    print_test_header("Router Authentication")
    
    if not agent:
        print_test_result(False, "Agent not available")
        return False
    
    try:
        success = agent.authenticate()
        print_test_result(success, "Authentication completed")
        return success
    except Exception as e:
        print_test_result(False, f"Authentication failed: {e}")
        return False

def test_signal_metrics_retrieval(agent):
    """Test signal metrics retrieval"""
    print_test_header("Signal Metrics Retrieval")
    
    if not agent:
        print_test_result(False, "Agent not available")
        return False
    
    try:
        metrics = agent.router.get_signal_metrics()
        if metrics:
            print(f"{Fore.CYAN}📡 Current Signal Metrics:{Style.RESET_ALL}")
            print(f"  Band: {metrics.band}")
            print(f"  RSRP: {metrics.rsrp:.1f} dBm")
            print(f"  RSRQ: {metrics.rsrq:.1f} dB")
            print(f"  SINR: {metrics.sinr:.1f} dB")
            print(f"  RSSI: {metrics.rssi:.1f} dBm")
            print(f"  Cell ID: {metrics.cell_id}")
            print(f"  PLMN: {metrics.plmn}")
            print_test_result(True, "Signal metrics retrieved successfully")
            return True
        else:
            print_test_result(False, "No signal metrics available")
            return False
    except Exception as e:
        print_test_result(False, f"Signal metrics retrieval failed: {e}")
        return False

def test_available_bands(agent):
    """Test available bands retrieval"""
    print_test_header("Available Bands Retrieval")
    
    if not agent:
        print_test_result(False, "Agent not available")
        return False
    
    try:
        bands = agent.router.get_available_bands()
        if bands:
            print(f"{Fore.CYAN}📡 Available LTE Bands:{Style.RESET_ALL}")
            for band in bands:
                print(f"  - {band}")
            print_test_result(True, f"Found {len(bands)} available bands")
            return True
        else:
            print_test_result(False, "No bands available")
            return False
    except Exception as e:
        print_test_result(False, f"Band retrieval failed: {e}")
        return False

def test_data_logging(agent):
    """Test data logging functionality"""
    print_test_header("Data Logging Test")
    
    if not agent:
        print_test_result(False, "Agent not available")
        return False
    
    try:
        # Get current metrics
        metrics = agent.router.get_signal_metrics()
        if metrics:
            # Test logging
            success = agent.data_logger.log_metrics(metrics)
            print_test_result(success, "Metrics logged successfully")
            return success
        else:
            print_test_result(False, "No metrics to log")
            return False
    except Exception as e:
        print_test_result(False, f"Data logging failed: {e}")
        return False

def test_visualization(agent):
    """Test visualization generation"""
    print_test_header("Visualization Test")
    
    if not agent:
        print_test_result(False, "Agent not available")
        return False
    
    try:
        # Generate a simple visualization
        csv_file = agent.data_logger.csv_file
        if csv_file and agent.visualizer:
            # Try to create a timeline plot
            plot_file = agent.visualizer.plot_signal_timeline(csv_file, hours=1)
            if plot_file:
                print_test_result(True, f"Visualization created: {plot_file}")
                return True
            else:
                print_test_result(False, "No data available for visualization")
                return False
        else:
            print_test_result(False, "Visualization components not available")
            return False
    except Exception as e:
        print_test_result(False, f"Visualization failed: {e}")
        return False

def test_band_performance_analysis(agent):
    """Test band performance analysis"""
    print_test_header("Band Performance Analysis")
    
    if not agent:
        print_test_result(False, "Agent not available")
        return False
    
    try:
        # Get metrics summary
        summary = agent.data_logger.get_metrics_summary(hours=24)
        if summary:
            print(f"{Fore.CYAN}📊 Performance Summary:{Style.RESET_ALL}")
            print(f"  Total records: {summary.get('total_records', 0)}")
            print(f"  Bands tested: {', '.join(summary.get('bands_tested', []))}")
            
            if 'average_metrics' in summary:
                avg = summary['average_metrics']
                print(f"  Avg RSRP: {avg.get('rsrp', 0):.1f} dBm")
                print(f"  Avg SINR: {avg.get('sinr', 0):.1f} dB")
                print(f"  Avg bandwidth score: {avg.get('bandwidth_score', 0):.3f}")
            
            print_test_result(True, "Performance analysis completed")
            return True
        else:
            print_test_result(False, "No performance data available")
            return False
    except Exception as e:
        print_test_result(False, f"Performance analysis failed: {e}")
        return False

def test_peak_hour_optimization(agent):
    """Test peak hour optimization logic"""
    print_test_header("Peak Hour Optimization Test")
    
    if not agent:
        print_test_result(False, "Agent not available")
        return False
    
    try:
        # Test the optimization logic
        current_hour = datetime.now().hour
        print(f"{Fore.CYAN}⏰ Current hour: {current_hour}{Style.RESET_ALL}")
        
        # Check if we're in peak hours
        peak_hours = [7, 8, 9, 17, 18, 19]
        is_peak = current_hour in peak_hours
        
        print(f"  Peak hours: {peak_hours}")
        print(f"  Is peak hour: {is_peak}")
        
        # Test optimization function
        agent.optimize_for_peak_hours()
        print_test_result(True, "Peak hour optimization logic tested")
        return True
    except Exception as e:
        print_test_result(False, f"Peak hour optimization failed: {e}")
        return False

def test_connection_status(agent):
    """Test connection status retrieval"""
    print_test_header("Connection Status Test")
    
    if not agent:
        print_test_result(False, "Agent not available")
        return False
    
    try:
        status = agent.router.get_connection_status()
        if status:
            print(f"{Fore.CYAN}📡 Connection Status:{Style.RESET_ALL}")
            for key, value in status.items():
                print(f"  {key}: {value}")
            print_test_result(True, "Connection status retrieved")
            return True
        else:
            print_test_result(False, "No connection status available")
            return False
    except Exception as e:
        print_test_result(False, f"Connection status failed: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print(f"{Fore.CYAN}🚀 Starting Comprehensive Test Suite{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This will test all major components of the LTE automation agent{Style.RESET_ALL}")
    
    # Test results tracking
    test_results = []
    
    # Initialize agent
    agent = test_agent_initialization()
    test_results.append(("Agent Initialization", agent is not None))
    
    if agent:
        # Test authentication
        auth_success = test_router_authentication(agent)
        test_results.append(("Router Authentication", auth_success))
        
        # Test signal metrics
        metrics_success = test_signal_metrics_retrieval(agent)
        test_results.append(("Signal Metrics", metrics_success))
        
        # Test available bands
        bands_success = test_available_bands(agent)
        test_results.append(("Available Bands", bands_success))
        
        # Test data logging
        logging_success = test_data_logging(agent)
        test_results.append(("Data Logging", logging_success))
        
        # Test visualization
        viz_success = test_visualization(agent)
        test_results.append(("Visualization", viz_success))
        
        # Test performance analysis
        analysis_success = test_band_performance_analysis(agent)
        test_results.append(("Performance Analysis", analysis_success))
        
        # Test peak hour optimization
        optimization_success = test_peak_hour_optimization(agent)
        test_results.append(("Peak Hour Optimization", optimization_success))
        
        # Test connection status
        status_success = test_connection_status(agent)
        test_results.append(("Connection Status", status_success))
        
        # Cleanup
        agent.cleanup()
    
    # Print summary
    print_test_header("Test Summary")
    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)
    
    print(f"{Fore.CYAN}📊 Test Results:{Style.RESET_ALL}")
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\n{Fore.GREEN}Overall: {passed}/{total} tests passed{Style.RESET_ALL}")
    
    if passed == total:
        print(f"{Fore.GREEN}🎉 All tests passed! The agent is ready to use.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️ Some tests failed. Check the output above for details.{Style.RESET_ALL}")

def run_quick_test():
    """Run a quick connectivity test"""
    print(f"{Fore.CYAN}⚡ Quick Connectivity Test{Style.RESET_ALL}")
    
    try:
        agent = AIAutomationAgent(ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD)
        print(f"{Fore.GREEN}✅ Agent initialized{Style.RESET_ALL}")
        
        if agent.authenticate():
            print(f"{Fore.GREEN}✅ Authentication successful{Style.RESET_ALL}")
            
            metrics = agent.router.get_signal_metrics()
            if metrics:
                print(f"{Fore.GREEN}✅ Signal metrics retrieved{Style.RESET_ALL}")
                print(f"  Band: {metrics.band}")
                print(f"  RSRP: {metrics.rsrp:.1f} dBm")
                print(f"  SINR: {metrics.sinr:.1f} dB")
            else:
                print(f"{Fore.YELLOW}⚠️ No signal metrics available{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Authentication failed{Style.RESET_ALL}")
        
        agent.cleanup()
        
    except Exception as e:
        print(f"{Fore.RED}❌ Quick test failed: {e}{Style.RESET_ALL}")

def main():
    """Main test function"""
    print(f"{Fore.CYAN}🧪 Huawei LTE Router AI Agent Test Suite{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Router IP: {ROUTER_IP}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Username: {ROUTER_USERNAME}{Style.RESET_ALL}")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            run_quick_test()
        elif sys.argv[1] == "--comprehensive":
            run_comprehensive_test()
        else:
            print(f"{Fore.RED}❌ Unknown argument: {sys.argv[1]}{Style.RESET_ALL}")
            print(f"Usage: python test_agent.py [--quick|--comprehensive]")
    else:
        # Default to comprehensive test
        run_comprehensive_test()

if __name__ == "__main__":
    main() 