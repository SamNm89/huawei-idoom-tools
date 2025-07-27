"""
Configuration settings for Huawei LTE Router Automation Agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Router Configuration
ROUTER_IP = os.getenv('ROUTER_IP', '192.168.8.1')
ROUTER_USERNAME = os.getenv('ROUTER_USERNAME', 'admin')
ROUTER_PASSWORD = os.getenv('ROUTER_PASSWORD', 'admin')

# LTE Band Configuration
LTE_BANDS = {
    'Band 1': {'freq_range': '2100 MHz', 'bandwidth': '20 MHz'},
    'Band 3': {'freq_range': '1800 MHz', 'bandwidth': '20 MHz'},
    'Band 7': {'freq_range': '2600 MHz', 'bandwidth': '20 MHz'},
    'Band 8': {'freq_range': '900 MHz', 'bandwidth': '10 MHz'},
    'Band 20': {'freq_range': '800 MHz', 'bandwidth': '10 MHz'},
    'Band 28': {'freq_range': '700 MHz', 'bandwidth': '10 MHz'},
    'Band 38': {'freq_range': '2600 MHz', 'bandwidth': '20 MHz'},
    'Band 40': {'freq_range': '2300 MHz', 'bandwidth': '20 MHz'},
}

# Signal Quality Thresholds
SIGNAL_THRESHOLDS = {
    'excellent': {'rsrp': -80, 'rsrq': -10, 'sinr': 20},
    'good': {'rsrp': -90, 'rsrq': -15, 'sinr': 13},
    'fair': {'rsrp': -100, 'rsrq': -20, 'sinr': 0},
    'poor': {'rsrp': -110, 'rsrq': -25, 'sinr': -10},
}

# Monitoring Configuration
MONITORING_CONFIG = {
    'measurement_interval': 30,  # seconds
    'band_test_duration': 300,   # seconds (5 minutes per band)
    'auto_switch_threshold': 0.8,  # 80% degradation triggers band switch
    'peak_hours': {
        'morning': {'start': '07:00', 'end': '09:00'},
        'evening': {'start': '17:00', 'end': '19:00'},
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    'log_file': 'lte_metrics.json',
    'csv_file': 'lte_metrics.csv',
    'log_level': 'INFO',
    'max_log_size': 1000000,  # 1MB
}

# Visualization Configuration
VIZ_CONFIG = {
    'figure_size': (12, 8),
    'dpi': 100,
    'save_format': 'png',
    'update_interval': 60,  # seconds
} 