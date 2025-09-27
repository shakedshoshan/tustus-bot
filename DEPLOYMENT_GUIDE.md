# 🚀 WhatsApp Bot - GitHub Actions Deployment Guide

This guide shows you how to deploy your WhatsApp bot using GitHub Actions for completely free, automated scheduling.

## 🎯 **Why GitHub Actions?**

- ✅ **Completely Free** for public repositories
- ✅ **Built-in Cron Scheduling** (5 times daily)
- ✅ **No server maintenance** required
- ✅ **Automatic Chrome/ChromeDriver setup**
- ✅ **Easy to monitor and debug**
- ✅ **Runs on GitHub's reliable infrastructure**

## 📋 **Prerequisites**

1. **GitHub Account** (free)
2. **Resend API Key** (from your existing setup)
3. **Target Website URL** (already configured)

## 🚀 **Quick Setup (3 Steps)**

### Step 1: Push Your Code to GitHub

```bash
git add .
git commit -m "Add GitHub Actions deployment"
git push origin main
```

### Step 2: Set Up GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `SECRETS_TARGET_URL` | `https://www.tustus.co.il/Arkia/Home` | Website to scrape |
| `RESEND_API_KEY` | `re_C3uDPvQ3_JPsxnE6RiABMDucv8UUwMPW7` | Your Resend API key |
| `FROM_EMAIL` | `onboarding@resend.dev` | Sender email |
| `TO_EMAIL` | `shakedshoshan8@gmail.com` | Your email |
| `EMAIL_SUBJECT` | `Tustus Destinations Update` | Email subject |
| `REQUEST_TIMEOUT` | `30` | Request timeout in seconds |

### Step 3: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. The workflow will run automatically on schedule
3. You can also trigger it manually by clicking **Run workflow**

## ⏰ **Schedule Times**

Your bot will run automatically 5 times daily:

| UTC Time | Israel Time | Purpose |
|----------|-------------|---------|
| 8:00 AM | 10:00 AM | Morning update |
| 11:00 AM | 1:00 PM | Lunch break check |
| 2:00 PM | 4:00 PM | Afternoon update |
| 5:00 PM | 7:00 PM | Evening check |
| 8:00 PM | 10:00 PM | Night update |

## 🔍 **Monitoring Your Bot**

### View Execution Logs:
1. Go to **Actions** tab in your repository
2. Click on any workflow run to see detailed logs
3. Check the **Run WhatsApp Bot** step for execution details

### Manual Triggering:
1. Go to **Actions** tab
2. Click **🤖 WhatsApp Bot - Tustus Scraper**
3. Click **Run workflow** button
4. Select branch and click **Run workflow**

## 🛠️ **Troubleshooting**

### Common Issues:

1. **❌ Environment Variables Not Set:**
   - Check that all secrets are added in Settings → Secrets
   - Verify secret names match exactly (case-sensitive)

2. **❌ Chrome/ChromeDriver Issues:**
   - GitHub Actions handles this automatically
   - Check the "Install ChromeDriver" step in logs

3. **❌ Email Sending Issues:**
   - Verify Resend API key is valid
   - Check email addresses are correct
   - Look for error messages in the bot execution logs

4. **❌ Website Scraping Issues:**
   - Check if the target website is accessible
   - Verify the website structure hasn't changed
   - Look for timeout errors in logs

### Debug Steps:

1. **Check Workflow Logs:**
   - Go to Actions → Click on failed run
   - Expand each step to see detailed output

2. **Test Locally:**
   ```bash
   python whatsapp_bot.py
   ```

3. **Validate Environment:**
   - The workflow includes a validation step
   - Check if all required secrets are set

## 🔧 **Workflow Features**

### What the GitHub Actions workflow does:

1. **🔧 System Setup:**
   - Installs Chrome browser
   - Installs ChromeDriver
   - Sets up Python 3.11

2. **📦 Dependencies:**
   - Installs all Python packages
   - Caches pip dependencies for faster runs

3. **🔍 Validation:**
   - Checks all required environment variables
   - Fails early if configuration is missing

4. **🤖 Bot Execution:**
   - Runs your WhatsApp bot
   - Captures all output and errors

5. **📊 Logging:**
   - Uploads execution logs as artifacts
   - Keeps logs for 7 days
   - Shows clear success/failure status

## 📈 **Performance Optimizations**

The workflow is optimized for:
- **Fast execution** (10-minute timeout)
- **Efficient caching** (pip dependencies cached)
- **Clean environment** (fresh Ubuntu runner each time)
- **Resource cleanup** (automatic cleanup after execution)

## 🎉 **You're All Set!**

Your WhatsApp bot will now:
- ✅ Run automatically 5 times daily
- ✅ Scrape the Tustus website
- ✅ Send you email updates
- ✅ Handle errors gracefully
- ✅ Provide detailed logs

**No more manual running required!** 🚀

## 📞 **Need Help?**

If you encounter issues:
1. Check the workflow logs in the Actions tab
2. Verify all secrets are set correctly
3. Test locally first with `python whatsapp_bot.py`
4. Check the troubleshooting section above

Your bot is now running in the cloud! 🌟
