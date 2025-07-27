"""
Huawei LTE Router Interface
Handles authentication, signal monitoring, and band configuration
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import xml.etree.ElementTree as ET
from config import ROUTER_IP, ROUTER_USERNAME, ROUTER_PASSWORD, LTE_BANDS

@dataclass
class SignalMetrics:
    """Data class for LTE signal metrics"""
    timestamp: datetime
    band: str
    rsrp: float
    rsrq: float
    sinr: float
    rssi: float
    cell_id: str
    plmn: str

class HuaweiRouter:
    """Main class for interacting with Huawei LTE router"""
    
    def __init__(self, ip: str = ROUTER_IP, username: str = ROUTER_USERNAME, password: str = ROUTER_PASSWORD):
        self.ip = ip
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.verify = False
        self.base_url = f"http://{ip}"
        self.logger = logging.getLogger(__name__)
        
        # Disable SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def authenticate(self) -> bool:
        """Authenticate with the router"""
        try:
            # First, get the login page to extract tokens
            login_url = f"{self.base_url}/api/user/login"
            login_data = {
                'username': self.username,
                'password': self.password
            }
            
            response = self.session.post(login_url, data=login_data, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("Authentication successful")
                return True
            else:
                self.logger.error(f"Authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            return False
    
    def get_signal_metrics(self) -> Optional[SignalMetrics]:
        """Retrieve current LTE signal metrics"""
        try:
            # Get signal information
            signal_url = f"{self.base_url}/api/device/signal"
            response = self.session.get(signal_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract metrics from response
                metrics = SignalMetrics(
                    timestamp=datetime.now(),
                    band=data.get('band', 'Unknown'),
                    rsrp=float(data.get('rsrp', 0)),
                    rsrq=float(data.get('rsrq', 0)),
                    sinr=float(data.get('sinr', 0)),
                    rssi=float(data.get('rssi', 0)),
                    cell_id=data.get('cell_id', 'Unknown'),
                    plmn=data.get('plmn', 'Unknown')
                )
                
                return metrics
            else:
                self.logger.error(f"Failed to get signal metrics: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting signal metrics: {e}")
            return None
    
    def get_available_bands(self) -> List[str]:
        """Get list of available LTE bands"""
        try:
            bands_url = f"{self.base_url}/api/device/band"
            response = self.session.get(bands_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('bands', list(LTE_BANDS.keys()))
            else:
                self.logger.warning("Could not retrieve available bands, using default list")
                return list(LTE_BANDS.keys())
                
        except Exception as e:
            self.logger.error(f"Error getting available bands: {e}")
            return list(LTE_BANDS.keys())
    
    def set_lte_band(self, band: str) -> bool:
        """Set the LTE band to a specific frequency band"""
        try:
            band_url = f"{self.base_url}/api/device/band"
            band_data = {
                'band': band,
                'action': 'set'
            }
            
            response = self.session.post(band_url, data=band_data, timeout=10)
            
            if response.status_code == 200:
                self.logger.info(f"Successfully set LTE band to {band}")
                # Wait for band change to take effect
                time.sleep(10)
                return True
            else:
                self.logger.error(f"Failed to set band {band}: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting band {band}: {e}")
            return False
    
    def set_lte_bands_config(self, band_config: dict) -> bool:
        """Set multiple LTE bands configuration using the client.net.set_lte_band format"""
        try:
            # Convert the band configuration to the format expected by the router
            band_url = f"{self.base_url}/api/device/band"
            
            # Create the band configuration data
            band_data = {
                'action': 'set_bands',
                'bands': band_config
            }
            
            response = self.session.post(band_url, data=band_data, timeout=10)
            
            if response.status_code == 200:
                enabled_bands = [band for band, enabled in band_config.items() if enabled]
                self.logger.info(f"Successfully set LTE bands configuration: {enabled_bands}")
                # Wait for band changes to take effect
                time.sleep(15)
                return True
            else:
                self.logger.error(f"Failed to set bands configuration: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting bands configuration: {e}")
            return False
    
    def get_current_band_config(self) -> dict:
        """Get current LTE band configuration"""
        try:
            band_url = f"{self.base_url}/api/device/band"
            response = self.session.get(band_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('bands', {})
            else:
                self.logger.error(f"Failed to get band configuration: {response.status_code}")
                return {}
                
        except Exception as e:
            self.logger.error(f"Error getting band configuration: {e}")
            return {}
    
    def get_band_info(self, band: str) -> Dict:
        """Get detailed information about a specific band"""
        return LTE_BANDS.get(band, {})
    
    def test_band_performance(self, band: str, duration: int = 300) -> List[SignalMetrics]:
        """Test performance of a specific band over a duration"""
        self.logger.info(f"Testing band {band} for {duration} seconds")
        
        if not self.set_lte_band(band):
            return []
        
        metrics_list = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            metrics = self.get_signal_metrics()
            if metrics:
                metrics.band = band
                metrics_list.append(metrics)
            
            time.sleep(30)  # Measure every 30 seconds
        
        return metrics_list
    
    def get_connection_status(self) -> Dict:
        """Get current connection status"""
        try:
            status_url = f"{self.base_url}/api/device/information"
            response = self.session.get(status_url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            self.logger.error(f"Error getting connection status: {e}")
            return {}
    
    def reboot_router(self) -> bool:
        """Reboot the router (use with caution)"""
        try:
            reboot_url = f"{self.base_url}/api/device/control"
            reboot_data = {
                'action': 'reboot'
            }
            
            response = self.session.post(reboot_url, data=reboot_data, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("Router reboot initiated")
                return True
            else:
                self.logger.error(f"Failed to reboot router: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error rebooting router: {e}")
            return False
    
    def close(self):
        """Close the session"""
        self.session.close() 