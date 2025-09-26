"""
Scheduler for WhatsApp Bot
=========================
Alternative scheduling solution using Python's schedule library.
Runs the bot 5 times daily at specified intervals.

Usage:
    python scheduler.py

Note: This is an alternative to using Windows Task Scheduler or cron jobs.
"""

import schedule
import time
import logging
from datetime import datetime
from whatsapp_bot import WhatsAppBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class BotScheduler:
    """Scheduler class to manage automated bot runs."""
    
    def __init__(self):
        self.bot = None
        self.run_count = 0
    
    def run_scheduled_task(self):
        """Execute a scheduled bot run."""
        self.run_count += 1
        logger.info(f"🚀 Starting scheduled run #{self.run_count}")
        
        try:
            # Create a new bot instance for each run
            self.bot = WhatsAppBot()
            success = self.bot.run_bot_cycle()
            
            if success:
                logger.info(f"✅ Scheduled run #{self.run_count} completed successfully")
            else:
                logger.warning(f"⚠️ Scheduled run #{self.run_count} completed with issues")
                
        except Exception as e:
            logger.error(f"❌ Scheduled run #{self.run_count} failed: {e}")
        
        logger.info(f"📊 Total runs today: {self.run_count}")
    
    def setup_schedule(self):
        """Set up the daily schedule - 5 times per day."""
        
        # Define the 5 daily run times
        run_times = ["08:00", "11:00", "14:00", "17:00", "20:00"]
        
        logger.info("⏰ Setting up daily schedule:")
        for run_time in run_times:
            schedule.every().day.at(run_time).do(self.run_scheduled_task)
            logger.info(f"   - {run_time}")
        
        logger.info(f"✅ Scheduled {len(run_times)} daily runs")
    
    def run_scheduler(self):
        """Main scheduler loop."""
        logger.info("🤖 WhatsApp Bot Scheduler Starting")
        logger.info(f"📅 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.setup_schedule()
        
        # Show next scheduled runs
        logger.info("📋 Next scheduled runs:")
        for job in schedule.jobs:
            logger.info(f"   - {job.next_run}")
        
        logger.info("🔄 Scheduler running... (Press Ctrl+C to stop)")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("🛑 Scheduler stopped by user")
        except Exception as e:
            logger.error(f"❌ Scheduler error: {e}")

def main():
    """Main function to start the scheduler."""
    scheduler = BotScheduler()
    scheduler.run_scheduler()

if __name__ == "__main__":
    main()
