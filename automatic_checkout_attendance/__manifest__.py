{
    'name': "Automatic Checkout Attendance",
    'summary': "Automatic checkout for lunch breaks and daily limits",
    'description': """
        This module automatically handles employee checkouts when they forget:
        - Auto-checkout after 7 hours for lunch breaks
        - Enforces 30-minute break (configurable)
        - Auto-checkout after 8 working hours
        - Auto-checkout after 1 hour overtime
        - Seamless integration with HR Attendance
    """,
    'author': "Niazi Mahrab",
    'website': "https://niazimahrab.com/",
    'license': 'OPL-1',
    'category': 'Human Resources',
    'version': '16.0.1.0',
    'depends': ['hr', 'hr_attendance'],
    'data': [
        'data/automatic_checkout_attendance_scheduler.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 16.0,
    'currency': 'USD',
}