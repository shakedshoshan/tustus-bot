"""
Personal WhatsApp Bot - Python, Selenium, Twilio
==============================================
This bot scrapes data from a target website using Selenium and sends
the results to your personal WhatsApp using the Twilio API.

Author: Your Name
Created: 2025
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import resend
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
TARGET_URL = os.environ.get("TARGET_URL", "http://example.com/data")
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "30"))

# --- Resend Configuration ---
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
FROM_EMAIL = os.environ.get("FROM_EMAIL")
TO_EMAIL = os.environ.get("TO_EMAIL")
EMAIL_SUBJECT = os.environ.get("EMAIL_SUBJECT", "Tustus Destinations Update")

class WhatsAppBot:
    """Main bot class that handles web scraping and WhatsApp messaging."""
    
    def __init__(self):
        self.driver = None
        self._initialize_resend()
    
    def _initialize_driver(self):
        """Initialize Selenium WebDriver with optimal settings."""
        chrome_options = Options()
        
        # Basic Chrome options
        chrome_options.add_argument("--headless=new")  # New headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Disable unnecessary features
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-web-security")  # Allow cross-origin requests
        chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")  # Disable site isolation
        
        # Performance optimizations
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-login-animations")
        chrome_options.add_argument("--disable-prompts")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--disable-sync")
        
        # Additional options for stability and to avoid detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent to avoid detection
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36')
        
        try:
            print("🔧 Setting up Chrome WebDriver...")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Remove webdriver flag
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome WebDriver initialized successfully.")
            return True
        except Exception as e:
            print(f"❌ Error initializing WebDriver: {e}")
            return False
    
    def _initialize_resend(self):
        """Initialize Resend email client with API key."""
        if not RESEND_API_KEY:
            print("❌ Resend API key not found")
            print("ℹ️ Get your API key from: https://resend.com/dashboard/api-keys")
            raise ValueError("Resend API key not found. Please check your .env file.")
        
        if not TO_EMAIL:
            print("❌ Email configuration missing")
            print("Required environment variables:")
            print("- TO_EMAIL: Destination email address")
            raise ValueError("Email configuration missing. Please check your .env file.")
            
        # Use default Resend sender if not specified
        global FROM_EMAIL
        if not FROM_EMAIL:
            FROM_EMAIL = "onboarding@resend.dev"
            print("ℹ️ Using default Resend sender email: onboarding@resend.dev")
        
        # Initialize Resend with API key
        resend.api_key = RESEND_API_KEY
        print("✅ Resend client initialized successfully")
    
    
    def scrape_data(self, url):
        """
        Scrapes destination data from the Tustus website using Selenium.
        
        Args:
            url (str): The target website URL
            
        Returns:
            list: Extracted destination items or None if failed
        """
        if not self._initialize_driver():
            return None
        
        try:
            print(f"🌐 Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to be fully loaded
            wait = WebDriverWait(self.driver, 20)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            print("✅ Page fully loaded")
            
            # Wait for any dynamic content to load
            time.sleep(3)
            
            # Try to make the dropdown visible using JavaScript
            print("🔧 Trying to show dropdown...")
            self.driver.execute_script("""
                // Remove any hidden class and show the dropdown
                var dropList = document.getElementById('dropList_serach');
                if (dropList) {
                    dropList.classList.remove('hidden');
                    dropList.style.display = 'block';
                    dropList.style.visibility = 'visible';
                    dropList.style.opacity = '1';
                }
                
                // Also try to show the parent container
                var searchDiv = document.querySelector('.search_by_text');
                if (searchDiv) {
                    searchDiv.style.display = 'block';
                    searchDiv.style.visibility = 'visible';
                    searchDiv.style.opacity = '1';
                }
            """)
            
            # Extract the destinations
            extracted_data = self._extract_target_data()
            
            if extracted_data:
                print(f"✅ Successfully scraped {len(extracted_data)} destinations.")
                return extracted_data
            else:
                print("⚠️ No destinations found.")
                return []
                
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 WebDriver closed.")
    
    def _extract_target_data(self):
        """
        Extract destination data from the Tustus website using Selenium.
        
        Returns:
            list: Extracted destination items
        """
        extracted_items = []
        
        try:
            print("🔍 Looking for dropList_serach element...")
            
            # Get the dropdown list directly since we've already made it visible
            drop_list = self.driver.find_element(By.ID, "dropList_serach")
            print("✅ Found dropList_serach element")
            
            # Get the HTML content directly
            html_content = drop_list.get_attribute('innerHTML')
            print("📄 Got dropdown HTML content")
            
            # Extract destinations using string manipulation
            if html_content:
                # Split by <li> tags and clean up
                destinations = html_content.split('</li>')
                for dest in destinations:
                    # Clean up the HTML tags
                    dest = dest.replace('<li>', '').strip()
                    if dest and len(dest) > 2:
                        extracted_items.append(dest)
                        print(f"✅ Added destination from HTML: {dest}")
            
            # If no items found from HTML, try getting li elements directly
            if not extracted_items:
                print("🔍 Trying to get li elements directly...")
                li_elements = drop_list.find_elements(By.TAG_NAME, "li")
                print(f"📋 Found {len(li_elements)} li elements")
                
                for li in li_elements:
                    destination = li.text.strip()
                    if destination and len(destination) > 2:
                        extracted_items.append(destination)
                        print(f"✅ Added destination: {destination}")
                
                if extracted_items:
                    print(f"✅ Successfully extracted {len(extracted_items)} destinations")
                else:
                    print("❌ No destination items found in the dropdown")
            
            # Remove duplicates while preserving order
            seen = set()
            unique_items = []
            for item in extracted_items:
                if item not in seen:
                    seen.add(item)
                    unique_items.append(item)
            
            print(f"📊 Final result: {len(unique_items)} unique destinations")
            if unique_items:
                print(f"📋 Sample destinations: {unique_items[:3]}")
            
            return unique_items
            
        except Exception as e:
            print(f"❌ Error extracting data: {e}")
            return []
    
    def send_email_update(self, data_list):
        """
        Sends the scraped data via email using Resend API.
        
        Args:
            data_list (list): The scraped data to send
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create HTML email content
        if not data_list:
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; direction: rtl;">
                <h2 style="color: #333;">🤖 עדכון בוט - {timestamp}</h2>
                <p style="color: #dc3545; background: #ffe5e5; padding: 10px; border-radius: 5px;">
                    ❌ <strong>סטטוס:</strong> לא נמצאו יעדים
                </p>
                <p>האתר אינו זמין או שהמבנה שלו השתנה.</p>
            </div>
            """
        else:
            # Format the list nicely for HTML
            if len(data_list) > 15:
                list_preview = data_list[:15]
                list_items = "\n".join([f'<li style="padding: 10px; border-bottom: 1px solid #dee2e6;">{item}</li>' for item in list_preview])
                list_items += f'\n<li style="padding: 10px; color: #6c757d;">... ועוד {len(data_list) - 15} יעדים נוספים</li>'
            else:
                list_items = "\n".join([f'<li style="padding: 10px; border-bottom: 1px solid #dee2e6;">{item}</li>' for item in data_list])
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; direction: rtl;">
                <h2 style="color: #333;">🤖 עדכון יעדי טוסטוס - {timestamp}</h2>
                <p style="color: #28a745; background: #e8f5e9; padding: 10px; border-radius: 5px;">
                    ✅ <strong>נמצאו {len(data_list)} יעדים:</strong>
                </p>
                <ul style="list-style-type: none; padding: 0; margin: 20px 0; background: #f8f9fa; border-radius: 5px;">
                    {list_items}
                </ul>
            </div>
            """
        
        try:
            # Send email using Resend
            params = {
                "from": FROM_EMAIL,
                "to": TO_EMAIL,
                "subject": EMAIL_SUBJECT,
                "html": html_content,
            }
            
            response = resend.Emails.send(params)
            
            print(f"✅ Email sent successfully!")
            print(f"📧 Email ID: {response['id']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            
            # Try to send error notification
            try:
                error_html = f"""
                <h2>🤖 Bot Error - {timestamp}</h2>
                <p style="color: red;">❌ Failed to send scheduled update.</p>
                <p><strong>Error:</strong> {str(e)}</p>
                """
                
                resend.Emails.send({
                    "from": FROM_EMAIL,
                    "to": TO_EMAIL,
                    "subject": "Bot Error: Tustus Update Failed",
                    "html": error_html,
                })
                print("📧 Error notification email sent.")
            except:
                print("❌ Could not send error notification.")
            
            return False
    
    def run_bot_cycle(self):
        """Execute one complete bot cycle: scrape data and send WhatsApp message."""
        print(f"\n🚀 Starting bot cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Validate configuration
        if not self._validate_configuration():
            return False
        
        # Scrape data
        scraped_data = self.scrape_data(TARGET_URL)
        
        # Send email update
        success = self.send_email_update(scraped_data)
        
        print("=" * 50)
        print(f"✅ Bot cycle completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return success
    
    def _validate_configuration(self):
        """Validate that all required configuration is present."""
        required_vars = {
            "TARGET_URL": TARGET_URL,
            "RESEND_API_KEY": RESEND_API_KEY,
            "FROM_EMAIL": FROM_EMAIL,
            "TO_EMAIL": TO_EMAIL,
            "EMAIL_SUBJECT": EMAIL_SUBJECT,
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            print("❌ Missing required configuration:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\nPlease check your .env file and ensure all variables are set.")
            return False
        
        return True

def main():
    """Main function to run the WhatsApp bot."""
    try:
        bot = WhatsAppBot()
        bot.run_bot_cycle()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
