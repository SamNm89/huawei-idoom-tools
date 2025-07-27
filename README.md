# Huawei LTE Router AI Automation Agent

A comprehensive Python-based AI automation agent that **bypasses hidden firmware pages** and gains **direct control over LTE band configuration** on Huawei LTE routers. It provides intelligent signal optimization, real-time monitoring, and automated band switching based on performance analysis.

## 🚀 Features

### Core Functionality
- **Router Authentication**: Secure connection to Huawei LTE routers via web interface
- **Real-time Signal Monitoring**: Track RSRP, RSRQ, SINR, and RSSI metrics
- **LTE Band Testing**: Test individual bands (Band 3, Band 7, etc.) for performance
- **Intelligent Band Switching**: Automatic band selection based on signal quality
- **Peak Hour Optimization**: Optimize for bandwidth during peak usage times
- **Performance Benchmarking**: Comprehensive analysis of band performance
- **Direct Band Control**: Set specific band configurations like `client.net.set_lte_band()`

### Advanced Features
- **Data Logging**: CSV and JSON logging with automatic rotation
- **Visualization**: Generate graphs and charts for signal analysis
- **Smart Scheduling**: Automatic optimization at peak hours
- **Performance Reports**: Comprehensive PDF reports with visualizations
- **Real-time Monitoring**: Continuous signal quality monitoring with alerts
- **Multi-threading**: Background monitoring and concurrent operations
- **AI Intelligence**: Learning algorithms and predictive switching
- **Configuration Management**: Environment variables and flexible settings

## 📋 Requirements

- Python 3.8+
- Huawei LTE router (E5573, E5785, or similar)
- Network connection to router (192.168.8.1)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd router
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure router credentials**:
   ```bash
   cp env_example.txt .env
   # Edit .env with your router credentials
   ```

4. **Update router settings** (if needed):
   ```bash
   # Edit config.py to customize:
   # - Router IP address
   # - LTE band configurations
   # - Monitoring intervals
   # - Signal thresholds
   ```

## 🚀 Quick Start

### Interactive Mode
```bash
python main.py
```

### Automated Mode
```bash
# Test all bands
python main.py --test-bands

# Start monitoring
python main.py --monitor

# Generate report
python main.py --report

# Run optimization
python main.py --optimize

# Run all operations
python main.py --automated
```

### Direct Band Configuration
```bash
# Apply your specific band configuration
python apply_band_config.py
```

## 📖 How to Use

### **1. Initial Setup**

#### **Step 1: Install Dependencies**
```bash
# Activate virtual environment (if using)
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

#### **Step 2: Configure Router Credentials**
```bash
# Copy environment template
cp env_example.txt .env

# Edit .env with your router details
ROUTER_IP=192.168.8.1
ROUTER_USERNAME=admin
ROUTER_PASSWORD=your_password
```

#### **Step 3: Test Connection**
```bash
# Run quick connectivity test
python test_agent.py --quick

# Run comprehensive tests
python test_agent.py --comprehensive
```

### **2. Interactive Mode Usage**

#### **Start the Application**
```bash
python main.py
```

#### **Menu Options Explained**

**1. Authenticate with router**
- Establishes secure connection to your Huawei router
- Required before any other operations

**2. Test all LTE bands**
- Tests each available LTE band for performance
- Duration: 5 minutes per band (configurable)
- Generates performance comparison data

**3. Start continuous monitoring**
- Real-time signal monitoring with colored output
- Automatic logging to CSV/JSON files
- Press Ctrl+C to stop

**4. Stop monitoring**
- Stops any running monitoring processes

**5. Generate performance report**
- Creates comprehensive PDF report with visualizations
- Includes timeline charts, band comparisons, and dashboards

**6. Optimize for peak hours**
- Runs peak hour optimization algorithm
- Switches to best performing band for current time

**7. Schedule automatic optimization**
- Sets up automatic optimization at peak hours (7 AM, 5 PM)
- Runs in background thread

**8. View current status**
- Shows current signal metrics and band information
- Real-time status display

**9. Manual band switch**
- **Option 1**: Switch to single band
- **Option 2**: Set band configuration (like `client.net.set_lte_band`)

**10. Band configuration (client.net.set_lte_band)**
- **Option 1**: Get current band configuration
- **Option 2**: Set custom band configuration
- **Option 3**: Apply your specific configuration

**11. View metrics summary**
- Shows performance summary for last 24 hours
- Displays best performing bands and statistics

**12. Export band comparison**
- Exports band performance data to CSV
- For external analysis

**13. Cleanup and exit**
- Stops all processes and cleans up resources

### **3. Direct Band Configuration**

#### **Apply Your Specific Configuration**
```bash
python apply_band_config.py
```

This applies the exact configuration you specified:
```python
{
    'Band3': True,    # Enable Band 3
    'Band7': False,   # Disable Band 7
    'Band20': False,  # Disable Band 20
    'Band8': False    # Disable Band 8
}
```

#### **Custom Band Configuration**
```python
from ai_agent import AIAutomationAgent

