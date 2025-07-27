"""
AI Automation Agent for Huawei LTE Router
Handles intelligent band selection, monitoring, and optimization
"""

import time
import logging
import schedule
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from dataclasses import dataclass
from colorama import init, Fore, Style
import json

from huawei_router import HuaweiRouter, SignalMetrics
from data_logger import DataLogger
from visualization import SignalVisualizer
from config import MONITORING_CONFIG, SIGNAL_THRESHOLDS, LTE_BANDS

# Initialize colorama for colored output
init()

@dataclass
class BandPerformance:
    """Data class for band performance analysis"""
    band: str
    avg_rsrp: float
    avg_rsrq: float
    avg_sinr: float
    avg_bandwidth_score: float
    stability_score: float
    peak_performance: float
    off_peak_performance: float

class AIAutomationAgent:
    """Main AI automation agent for LTE band optimization"""
    
    def __init__(self, router_ip: str = None, username: str = None, password: str = None):
        self.router = HuaweiRouter(router_ip, username, password)
        self.data_logger = DataLogger()
        self.visualizer = SignalVisualizer()
        self.logger = logging.getLogger(__name__)
        
        # Performance tracking
        self.band_performance_history = {}
        self.current_best_band = None
        self.auto_switch_enabled = True
        self.monitoring_active = False
        
        # Threading for background monitoring
        self.monitor_thread = None
        self.stop_monitoring = threading.Event()
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('lte_agent.log'),
                logging.StreamHandler()
            ]
        )
    
    def authenticate(self) -> bool:
        """Authenticate with the router"""
        print(f"{Fore.CYAN}🔐 Authenticating with Huawei router...{Style.RESET_ALL}")
        success = self.router.authenticate()
        
        if success:
            print(f"{Fore.GREEN}✅ Authentication successful{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Authentication failed{Style.RESET_ALL}")
        
        return success
    
    def test_all_bands(self, duration_per_band: int = 300) -> Dict[str, BandPerformance]:
        """Test all available LTE bands and analyze performance"""
        print(f"{Fore.YELLOW}📡 Testing all available LTE bands...{Style.RESET_ALL}")
        
        available_bands = self.router.get_available_bands()
        band_results = {}
        
        for band in available_bands:
            print(f"{Fore.CYAN}Testing {band}...{Style.RESET_ALL}")
            
            # Test the band
            metrics_list = self.router.test_band_performance(band, duration_per_band)
            
            if metrics_list:
                # Log all metrics
                self.data_logger.log_batch_metrics(metrics_list)
                
                # Analyze performance
                performance = self._analyze_band_performance(band, metrics_list)
                band_results[band] = performance
                
                print(f"{Fore.GREEN}✅ {band} completed - Avg Score: {performance.avg_bandwidth_score:.3f}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ {band} failed to collect data{Style.RESET_ALL}")
        
        # Update best band
        if band_results:
            self.current_best_band = max(band_results.keys(), 
                                       key=lambda x: band_results[x].avg_bandwidth_score)
            print(f"{Fore.GREEN}🏆 Best performing band: {self.current_best_band}{Style.RESET_ALL}")
        
        return band_results
    
    def _analyze_band_performance(self, band: str, metrics_list: List[SignalMetrics]) -> BandPerformance:
        """Analyze performance metrics for a specific band"""
        if not metrics_list:
            return BandPerformance(band, 0, 0, 0, 0, 0, 0, 0)
        
        # Calculate averages
        avg_rsrp = np.mean([m.rsrp for m in metrics_list])
        avg_rsrq = np.mean([m.rsrq for m in metrics_list])
        avg_sinr = np.mean([m.sinr for m in metrics_list])
        
        # Calculate bandwidth scores
        bandwidth_scores = []
        for metrics in metrics_list:
            # Calculate bandwidth score (similar to data_logger)
            sinr_score = max(0, min(1, (metrics.sinr + 10) / 30))
            rsrp_score = max(0, min(1, (metrics.rsrp + 140) / 60))
            bandwidth_score = (sinr_score * 0.7 + rsrp_score * 0.3)
            bandwidth_scores.append(bandwidth_score)
        
        avg_bandwidth_score = np.mean(bandwidth_scores)
        
        # Calculate stability (lower std = more stable)
        stability_score = 1 - np.std(bandwidth_scores)  # Higher is better
        
        # Analyze peak vs off-peak performance
        peak_hours = [7, 8, 9, 17, 18, 19]  # Morning and evening peak hours
        peak_metrics = [m for m in metrics_list if m.timestamp.hour in peak_hours]
        off_peak_metrics = [m for m in metrics_list if m.timestamp.hour not in peak_hours]
        
        peak_performance = np.mean([m.sinr for m in peak_metrics]) if peak_metrics else 0
        off_peak_performance = np.mean([m.sinr for m in off_peak_metrics]) if off_peak_metrics else 0
        
        return BandPerformance(
            band=band,
            avg_rsrp=avg_rsrp,
            avg_rsrq=avg_rsrq,
            avg_sinr=avg_sinr,
            avg_bandwidth_score=avg_bandwidth_score,
            stability_score=stability_score,
            peak_performance=peak_performance,
            off_peak_performance=off_peak_performance
        )
    
    def start_continuous_monitoring(self, interval_seconds: int = 30):
        """Start continuous monitoring of signal quality"""
        print(f"{Fore.CYAN}📊 Starting continuous monitoring...{Style.RESET_ALL}")
        
        self.monitoring_active = True
        self.stop_monitoring.clear()
        
        def monitor_loop():
            while not self.stop_monitoring.is_set():
                try:
                    # Get current metrics
                    metrics = self.router.get_signal_metrics()
                    
                    if metrics:
                        # Log the metrics
                        self.data_logger.log_metrics(metrics)
                        
                        # Check if we need to switch bands
                        if self.auto_switch_enabled:
                            self._check_band_switch(metrics)
                        
                        # Print current status
                        self._print_status(metrics)
                    
                    time.sleep(interval_seconds)
                    
                except Exception as e:
                    self.logger.error(f"Error in monitoring loop: {e}")
                    time.sleep(interval_seconds)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_continuous_monitoring(self):
        """Stop continuous monitoring"""
        print(f"{Fore.YELLOW}🛑 Stopping continuous monitoring...{Style.RESET_ALL}")
        self.monitoring_active = False
        self.stop_monitoring.set()
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _check_band_switch(self, current_metrics: SignalMetrics):
        """Check if we need to switch bands based on performance degradation"""
        try:
            # Get recent performance data
            summary = self.data_logger.get_metrics_summary(hours=1)
            
            if not summary or 'average_metrics' not in summary:
                return
            
            current_score = self._calculate_current_score(current_metrics)
            historical_avg = summary['average_metrics']['bandwidth_score']
            
            # If current performance is significantly worse than historical average
            degradation_threshold = MONITORING_CONFIG['auto_switch_threshold']
            
            if current_score < (historical_avg * degradation_threshold):
                print(f"{Fore.YELLOW}⚠️ Performance degradation detected. Considering band switch...{Style.RESET_ALL}")
                self._smart_band_switch()
                
        except Exception as e:
            self.logger.error(f"Error checking band switch: {e}")
    
    def _calculate_current_score(self, metrics: SignalMetrics) -> float:
        """Calculate current bandwidth score"""
        sinr_score = max(0, min(1, (metrics.sinr + 10) / 30))
        rsrp_score = max(0, min(1, (metrics.rsrp + 140) / 60))
        return (sinr_score * 0.7 + rsrp_score * 0.3)
    
    def _smart_band_switch(self):
        """Intelligently switch to the best available band"""
        try:
            # Get recent performance data for all bands
            summary = self.data_logger.get_metrics_summary(hours=6)
            
            if not summary or 'best_performing_band' not in summary:
                return
            
            best_band = summary['best_performing_band']
            current_band = self.router.get_signal_metrics().band if self.router.get_signal_metrics() else None
            
            if best_band and best_band != current_band:
                print(f"{Fore.CYAN}🔄 Switching from {current_band} to {best_band}...{Style.RESET_ALL}")
                
                if self.router.set_lte_band(best_band):
                    print(f"{Fore.GREEN}✅ Successfully switched to {best_band}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Failed to switch to {best_band}{Style.RESET_ALL}")
                    
        except Exception as e:
            self.logger.error(f"Error in smart band switch: {e}")
    
    def _print_status(self, metrics: SignalMetrics):
        """Print current status with colored output"""
        quality = self._get_signal_quality(metrics)
        quality_color = {
            'excellent': Fore.GREEN,
            'good': Fore.CYAN,
            'fair': Fore.YELLOW,
            'poor': Fore.RED
        }.get(quality, Fore.WHITE)
        
        print(f"{Fore.CYAN}📡 Band: {metrics.band} | "
              f"RSRP: {metrics.rsrp:.1f} dBm | "
              f"SINR: {metrics.sinr:.1f} dB | "
              f"Quality: {quality_color}{quality}{Style.RESET_ALL}")
    
    def _get_signal_quality(self, metrics: SignalMetrics) -> str:
        """Determine signal quality based on metrics"""
        # Calculate quality score
        rsrp_score = max(0, (metrics.rsrp + 140) / 60)
        rsrq_score = max(0, (metrics.rsrq + 25) / 15)
        sinr_score = max(0, (metrics.sinr + 10) / 30)
        
        quality_score = (rsrp_score * 0.4 + rsrq_score * 0.3 + sinr_score * 0.3)
        
        if quality_score >= 0.8:
            return 'excellent'
        elif quality_score >= 0.6:
            return 'good'
        elif quality_score >= 0.4:
            return 'fair'
        else:
            return 'poor'
    
    def generate_performance_report(self) -> str:
        """Generate comprehensive performance report with visualizations"""
        print(f"{Fore.CYAN}📊 Generating performance report...{Style.RESET_ALL}")
        
        try:
            # Generate all visualizations
            timeline_plot = self.visualizer.plot_signal_timeline(self.data_logger.csv_file)
            band_plot = self.visualizer.plot_band_comparison(self.data_logger.csv_file)
            heatmap_plot = self.visualizer.plot_heatmap(self.data_logger.csv_file)
            dashboard_plot = self.visualizer.plot_performance_summary(self.data_logger.csv_file)
            
            # Generate comprehensive report
            report_file = self.visualizer.generate_report(self.data_logger.csv_file)
            
            print(f"{Fore.GREEN}✅ Performance report generated: {report_file}{Style.RESET_ALL}")
            return report_file
            
        except Exception as e:
            self.logger.error(f"Error generating performance report: {e}")
            return ""
    
    def optimize_for_peak_hours(self):
        """Optimize band selection for peak usage hours"""
        print(f"{Fore.CYAN}⏰ Optimizing for peak hours...{Style.RESET_ALL}")
        
        try:
            # Get current time
            current_hour = datetime.now().hour
            
            # Check if we're in peak hours
            peak_hours = MONITORING_CONFIG['peak_hours']
            is_peak_hour = False
            
            for period in peak_hours.values():
                start_hour = int(period['start'].split(':')[0])
                end_hour = int(period['end'].split(':')[0])
                
                if start_hour <= current_hour <= end_hour:
                    is_peak_hour = True
                    break
            
            if is_peak_hour:
                print(f"{Fore.YELLOW}📈 Peak hours detected - optimizing for bandwidth...{Style.RESET_ALL}")
                # Switch to band with best peak performance
                self._switch_to_peak_optimized_band()
            else:
                print(f"{Fore.CYAN}📉 Off-peak hours - optimizing for stability...{Style.RESET_ALL}")
                # Switch to band with best stability
                self._switch_to_stability_optimized_band()
                
        except Exception as e:
            self.logger.error(f"Error optimizing for peak hours: {e}")
    
    def _switch_to_peak_optimized_band(self):
        """Switch to band optimized for peak hour performance"""
        try:
            # Get band performance data
            band_comparison = self.data_logger.export_band_comparison()
            
            if band_comparison is not None and not band_comparison.empty:
                # Find band with best peak performance (highest SINR during peak hours)
                best_peak_band = band_comparison['sinr_mean'].idxmax()
                
                current_metrics = self.router.get_signal_metrics()
                current_band = current_metrics.band if current_metrics else None
                
                if best_peak_band and best_peak_band != current_band:
                    print(f"{Fore.CYAN}🔄 Switching to peak-optimized band: {best_peak_band}{Style.RESET_ALL}")
                    self.router.set_lte_band(best_peak_band)
                    
        except Exception as e:
            self.logger.error(f"Error switching to peak optimized band: {e}")
    
    def set_band_configuration(self, band_config: dict) -> bool:
        """Set LTE band configuration using the client.net.set_lte_band format"""
        try:
            print(f"{Fore.CYAN}🔄 Setting LTE band configuration...{Style.RESET_ALL}")
            print(f"Configuration: {band_config}")
            
            success = self.router.set_lte_bands_config(band_config)
            
            if success:
                enabled_bands = [band for band, enabled in band_config.items() if enabled]
                print(f"{Fore.GREEN}✅ Successfully set bands: {enabled_bands}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Failed to set band configuration{Style.RESET_ALL}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error setting band configuration: {e}")
            return False
    
    def get_current_band_config(self) -> dict:
        """Get current LTE band configuration"""
        try:
            config = self.router.get_current_band_config()
            if config:
                print(f"{Fore.CYAN}📡 Current band configuration: {config}{Style.RESET_ALL}")
            return config
        except Exception as e:
            self.logger.error(f"Error getting band configuration: {e}")
            return {}
    
    def _switch_to_stability_optimized_band(self):
        """Switch to band optimized for stability"""
        try:
            # Get band performance data
            band_comparison = self.data_logger.export_band_comparison()
            
            if band_comparison is not None and not band_comparison.empty:
                # Find band with best stability (lowest std deviation)
                best_stable_band = band_comparison['bandwidth_score_std'].idxmin()
                
                current_metrics = self.router.get_signal_metrics()
                current_band = current_metrics.band if current_metrics else None
                
                if best_stable_band and best_stable_band != current_band:
                    print(f"{Fore.CYAN}🔄 Switching to stability-optimized band: {best_stable_band}{Style.RESET_ALL}")
                    self.router.set_lte_band(best_stable_band)
                    
        except Exception as e:
            self.logger.error(f"Error switching to stability optimized band: {e}")
    
    def schedule_optimization(self):
        """Schedule automatic optimization at peak hours"""
        print(f"{Fore.CYAN}⏰ Scheduling automatic optimization...{Style.RESET_ALL}")
        
        # Schedule peak hour optimization
        schedule.every().day.at("07:00").do(self.optimize_for_peak_hours)
        schedule.every().day.at("17:00").do(self.optimize_for_peak_hours)
        
        # Schedule off-peak optimization
        schedule.every().day.at("10:00").do(self.optimize_for_peak_hours)
        schedule.every().day.at("20:00").do(self.optimize_for_peak_hours)
        
        print(f"{Fore.GREEN}✅ Optimization scheduled for peak hours (07:00, 17:00) and off-peak (10:00, 20:00){Style.RESET_ALL}")
    
    def run_scheduler(self):
        """Run the scheduler in a separate thread"""
        def scheduler_loop():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        scheduler_thread.start()
    
    def cleanup(self):
        """Cleanup resources"""
        print(f"{Fore.YELLOW}🧹 Cleaning up resources...{Style.RESET_ALL}")
        
        self.stop_continuous_monitoring()
        self.router.close()
        
        # Cleanup old logs
        self.data_logger.cleanup_old_logs()
        
        print(f"{Fore.GREEN}✅ Cleanup completed{Style.RESET_ALL}") 