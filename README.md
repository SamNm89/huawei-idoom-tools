# Huawei LTE Router AI Automation Agent

An intelligent Python tool that **bypasses router limitations** and **optimizes LTE signal quality** through automated band switching and real-time monitoring.

## 🚀 Quick Start

### 1. Setup
```bash
# Clone and enter directory
git clone <repository-url>
cd router

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure router credentials
cp env_example.txt .env
# Edit .env with your router details
```

### 2. Run

**Option A: Quick Start (Recommended)**
```bash
# Windows - Double click or run:
start.bat

# Or PowerShell:
.\start.ps1
```

**Option B: Manual Commands**
```bash
# Interactive mode
python main.py

# Or automated mode
python main.py --automated
```

## 🎯 What It Does

- **Bypasses router limitations** - Access hidden firmware features
- **Optimizes LTE bands** - Automatically selects best performing bands
- **Real-time monitoring** - Tracks signal quality (RSRP, RSRQ, SINR, RSSI)
- **Peak hour optimization** - Different strategies for busy vs quiet times
- **Professional reports** - Generates PDF reports with visualizations
- **Direct band control** - Set specific configurations like `client.net.set_lte_band()`

## 📋 Requirements

- Python 3.8+
- Huawei LTE router (E5573, E5785, or similar)
- Network connection to router (192.168.8.1)

## 🛠️ Usage

### Quick Start Scripts (Windows)

**For easiest setup, use the provided scripts:**

```bash
# Double click or run:
start.bat

# Or PowerShell:
.\start.ps1
```

**What the scripts do:**
- ✅ Automatically create virtual environment if needed
- ✅ Install dependencies automatically
- ✅ Create `.env` file from template
- ✅ Activate virtual environment
- ✅ Start the application

### Interactive Mode
```bash
python main.py
```
Choose from menu options:
- Test all LTE bands
- Start monitoring
- Generate reports
- Optimize for peak hours
- Manual band switching

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

# Run everything
python main.py --automated
```

### Direct Band Configuration
```bash
# Apply your specific band configuration
python apply_band_config.py
```

## 🔧 Configuration

### Router Settings (`config.py`)
```python
ROUTER_IP = "192.168.8.1"
ROUTER_USERNAME = "admin"
ROUTER_PASSWORD = "admin"

LTE_BANDS = {
    'Band 3': {'freq_range': '1800 MHz', 'bandwidth': '20 MHz'},
    'Band 7': {'freq_range': '2600 MHz', 'bandwidth': '20 MHz'},
    'Band 20': {'freq_range': '800 MHz', 'bandwidth': '10 MHz'},
}
```

### Environment Variables (`.env`)
```bash
ROUTER_IP=192.168.8.1
ROUTER_USERNAME=admin
ROUTER_PASSWORD=your_password
```

## 📊 Signal Metrics

| Metric | Excellent | Good | Fair | Poor |
|--------|-----------|------|------|------|
| RSRP | -80 dBm+ | -90 to -80 | -100 to -90 | < -100 |
| RSRQ | -10 dB+ | -15 to -10 | -20 to -15 | < -20 |
| SINR | 20 dB+ | 13 to 20 | 0 to 13 | < 0 |

## 🔍 Troubleshooting

### Common Issues

**Virtual Environment Problems:**
```bash
# Make sure it's activated (you'll see (.venv) in prompt)
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac
```

**Authentication Failed:**
```bash
# Check router connectivity
ping 192.168.8.1

# Verify .env file has correct credentials
```

**Unicode Error:**
```bash
# Save .env file with UTF-8 encoding
# Use Notepad++ or similar editor
```

**No Signal Metrics:**
```bash
# Check if router is connected to LTE
# Verify router supports the API endpoints
```

## 📁 File Structure

```
router/
├── main.py                 # Main application
├── ai_agent.py            # Core automation agent
├── huawei_router.py       # Router interface
├── data_logger.py         # Data logging
├── visualization.py        # Charts and reports
├── config.py              # Configuration
├── apply_band_config.py   # Quick band setup
├── start.bat              # Windows batch startup script
├── start.ps1              # PowerShell startup script
├── requirements.txt       # Dependencies
├── .env                   # Router credentials
└── logs/                  # Generated logs
```

## 🎉 Key Features

✅ **Bypasses router limitations** and accesses hidden features  
✅ **Optimizes LTE signal quality** through intelligent band selection  
✅ **Real-time monitoring** with comprehensive logging  
✅ **Peak hour optimization** for maximum performance  
✅ **Professional reports** with visualizations  
✅ **Direct band control** with your exact configuration format  
✅ **AI intelligence** for predictive optimization  
✅ **Multi-threading** for background operations  

## ⚠️ Disclaimer

This tool is for educational and research purposes. Use responsibly and in accordance with your router's terms of service.

---

**🎯 Transform your Huawei router into an intelligent, self-optimizing device! 📡✨** 