agent = AIAutomationAgent()
agent.authenticate()

# Set custom band configuration
config = {
    'Band1': True,
    'Band3': True,
    'Band7': False,
    'Band8': False,
    'Band20': False
}

success = agent.set_band_configuration(config)
```

### **4. Automated Mode Usage**

#### **Test All Bands**
```bash
python main.py --test-bands
```
- Tests all available LTE bands
- Generates performance data
- Creates visualizations

#### **Continuous Monitoring**
```bash
python main.py --monitor
```
- Starts real-time monitoring
- Runs for 5 minutes by default
- Logs all metrics

#### **Generate Report**
```bash
python main.py --report
```
- Creates comprehensive performance report
- Includes all visualizations
- Saves as PDF

#### **Run Optimization**
```bash
python main.py --optimize
```
- Runs peak hour optimization
- Switches to best performing band

### **5. Advanced Usage Examples**

#### **Real-time Signal Monitoring**
```python
from ai_agent import AIAutomationAgent

agent = AIAutomationAgent()
agent.authenticate()

# Start monitoring with 30-second intervals
agent.start_continuous_monitoring(interval_seconds=30)

# The agent will automatically:
# - Log metrics to CSV/JSON
# - Switch bands when performance degrades
# - Generate visualizations
```

#### **Peak Hour Optimization**
```python
# Optimize for peak hours (7-9 AM, 5-7 PM)
agent.optimize_for_peak_hours()

# Schedule automatic optimization
agent.schedule_optimization()
agent.run_scheduler()
```

#### **Performance Analysis**
```python
# Generate comprehensive performance report
report_file = agent.generate_performance_report()
print(f"Report saved to: {report_file}")

# Get metrics summary
summary = agent.data_logger.get_metrics_summary(hours=24)
print(f"Best performing band: {summary['best_performing_band']}")
```

#### **Band Configuration Management**
```python
# Get current band configuration
config = agent.get_current_band_config()
print(f"Current config: {config}")

# Set specific configuration
band_config = {
    'Band3': True,
    'Band7': False,
    'Band20': False,
    'Band8': False
}
success = agent.set_band_configuration(band_config)
```

### **6. Monitoring and Logging**

#### **Real-time Monitoring**
- **Signal Metrics**: RSRP, RSRQ, SINR, RSSI
- **Quality Assessment**: Excellent/Good/Fair/Poor
- **Band Information**: Current band, cell ID, PLMN
- **Performance Tracking**: Bandwidth scores and stability

#### **Data Logging**
- **CSV Format**: `lte_metrics.csv` with timestamps
- **JSON Format**: `lte_metrics.json` for complex data
- **Automatic Rotation**: Prevents log files from growing too large
- **Backup System**: Automatic backup of important data

#### **Visualizations Generated**
- **Timeline Charts**: Signal metrics over time
- **Band Comparisons**: Performance across different bands
- **Heatmaps**: Signal quality by time and band
- **Performance Dashboards**: Comprehensive summaries

### **7. Troubleshooting Common Issues**

#### **Authentication Problems**
```bash
# Check router connectivity
ping 192.168.8.1

# Verify credentials in .env file
cat .env

# Test with debug mode
python -c "from ai_agent import AIAutomationAgent; agent = AIAutomationAgent(); print(agent.authenticate())"
```

#### **No Signal Metrics**
```bash
# Check router connection
python main.py
# Select option 8: View current status

