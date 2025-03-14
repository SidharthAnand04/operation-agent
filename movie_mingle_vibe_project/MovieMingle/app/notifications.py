from flask import flash

# Notifications for user actions consistently used throughout the app
def notify_user_success(message):
    flash(message, 'success')

def notify_user_error(message):
    flash(message, 'error')