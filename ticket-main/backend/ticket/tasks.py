from celery import shared_task
import time
from .my_mail import send_mail
from jinja2 import Template
from .model import User, booking, Venue, shw, Movie, db
from datetime import datetime, timedelta, date
import os 
import csv
from flask import current_app
from sqlalchemy import and_
# from .worker import create_celery_app

# @shared_task()
# def send_email():
#     with open('mail-tempelate.html') as f:
#         text_msg = Template(f.read())
#         send_mail("test@gmail.com", "testing email", text_msg.render(user="Test User"))
        
        
# 1.daily reminder report

@shared_task()
def send_daily():
    try:
        with open('reminder.html') as f:
            text_msg = Template(f.read())
        
        # Access the Flask app using current_app
        app = current_app
        
        # Example: Query all users and send an email to each of them
        users = User.query.all()

        for user in users:
            last_booking = booking.query.filter_by(user_id=user.id).first()

            # Check if there's no last booking or if the last booking was made more than 1 day ago
            if not last_booking or last_booking.date_time < datetime.utcnow() - timedelta(days=1):
                send_mail(user.email, "Daily Email", text_msg.render(user=user.name))

        return {
            'status': 'success',
            'message': 'Emails sent successfully!',
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': 'Error sending emails: ' + str(e),
        }




# 2.csv exports

@shared_task
def export_venue_csv(selected_venue_id):
    try:
        if selected_venue_id is None:
            raise ValueError("No venue selected. Please provide a venue ID.")

        
            # Define the export fields
        venue_fields = ['ID', 'Name', 'Location', 'Total Seats']

            # Query the venues from the database based on selected_venue_id
        venue = Venue.query.get(selected_venue_id)

        if not venue:
            raise ValueError("Venue not found. Please provide a valid venue ID.")

            # Create a list of rows for the CSV file
        rows = []
        row = [venue.id, venue.name, venue.location, venue.num_total_seats]
        rows.append(row)

            # Generate a timestamp for the CSV file name
        now = datetime.now().strftime("%d-%m-%Y_%H%M%S")
        venue_filename = f'venues_{now}.csv'

            # Define the directory path to save CSV files
        csv_dir = os.path.join(current_app.root_path, 'templates', 'CSV exports', 'venues')
        os.makedirs(csv_dir, exist_ok=True)
        csv_path = os.path.join(csv_dir, venue_filename)

            # Write the CSV file
        with open(csv_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

                # Write the header row
            csvwriter.writerow(venue_fields)

                # Write the data rows
            csvwriter.writerows(rows)

        return {
            'status': 'success',
            'message': 'Venue CSV created successfully!',
            'venue_csv_path': csv_path,
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': 'Error exporting Venue CSV: ' + str(e),
        }
        
        
        
#3. Monthly reminder report
@shared_task()
def send_mr():
    try:
        with open('report.html') as f:
            report_template = Template(f.read())

        # Calculate the first and last day of the previous month
        today = date.today()
        first_day_of_month = date(today.year, today.month, 1)
        last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

        # Query all users from the database
        users = User.query.all()

        # Iterate over users and send the report to each of them
        for user in users:
            # Query bookings for the previous month for each user
            bookings = booking.query.filter(
                and_(booking.date_time >= first_day_of_month, booking.date_time <= last_day_of_month),
                booking.user_id == user.id
            ).all()

            # Render the report HTML with data
            report_html = report_template.render(
                month=last_day_of_month.strftime('%B'),
                year=last_day_of_month.year,
                bookings=bookings,
                user=user
            )

            # Send the report as an email to the user
            send_mail(user.email, "Monthly Entertainment Report", report_html)

        return {
            'status': 'success',
            'message': 'Monthly Entertainment Report sent successfully!',
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': 'Error sending Monthly Entertainment Report: ' + str(e),
        }