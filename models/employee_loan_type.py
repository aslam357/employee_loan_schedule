from odoo import models, fields, api

class EmployeeLoanType(models.Model):
    _name = 'employee.loan.type'
    _description = 'Employee Loan Type'
    
    employee = fields.Many2one(
        'hr.employee', 
        string="Name", 
        required=True
        )

    loan_limit = fields.Float(
        string="Loan Amount Limit"
        )
    loan_term = fields.Integer(
        string="Loan Term "
        )
    interest_rate = fields.Float(
        string="Interest Rate "
        )
    interest_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('variable', 'Variable'),
        ('reduce', 'Reduce')
    ], string="Interest Type")
    account_id = fields.Many2one(
        'account.account', 
        string="Loan Account"
        )
    interest_account = fields.Many2one(
        'account.account', 
        string="Interest Account"
        )
    apply_interest = fields.Boolean(
        string="Apply Interest"
        )



