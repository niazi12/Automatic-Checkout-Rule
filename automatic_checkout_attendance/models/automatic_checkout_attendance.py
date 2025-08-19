from datetime import timedelta, datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AutomaticCheckoutAttendance(models.Model):
    _inherit = "hr.attendance"

    block_duration = 30  # Block duration 30 in minutes

    def _get_current_employee_id(self):
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id

    employee_id = fields.Many2one('hr.employee', string="Employee", default=_get_current_employee_id)

    def _cron_automatic_user_checkout(self):
        today_date = datetime.today().strftime('%Y-%m-%d 00:00:00')
        non_checkout_attendance = self.env['hr.attendance'].sudo().search([('check_out', '=', False)])
        for attendance in non_checkout_attendance:
            checkin_date = attendance.check_in.strftime('%Y-%m-%d 00:00:00')
            user_all_attendance = self.env['hr.attendance'].sudo().search(
                [('employee_id', '=', attendance.employee_id.id), ('check_in', '>', checkin_date)],
                order='check_in desc')

            # check out after 8 hours for lunch break automatically
            if len(user_all_attendance) == 1:
                six_hours_ago = fields.Datetime.now() - timedelta(hours=7)
                if attendance.check_in <= six_hours_ago:
                    attendance.check_out = attendance.check_in + timedelta(hours=7)

            # check out after 8 hours
            elif len(user_all_attendance) == 2:
                prev_worked_hours = user_all_attendance[1].worked_hours
                current_worked_hours = datetime.now() - user_all_attendance[0].check_in
                total_worked_hours = prev_worked_hours + (current_worked_hours.total_seconds() / 3600)
                if total_worked_hours >= 8:
                    attendance.check_out = fields.datetime.now()

            # check out after 1 hour overtime
            elif len(user_all_attendance) > 2:
                one_hours_ago = fields.Datetime.now() - timedelta(hours=1)
                if attendance.check_in <= one_hours_ago:
                    attendance.check_out = attendance.check_in + timedelta(hours=1)


    @api.constrains('check_in')
    def _block_check_in(self):
        today_date = datetime.today().strftime('%Y-%m-%d 00:00:00')
        user_all_attendance = self.env['hr.attendance'].search(
            [('employee_id', '=', self.employee_id.id), ('check_in', '>', today_date), ('check_out', '!=', False)])
        if len(user_all_attendance) == 1:
            time_now = fields.Datetime.now()
            last_check_out = fields.Datetime.from_string(user_all_attendance.check_out)
            block_until = last_check_out + timedelta(minutes=self.block_duration)
            if fields.Datetime.from_string(time_now) < block_until:
                raise ValidationError(
                    f"Check-in blocked. Please wait for {self.block_duration} minutes for lunch break.")
        else:
            pass
