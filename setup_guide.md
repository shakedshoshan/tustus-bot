# 🚀 Quick Setup Guide

## Step-by-Step Setup (15 minutes)

### 1. Install Dependencies (5 minutes)

```bash
# Install Python packages
pip install -r requirements.txt

# Download ChromeDriver
# Go to: https://chromedriver.chromium.org/
# Download version matching your Chrome browser
# Place chromedriver.exe in project folder
```

### 2. Twilio WhatsApp Setup (5 minutes)

1. **Create Account**: [Twilio Console](https://console.twilio.com/)
2. **Go to WhatsApp Sandbox**: Console → Messaging → Try it out → Send a WhatsApp message
3. **Join Sandbox**: Send the code (e.g., "join <word>") to +1 415 523 8886
4. **Get Credentials**: Copy Account SID and Auth Token

### 3. Configure Bot (3 minutes)

```bash
# Copy template
copy env.example .env

# Edit .env file with:
SECRETS_TARGET_URL=https://your-website.com
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_token
MY_PHONE_NUMBER=whatsapp:+1234567890
```

### 4. Customize Scraping (2 minutes)

Edit `whatsapp_bot.py` line ~150 in `_extract_target_data()`:

```python
# Replace this with your website's selectors
items = self.driver.find_elements(By.CSS_SELECTOR, "your-selector-here")
```

### 5. Test Run

```bash
python whatsapp_bot.py
```

## 🎯 Quick Selector Guide

| Website Element | CSS Selector Example |
|----------------|---------------------|
| News Headlines | `"h2.headline"` |
| List Items | `"ul li"` or `".list-item"` |
| Product Names | `".product-title"` |
| Prices | `".price"` |
| Table Data | `"table tr td"` |

## 🔧 Common Fixes

**No data found?** → Update CSS selectors
**ChromeDriver error?** → Download correct version
**WhatsApp not working?** → Join Twilio sandbox first
**Permission error?** → Run as administrator

---
**Need help?** Check the full README.md for detailed instructions.
