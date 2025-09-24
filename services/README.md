 Here’s the services/README.md that explains what happens in the services
---

📂 services/ – Scheduling, Reporting & Notifications

The services/ folder extends OTC Ops Copilot beyond ad-hoc queries.
It adds capabilities for scheduling, report generation, and notifications, so ops teams can automate daily/weekly workflows.


---

📌 Files & Responsibilities

🔹 scheduler.py

Uses APScheduler to run jobs at specific times.

Key functions:

schedule_report(report_name, question, schedule_time, backend, recipients)
→ schedules a job (daily at schedule_time).

run_scheduled_report(report_name, question, backend, recipients)
→ executes pipeline: query → SQL → results → generate PDF → send email/Slack.


Example:

from services.scheduler import schedule_report
schedule_report("Daily Trades", "Show confirmed trades today", "09:00", backend="chroma", recipients=["ops@bank.com"])



---

🔹 report_generator.py

Generates PDF and Excel reports from SQL results.

Uses:

WeasyPrint → converts HTML tables into PDFs.

pandas → exports Excel files.


Key functions:

generate_pdf(report_name, sql, df) → creates PDF.

generate_excel(report_name, df) → creates Excel.


Output stored in ./reports/.



---

🔹 notifier.py

Sends reports to users via Email or Slack.

Email:

Uses SMTP (configure server, port, user, pass).

Supports attachments (PDF/Excel).


Slack:

Uses a Webhook URL to post messages.


Key functions:

send_email(recipients, subject, body, attachment)

send_slack(webhook_url, message)




---

📌 Flow of Control

1. Ops schedules a report in UI (app/pages/reports.py).


2. scheduler.py registers a job (e.g., every day at 9:00).


3. At runtime:

Engine runs NL → SQL → DB → results.

report_generator.py creates PDF/Excel.

notifier.py sends it to recipients (Email/Slack).



4. Ops receives report in inbox/Slack.




---

📌 Example Usage

from services.scheduler import schedule_report

# Schedule a daily report
schedule_report(
    report_name="Daily Trade Summary",
    question="Show total confirmed trades grouped by counterparty",
    schedule_time="08:30",
    backend="weaviate",
    recipients=["ops-team@bank.com"]
)


---

📌 Benefits for Ops Teams

No manual queries → Reports auto-delivered.

Consistency → Same queries run daily/weekly.

Auditability → SQL stored in report.

Flexibility → Works with ChromaDB, Weaviate, or Graph retrievers.



---

✅ In short:
The services/ folder makes OTC Ops Copilot not just interactive, but also a hands-off reporting assistant for operations teams.


---
