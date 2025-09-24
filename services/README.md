This folder contains extensions that make OTC Ops Copilot useful in day-to-day ops beyond ad-hoc queries.

We’ll cover all 3 files:

scheduler.py → for scheduling queries/reports (APScheduler).

report_generator.py → for PDF/Excel report generation.

notifier.py → for sending reports via email/Slack.

✅ Summary of services/

scheduler.py

Uses APScheduler for cron-like jobs.

Executes reports → generates PDFs/Excels → notifies users.

report_generator.py

Creates PDF reports (WeasyPrint).

Creates Excel reports (pandas → Excel).

notifier.py

Sends reports via email (SMTP).

Sends alerts to Slack via webhook.
