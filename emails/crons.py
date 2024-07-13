from django_cron import CronJobBase, Schedule
from .utils import fetch_emails


class FetchEmailsCronJob(CronJobBase):
    RUN_EVERY_MINS = 5  # every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'emails.fetch_emails_cron_job'

    def do(self):
        fetch_emails()