# Test signal retrieval
python test_agent.py --quick
```

#### **Band Switching Issues**
```bash
# Check available bands
python main.py
# Select option 9: Manual band switch

# Test band configuration
python apply_band_config.py
```

#### **Performance Issues**
```bash
# Reduce monitoring interval
# Edit config.py: MONITORING_CONFIG['measurement_interval'] = 60

# Check disk space
dir logs/
dir plots/

# Clean up old files
python -c "from data_logger import DataLogger; DataLogger().cleanup_old_logs()"
```

### **8. Configuration Options**

#### **Router Settings (config.py)**
```python
# Router Configuration
ROUTER_IP = "192.168.8.1"
ROUTER_USERNAME = "admin"
ROUTER_PASSWORD = "admin"

# LTE Band Configuration
LTE_BANDS = {
    'Band 1': {'freq_range': '2100 MHz', 'bandwidth': '20 MHz'},
    'Band 3': {'freq_range': '1800 MHz', 'bandwidth': '20 MHz'},
    'Band 7': {'freq_range': '2600 MHz', 'bandwidth': '20 MHz'},
    'Band 8': {'freq_range': '900 MHz', 'bandwidth': '10 MHz'},
    'Band 20': {'freq_range': '800 MHz', 'bandwidth': '10 MHz'},
}

# Monitoring Configuration
MONITORING_CONFIG = {
    'measurement_interval': 30,  # seconds
    'band_test_duration': 300,   # seconds per band
    'auto_switch_threshold': 0.8,  # 80% degradation triggers switch
    'peak_hours': {
        'morning': {'start': '07:00', 'end': '09:00'},
        'evening': {'start': '17:00', 'end': '19:00'},
    }
}
```

#### **Environment Variables (.env)**
```bash
ROUTER_IP=192.168.8.1
ROUTER_USERNAME=admin
ROUTER_PASSWORD=your_password
ROUTER_MODEL=Huawei_E5573
```

## 📊 Usage Examples

### 1. Initial Band Testing
```python
from ai_agent import AIAutomationAgent

# Initialize agent
agent = AIAutomationAgent()

# Authenticate
if agent.authenticate():
    # Test all available bands
    results = agent.test_all_bands(duration_per_band=300)
    
    # View results
    for band, performance in results.items():
        print(f"{band}: Score {performance.avg_bandwidth_score:.3f}")
```

### 2. Continuous Monitoring
```python
# Start monitoring with 30-second intervals
agent.start_continuous_monitoring(interval_seconds=30)

# The agent will automatically:
# - Log metrics to CSV/JSON
# - Switch bands when performance degrades
# - Generate visualizations
```

### 3. Peak Hour Optimization
```python
# Optimize for peak hours (7-9 AM, 5-7 PM)
agent.optimize_for_peak_hours()

# Schedule automatic optimization
agent.schedule_optimization()
agent.run_scheduler()
```

### 4. Generate Reports
```python
# Generate comprehensive performance report
report_file = agent.generate_performance_report()
print(f"Report saved to: {report_file}")
```

## 🎯 **Complete Capabilities Overview**

### **🔐 Router Control & Authentication**
- **Secure Web Interface Access**: Connect to Huawei routers via `http://192.168.8.1`
- **Hidden Firmware Bypass**: Access features not available in standard web UI
- **Direct API Control**: Use router's internal APIs for precise band control
- **Session Management**: Maintain authenticated sessions for continuous operations
- **Multi-router Support**: Support for different Huawei router models

### **📡 Signal Monitoring & Analysis**
- **Real-time Metrics**: Live tracking of RSRP, RSRQ, SINR, and RSSI
- **Signal Quality Assessment**: Automatic scoring (Excellent/Good/Fair/Poor)
- **Performance Benchmarking**: Comprehensive analysis of band performance
- **Historical Data Analysis**: Learn from past performance patterns
- **Trend Detection**: Identify performance trends over time

### **🤖 AI Intelligence & Optimization**
- **Learning Algorithms**: Improve decisions based on historical data
- **Predictive Switching**: Anticipate performance degradation
- **Multi-factor Analysis**: Consider all signal metrics together
- **Weighted Scoring**: Prioritize metrics based on usage patterns
- **Risk Assessment**: Avoid switching to potentially worse bands
- **Pattern Recognition**: Identify optimal bands for different times

