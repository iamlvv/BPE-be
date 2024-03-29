import time

import schedule

from bpsky import bpsky
from services.survey_service.survey_recipient import Survey_send_service
from smtp.email import Email
import threading


class Scheduling_send_email:
    emails_dates_url = None

    @classmethod
    def get_email_recipients_and_survey_url(cls):
        emails_and_start_date_and_url = (
            Survey_send_service.get_all_emails_dates_url_of_not_published_survey()
        )
        cls.emails_dates_url = emails_and_start_date_and_url

    @classmethod
    def send_email(cls, email, survey_url, start_date, end_date):
        Email.send_survey_url(email, survey_url, start_date, end_date)

    @classmethod
    def schedule_emails(cls):
        with bpsky.app_context():
            cls.get_email_recipients_and_survey_url()
            for item in cls.emails_dates_url:
                email = item.email
                survey_url = item.survey_url
                start_date = item.start_date
                end_date = item.end_date
                print(email, survey_url, start_date, end_date)
                schedule.every().day.at(start_date).do(
                    cls.send_email, email, survey_url, start_date, end_date
                )

    @classmethod
    def schedule_loop(cls):
        while True:
            print("schedule running")
            schedule.run_pending()
            time.sleep(60)

    @classmethod
    def main(cls):
        schedule_thread = threading.Thread(target=cls.schedule_emails)
        schedule_thread.start()
        cls.schedule_loop()


if __name__ == "__main__":
    Scheduling_send_email.main()
