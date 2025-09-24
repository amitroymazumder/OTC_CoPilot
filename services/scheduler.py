from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from core.engine import Engine
from services import report_generator, notifier

# Global scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def run_scheduled_report(report_name, question, backend="chroma", recipients=None):
    """
    Executes a scheduled report:
    - Runs query
    - Generates PDF
    - Sends notification
    """
    engine = Engine(backend=backend)
    output = engine.ask(question)

    if "error" in output:
        print(f"[ERROR] Report {report_name}: {output['error']}")
        return

    # Generate report file
    filepath = report_generator.generate_pdf(report_name, output["sql"], output["result"])

    # Send notification (email/slack)
    if recipients:
        notifier.send_email(recipients, subject=f"OTC Report: {report_name}", attachment=filepath)

    print(f"[OK] Report {report_name} executed at {datetime.now()}")

def schedule_report(report_name, question, schedule_time, backend="chroma", recipients=None):
    """
    Schedule a report at a given time daily.
    Example: schedule_time = "09:00"
    """
    hour, minute = map(int, str(schedule_time).split(":"))

    scheduler.add_job(
        run_scheduled_report,
        "cron",
        hour=hour,
        minute=minute,
        args=[report_name, question, backend, recipients],
        id=f"report_{report_name}",
        replace_existing=True
    )
    print(f"[OK] Scheduled report '{report_name}' at {schedule_time} daily")
