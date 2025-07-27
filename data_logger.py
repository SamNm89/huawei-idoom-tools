"""
Data logging module for LTE signal metrics
Handles CSV and JSON logging with rotation and compression
"""

import json
import csv
import logging
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import pandas as pd
from huawei_router import SignalMetrics
from config import LOGGING_CONFIG

class DataLogger:
    """Handles logging of LTE signal metrics to CSV and JSON files"""
    
    def __init__(self, csv_file: str = None, json_file: str = None):
        self.csv_file = csv_file or LOGGING_CONFIG['csv_file']
        self.json_file = json_file or LOGGING_CONFIG['log_file']
        self.logger = logging.getLogger(__name__)
        
        # Create logs directory if it doesn't exist
        Path('logs').mkdir(exist_ok=True)
        
        # Initialize CSV file with headers
        self._init_csv_file()
    
    def _init_csv_file(self):
        """Initialize CSV file with headers"""
        if not os.path.exists(self.csv_file):
            headers = [
                'timestamp', 'band', 'rsrp', 'rsrq', 'sinr', 'rssi',
                'cell_id', 'plmn', 'signal_quality', 'bandwidth_score'
            ]
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
    
    def log_metrics(self, metrics: SignalMetrics) -> bool:
        """Log a single metrics record"""
        try:
            # Calculate signal quality score
            signal_quality = self._calculate_signal_quality(metrics)
            bandwidth_score = self._calculate_bandwidth_score(metrics)
            
            # Prepare CSV row
            csv_row = [
                metrics.timestamp.isoformat(),
                metrics.band,
                metrics.rsrp,
                metrics.rsrq,
                metrics.sinr,
                metrics.rssi,
                metrics.cell_id,
                metrics.plmn,
                signal_quality,
                bandwidth_score
            ]
            
            # Write to CSV
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(csv_row)
            
            # Prepare JSON record
            json_record = {
                'timestamp': metrics.timestamp.isoformat(),
                'band': metrics.band,
                'rsrp': metrics.rsrp,
                'rsrq': metrics.rsrq,
                'sinr': metrics.sinr,
                'rssi': metrics.rssi,
                'cell_id': metrics.cell_id,
                'plmn': metrics.plmn,
                'signal_quality': signal_quality,
                'bandwidth_score': bandwidth_score
            }
            
            # Append to JSON file
            self._append_to_json(json_record)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging metrics: {e}")
            return False
    
    def log_batch_metrics(self, metrics_list: List[SignalMetrics]) -> bool:
        """Log multiple metrics records efficiently"""
        try:
            for metrics in metrics_list:
                self.log_metrics(metrics)
            return True
        except Exception as e:
            self.logger.error(f"Error logging batch metrics: {e}")
            return False
    
    def _calculate_signal_quality(self, metrics: SignalMetrics) -> str:
        """Calculate overall signal quality based on metrics"""
        from config import SIGNAL_THRESHOLDS
        
        # Calculate weighted score
        rsrp_score = max(0, (metrics.rsrp + 140) / 60)  # Normalize RSRP (-140 to -80)
        rsrq_score = max(0, (metrics.rsrq + 25) / 15)   # Normalize RSRQ (-25 to -10)
        sinr_score = max(0, (metrics.sinr + 10) / 30)    # Normalize SINR (-10 to 20)
        
        # Weighted average
        quality_score = (rsrp_score * 0.4 + rsrq_score * 0.3 + sinr_score * 0.3)
        
        # Determine quality level
        if quality_score >= 0.8:
            return 'excellent'
        elif quality_score >= 0.6:
            return 'good'
        elif quality_score >= 0.4:
            return 'fair'
        else:
            return 'poor'
    
    def _calculate_bandwidth_score(self, metrics: SignalMetrics) -> float:
        """Calculate bandwidth efficiency score"""
        # Higher SINR generally means better bandwidth utilization
        sinr_score = max(0, min(1, (metrics.sinr + 10) / 30))
        
        # RSRP affects bandwidth stability
        rsrp_score = max(0, min(1, (metrics.rsrp + 140) / 60))
        
        return (sinr_score * 0.7 + rsrp_score * 0.3)
    
    def _append_to_json(self, record: Dict[str, Any]):
        """Append a record to the JSON log file"""
        try:
            # Read existing data
            data = []
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []
            
            # Append new record
            data.append(record)
            
            # Write back to file
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error appending to JSON: {e}")
    
    def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get summary statistics for the last N hours"""
        try:
            # Read CSV data
            df = pd.read_csv(self.csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filter by time range
            cutoff_time = datetime.now() - pd.Timedelta(hours=hours)
            recent_data = df[df['timestamp'] >= cutoff_time]
            
            if recent_data.empty:
                return {}
            
            # Calculate summary statistics
            summary = {
                'total_records': len(recent_data),
                'time_range': f"Last {hours} hours",
                'bands_tested': recent_data['band'].unique().tolist(),
                'average_metrics': {
                    'rsrp': recent_data['rsrp'].mean(),
                    'rsrq': recent_data['rsrq'].mean(),
                    'sinr': recent_data['sinr'].mean(),
                    'rssi': recent_data['rssi'].mean(),
                    'bandwidth_score': recent_data['bandwidth_score'].mean()
                },
                'signal_quality_distribution': recent_data['signal_quality'].value_counts().to_dict(),
                'best_performing_band': recent_data.groupby('band')['bandwidth_score'].mean().idxmax(),
                'worst_performing_band': recent_data.groupby('band')['bandwidth_score'].mean().idxmin()
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting metrics summary: {e}")
            return {}
    
    def export_band_comparison(self, output_file: str = 'band_comparison.csv'):
        """Export band comparison data for analysis"""
        try:
            df = pd.read_csv(self.csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Group by band and calculate statistics
            band_stats = df.groupby('band').agg({
                'rsrp': ['mean', 'std', 'min', 'max'],
                'rsrq': ['mean', 'std', 'min', 'max'],
                'sinr': ['mean', 'std', 'min', 'max'],
                'bandwidth_score': ['mean', 'std', 'min', 'max'],
                'signal_quality': lambda x: x.value_counts().index[0]  # Most common quality
            }).round(2)
            
            # Flatten column names
            band_stats.columns = ['_'.join(col).strip() for col in band_stats.columns]
            
            # Export to CSV
            band_stats.to_csv(output_file)
            self.logger.info(f"Band comparison exported to {output_file}")
            
            return band_stats
            
        except Exception as e:
            self.logger.error(f"Error exporting band comparison: {e}")
            return None
    
    def cleanup_old_logs(self, max_size_mb: int = 10):
        """Clean up old log files to prevent disk space issues"""
        try:
            # Check file sizes
            for file_path in [self.csv_file, self.json_file]:
                if os.path.exists(file_path):
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    if size_mb > max_size_mb:
                        # Create backup and start fresh
                        backup_path = f"{file_path}.backup"
                        os.rename(file_path, backup_path)
                        self.logger.info(f"Created backup of {file_path}")
                        
                        if file_path.endswith('.csv'):
                            self._init_csv_file()
                        
        except Exception as e:
            self.logger.error(f"Error cleaning up logs: {e}") 