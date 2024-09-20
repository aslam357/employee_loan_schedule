from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def action_loans(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employee Loans',
            'res_model': 'employee.loan',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('state', '=', 'department_approval')],
        }