### **⚡ Band Testing & Configuration**
- **Individual Band Testing**: Test each LTE band separately
- **Performance Benchmarking**: Comprehensive analysis of each band
- **Band Locking**: Lock to specific bands for controlled testing
- **Stability Analysis**: Measure signal stability over time
- **Direct Band Control**: Set specific configurations like `client.net.set_lte_band()`
- **Batch Operations**: Apply multiple band settings at once

### **⏰ Peak Hour Intelligence**
- **Time-based Optimization**: Different strategies for peak vs off-peak hours
- **Peak Hours**: 7-9 AM and 5-7 PM (configurable)
- **Bandwidth Focus**: Optimize for maximum bandwidth during peak hours
- **Stability Focus**: Optimize for signal stability during off-peak hours
- **Automatic Scheduling**: Schedule optimization at specific times

### **📊 Data Management & Visualization**
- **CSV Logging**: Structured data logging with timestamps
- **JSON Logging**: Flexible JSON format for complex data
- **Automatic Rotation**: Prevent log files from growing too large
- **Data Compression**: Efficient storage of historical data
- **Backup Systems**: Automatic backup of important data
- **Professional Reports**: PDF reports with all visualizations
- **Interactive Charts**: Timeline charts, band comparisons, heatmaps
- **Performance Dashboards**: Comprehensive performance summaries

### **🔄 Multi-threading & Automation**
- **Background Monitoring**: Monitor signals without blocking interface
- **Concurrent Operations**: Run multiple operations simultaneously
- **Thread Safety**: Safe concurrent access to router APIs
- **Automatic Optimization**: Continuous optimization without user intervention
- **Smart Scheduling**: Automatic optimization at peak hours

### **🎮 User Interface & Experience**
- **Interactive Menu**: Easy-to-use command-line interface
- **Colored Output**: Clear visual feedback on operations
- **Real-time Status**: Live updates of signal quality and band information
- **Error Handling**: Robust error handling and recovery
- **Progress Indicators**: Visual progress for long-running operations

## 📈 Signal Metrics Explained

### RSRP (Reference Signal Received Power)
- **Range**: -140 to -44 dBm
- **Excellent**: -80 dBm or higher
- **Good**: -90 to -80 dBm
- **Fair**: -100 to -90 dBm
- **Poor**: Below -100 dBm

### RSRQ (Reference Signal Received Quality)
- **Range**: -20 to -3 dB
- **Excellent**: -10 dB or higher
- **Good**: -15 to -10 dB
- **Fair**: -20 to -15 dB
- **Poor**: Below -20 dB

### SINR (Signal-to-Interference-plus-Noise Ratio)
- **Range**: -10 to 30 dB
- **Excellent**: 20 dB or higher
- **Good**: 13 to 20 dB
- **Fair**: 0 to 13 dB
- **Poor**: Below 0 dB

## 🔧 Configuration

### Router Settings (`config.py`)
```python
# Router Configuration
ROUTER_IP = "192.168.8.1"
ROUTER_USERNAME = "admin"
ROUTER_PASSWORD = "admin"

# LTE Band Configuration
LTE_BANDS = {
    'Band 1': {'freq_range': '2100 MHz', 'bandwidth': '20 MHz'},
    'Band 3': {'freq_range': '1800 MHz', 'bandwidth': '20 MHz'},
    'Band 7': {'freq_range': '2600 MHz', 'bandwidth': '20 MHz'},
    # ... more bands
}

# Monitoring Configuration
MONITORING_CONFIG = {
    'measurement_interval': 30,  # seconds
    'band_test_duration': 300,   # seconds per band
    'auto_switch_threshold': 0.8,  # 80% degradation triggers switch
}
```

### Environment Variables (`.env`)
```bash
ROUTER_IP=192.168.8.1
ROUTER_USERNAME=admin
ROUTER_PASSWORD=your_password
```

## 📁 File Structure

