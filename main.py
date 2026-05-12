from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time
import re
import smtplib
from email.message import EmailMessage

# Load environment variables
load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# Store emails
emails_found = []

# Email regex
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    # -------------------------
    # LOGIN LINKEDIN
    # -------------------------

    print("Opening LinkedIn...")

    page.goto("https://www.linkedin.com/login")

    time.sleep(3)

    page.fill("#username", LINKEDIN_EMAIL)

    page.fill("#password", LINKEDIN_PASSWORD)

    page.click("button[type='submit']")

    print("Logged into LinkedIn")

    time.sleep(5)

    # -------------------------
    # SEARCH POSTS
    # -------------------------

    print("Searching jobs...")

    keyword = "Java Developer Contract"

    url = f"https://www.linkedin.com/search/results/content/?keywords={keyword}"

    page.goto(url)

    time.sleep(5)

    # Scroll page
    for i in range(5):

        page.mouse.wheel(0, 5000)

        print(f"Scrolling {i+1}")

        time.sleep(3)

    # Get page content
    content = page.content()

    # Extract recruiter emails
    found_emails = re.findall(email_pattern, content)

    for email in found_emails:

        if email not in emails_found:

            emails_found.append(email)

    # Demo email if none found
    if len(emails_found) == 0:

        emails_found.append("samplehr@gmail.com")

    print("Recruiter Emails Found:")

    print(emails_found)

    print(f"Total Emails: {len(emails_found)}")

    # -------------------------
    # SEND EMAILS
    # -------------------------

    print("Sending applications...")

    for recruiter_email in emails_found:

        msg = EmailMessage()

        msg["Subject"] = "Application for Java Developer Role"

        msg["From"] = GMAIL_EMAIL

        msg["To"] = recruiter_email

        body = """
Dear Recruiter,

I hope you are doing well.

I came across your LinkedIn post regarding the Java Developer opportunity.

Please find my resume attached for your consideration.

Thank you for your time.

Best Regards,
Your Name
"""

        msg.set_content(body)

        # Attach Resume
        with open("resume.pdf", "rb") as f:

            file_data = f.read()

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="pdf",
            filename="resume.pdf"
        )

        # Send Email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)

            smtp.send_message(msg)

        print(f"Application sent to {recruiter_email}")

    print("Application sent successfully")

    print("Process completed")

    time.sleep(5)

    browser.close()