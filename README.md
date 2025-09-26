# 🤖 Personal WhatsApp Bot

A powerful Python bot that scrapes data from websites using Selenium and sends automated WhatsApp messages via the Twilio API. Perfect for daily updates, monitoring, and personal automation tasks.

## 🚀 Features

- **Web Scraping**: Uses Selenium WebDriver for dynamic content extraction
- **WhatsApp Integration**: Reliable messaging through Twilio's WhatsApp API
- **Headless Operation**: Runs silently in the background
- **Error Handling**: Comprehensive error handling and notifications
- **Configurable**: Easy setup through environment variables
- **Scheduling Ready**: Perfect for automated daily runs

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+** installed on your machine
- **Google Chrome** browser installed
- **ChromeDriver** compatible with your Chrome version
- **Twilio Account** with WhatsApp Sandbox access

## 🛠️ Installation

### 1. Clone or Download the Project

```bash
git clone <your-repo-url>
cd whatsapp-bot
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download ChromeDriver

1. Check your Chrome version: `chrome://version/`
2. Download matching ChromeDriver from [ChromeDriver Downloads](https://chromedriver.chromium.org/)
3. Extract and place `chromedriver.exe` in your project folder or system PATH

### 4. Set Up Twilio WhatsApp

1. **Create Twilio Account**: Sign up at [Twilio Console](https://console.twilio.com/)
2. **Access WhatsApp Sandbox**: Go to Messaging → Try it out → Send a WhatsApp message
3. **Join Sandbox**: Send the provided code to the Twilio WhatsApp number
4. **Get Credentials**: Note your Account SID and Auth Token

### 5. Configure Environment Variables

1. Copy the example configuration:
   ```bash
   copy env.example .env
   ```

2. Edit `.env` with your actual values:
   ```env
   TARGET_URL=https://your-target-website.com
   CHROME_DRIVER_PATH=chromedriver.exe
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   MY_PHONE_NUMBER=whatsapp:+1234567890
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TARGET_URL` | Website to scrape | `https://example.com/data` |
| `CHROME_DRIVER_PATH` | Path to ChromeDriver | `chromedriver.exe` |
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID | `ACxxxxxxxxxxxxx` |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token | `your_token_here` |
| `MY_PHONE_NUMBER` | Your WhatsApp number | `whatsapp:+1234567890` |

### Customizing Data Extraction

The bot includes a template for data extraction in the `_extract_target_data()` method. You'll need to customize this based on your target website:

```python
def _extract_target_data(self):
    """Customize this method for your specific website."""
    
    # Example: Extract from list items
    items = self.driver.find_elements(By.CSS_SELECTOR, "ul.your-list li")
    return [item.text.strip() for item in items if item.text.strip()]
```

### Common Selectors

- **Lists**: `"ul li"`, `"ol li"`, `".list-item"`
- **Tables**: `"table tr td"`, `".table-row .cell"`
- **Cards**: `".card"`, `".item"`, `".post"`
- **Specific Classes**: `".your-target-class"`

## 🏃‍♂️ Usage

### Manual Run

```bash
python whatsapp_bot.py
```

### Test Configuration

```python
from config import Config
Config.print_configuration()
```

## 📅 Scheduling (5 Times Daily)

### Windows Task Scheduler

1. Open **Task Scheduler**
2. Click **Create Basic Task**
3. Set trigger to **Daily**
4. Create 5 separate tasks for different times:
   - 8:00 AM
   - 11:00 AM
   - 2:00 PM
   - 5:00 PM
   - 8:00 PM

**Action Settings:**
- **Program**: `C:\Python\python.exe` (your Python path)
- **Arguments**: `C:\path\to\whatsapp_bot.py`
- **Start in**: `C:\path\to\project\folder`

### Linux/Mac Cron

Add to crontab (`crontab -e`):

```bash
# WhatsApp Bot - 5 times daily
0 8,11,14,17,20 * * * cd /path/to/bot && /usr/bin/python3 whatsapp_bot.py
```

### Using Python Schedule (Alternative)

Create `scheduler.py`:

```python
import schedule
import time
from whatsapp_bot import WhatsAppBot

def run_bot():
    bot = WhatsAppBot()
    bot.run_bot_cycle()

# Schedule 5 times daily
schedule.every().day.at("08:00").do(run_bot)
schedule.every().day.at("11:00").do(run_bot)
schedule.every().day.at("14:00").do(run_bot)
schedule.every().day.at("17:00").do(run_bot)
schedule.every().day.at("20:00").do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🔧 Troubleshooting

### Common Issues

**❌ ChromeDriver not found**
```
Solution: Ensure ChromeDriver is in PATH or update CHROME_DRIVER_PATH in .env
```

**❌ Twilio authentication failed**
```
Solution: Verify Account SID and Auth Token in Twilio Console
```

**❌ WhatsApp message not received**
```
Solution: 
1. Ensure you've joined the Twilio WhatsApp Sandbox
2. Verify phone number format: whatsapp:+1234567890
3. Check Twilio Console for message logs
```

**❌ No data scraped**
```
Solution: 
1. Check if target website is accessible
2. Update CSS selectors in _extract_target_data()
3. Increase wait time for dynamic content
```

### Debug Mode

Enable verbose logging by modifying the script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📁 Project Structure

```
whatsapp-bot/
│
├── whatsapp_bot.py      # Main bot script
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── env.example         # Environment variables template
├── .env                # Your actual environment variables (create this)
├── README.md           # This file
└── scheduler.py        # Optional scheduling script
```

## 🔒 Security Notes

- **Never commit your `.env` file** to version control
- **Keep your Twilio credentials secure**
- **Use environment variables** for all sensitive data
- **Regularly rotate your API tokens**

## 🤝 Customization Examples

### Example 1: News Headlines

```python
def _extract_target_data(self):
    headlines = self.driver.find_elements(By.CSS_SELECTOR, "h2.headline a")
    return [headline.text.strip() for headline in headlines[:10]]
```

### Example 2: Stock Prices

```python
def _extract_target_data(self):
    stocks = self.driver.find_elements(By.CSS_SELECTOR, ".stock-item")
    data = []
    for stock in stocks:
        name = stock.find_element(By.CSS_SELECTOR, ".stock-name").text
        price = stock.find_element(By.CSS_SELECTOR, ".stock-price").text
        data.append(f"{name}: {price}")
    return data
```

### Example 3: Weather Updates

```python
def _extract_target_data(self):
    temp = self.driver.find_element(By.CSS_SELECTOR, ".temperature").text
    condition = self.driver.find_element(By.CSS_SELECTOR, ".condition").text
    return [f"Temperature: {temp}", f"Condition: {condition}"]
```

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Verify your environment variables
3. Test with a simple website first
4. Check Twilio Console for API errors

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Happy Automating! 🚀**

*Made with ❤️ for personal automation and productivity*