```
router/
├── main.py                 # Main application with interactive menu
├── ai_agent.py            # Core AI automation agent
├── huawei_router.py       # Router interface and API calls
├── data_logger.py         # Data logging and analysis
├── visualization.py        # Charts, graphs, and reports
├── config.py              # Configuration settings
├── apply_band_config.py   # Quick band configuration script
├── test_agent.py          # Comprehensive testing suite
├── demo.py                # Feature demonstration script
├── requirements.txt       # Python dependencies
├── env_example.txt       # Environment variables example
├── README.md             # This documentation
├── logs/                 # Generated log files
├── plots/                # Generated visualizations
└── reports/              # Generated reports
```

## 📊 Output Files

### Logs
- `lte_metrics.csv` - Signal metrics in CSV format
- `lte_metrics.json` - Signal metrics in JSON format
- `lte_agent.log` - Application log file

### Visualizations
- `signal_timeline_*.png` - Signal metrics over time
- `band_comparison_*.png` - Band performance comparison
- `signal_heatmap_*.png` - Signal quality heatmap
- `performance_dashboard_*.png` - Performance dashboard

### Reports
- `lte_analysis_report_*.pdf` - Comprehensive performance report

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check router IP address
   - Verify username/password
   - Ensure network connectivity

2. **No Signal Metrics**
   - Check if router is connected to LTE network
   - Verify router supports the API endpoints
   - Check router firmware version

3. **Band Switching Not Working**
   - Some routers may not support band locking
   - Check router model compatibility
   - Verify band availability in your area

4. **Performance Issues**
   - Reduce monitoring interval
   - Check available memory/disk space
   - Optimize logging configuration

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug output
agent = AIAutomationAgent()
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Use responsibly and in accordance with your router's terms of service. The authors are not responsible for any damage to equipment or service interruptions.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `lte_agent.log`
3. Open an issue with detailed information
4. Include router model and firmware version

## 🔄 Updates

- **v1.0.0**: Initial release with basic functionality
- **v1.1.0**: Added visualization and reporting features
- **v1.2.0**: Enhanced AI optimization algorithms
- **v1.3.0**: Added peak hour optimization and scheduling

## 🎉 **Success Metrics & Achievements**

### **✅ What This Project Successfully Accomplishes**

#### **🔓 Router Access & Control**
- **Bypasses Router Limitations**: Access hidden firmware features not available in web UI
- **Direct Band Control**: Set specific band configurations like your `client.net.set_lte_band()` format
- **Secure Authentication**: Maintain secure connections to router APIs
- **Multi-band Management**: Control multiple LTE bands simultaneously

#### **📈 Signal Optimization**
- **Performance Improvement**: Automatically select the best performing LTE bands
- **Real-time Monitoring**: Continuously track signal quality and performance
- **Intelligent Switching**: Switch bands when performance degrades
- **Peak Hour Optimization**: Different strategies for peak vs off-peak usage

#### **🤖 AI Intelligence**
- **Learning Capabilities**: Improve decisions based on historical performance data
- **Predictive Analysis**: Anticipate performance issues before they occur
- **Pattern Recognition**: Identify optimal bands for different times and conditions
- **Risk Management**: Avoid switching to potentially worse bands

#### **📊 Data & Analytics**
- **Comprehensive Logging**: Track all signal metrics over time
- **Professional Reports**: Generate PDF reports with visualizations
- **Performance Analysis**: Detailed analysis of band performance
- **Historical Trends**: Learn from past performance patterns

#### **🎮 User Experience**
- **Easy-to-Use Interface**: Simple menu-driven interface with colored output
- **Multiple Operation Modes**: Interactive, automated, and direct configuration modes
- **Robust Error Handling**: Graceful handling of network issues and errors
- **Real-time Feedback**: Live updates on signal quality and operations

### **🚀 Key Achievements**

✅ **Bypasses router limitations** and accesses hidden firmware features  
✅ **Optimizes LTE signal quality** through intelligent band selection  
✅ **Provides real-time monitoring** with comprehensive logging  
✅ **Automates peak hour optimization** for maximum performance  
✅ **Supports your exact band configuration** format  
✅ **Generates professional reports** with visualizations  
✅ **Offers both interactive and automated** operation modes  
✅ **Implements AI intelligence** for predictive optimization  
✅ **Provides multi-threading** for background operations  
✅ **Ensures robust error handling** and recovery  

---

**🎯 This is a complete LTE optimization solution that transforms your Huawei router into an intelligent, self-optimizing device! 📡✨** 