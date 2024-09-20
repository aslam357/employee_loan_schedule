from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class LoanInstallment(models.Model):
    _name = 'loan.installment'
    _description = 'Loan Installment'

    employee_id = fields.Many2one(
        'hr.employee', 
        string="Employee", 
        required=True
        )
    loan_id = fields.Many2one(
        'employee.loan', 
        string="Loan", 
        required=True, 
        ondelete='cascade'
        )
    name = fields.Char(
        string="Name", 
        related="loan_id.name", 
        required=True
        )
    installment_date = fields.Date(
        string="Installment Date", 
        required=True
        )
    installment_amount = fields.Float(
        string="Installment Amount", 
        compute="_compute_installment_amount", 
        store=True
        )
    paid_amount = fields.Float(
        string="Paid Amount", 
        default=0.0
        )
    loan_date = fields.Date(
        string="Loan Date", 
        default=fields.Date.today
        )
    loan_amount = fields.Float(
        string="Loan Amount", 
        related="loan_id.loan_amount", 
        store=True
        )
    interest_amount = fields.Float(
        string="Interest Amount", 
        related="loan_id.interest_amount", 
        store=True
        )
    remaining_amount = fields.Float(
        string="Remaining Amount", 
        related="loan_id.remaining_amount", 
        store=True
        )
    total_interest = fields.Float(
        string="Total Interest", 
        compute="_compute_total_interest", 
        store=True
        )
    grand_total = fields.Float(
        string="Grand Total", 
        compute="_compute_grand_total", 
        store=True
        )
    employee_name = fields.Char(
        string="Employee Name", 
        related="employee_id.name", 
        store=True
        )
    employee_job = fields.Char(
        string="Employee Job Position", 
        related="employee_id.job_id.name", 
        store=True
        )
    employee_department = fields.Char(
        string="Employee Department", 
        related="employee_id.department_id.name", 
        store=True
        )
    
    employee_id = fields.Many2one(
        'hr.employee', 
        string="Employee"
    )


    @api.depends('installment_amount', 
                 'interest_amount'
                 )
    def _compute_grand_total(self):
        for rec in self:
            rec.grand_total = rec.installment_amount + rec.interest_amount

    @api.depends('loan_id.interest_amount')
    def _compute_total_interest(self):
        for rec in self:
            rec.total_interest = rec.loan_id.interest_amount

    @api.depends('loan_id.installment_amount')
    def _compute_installment_amount(self):
        for rec in self:
            rec.installment_amount = rec.loan_id.installment_amount

    @api.onchange('loan_id')
    def _onchange_loan_id(self):
        if self.loan_id:
            self.installment_amount = self.loan_id.installment_amount
            self.total_interest = self.loan_id.interest_amount
            self.remaining_amount = self.loan_id.remaining_amount
            self.loan_amount = self.loan_id.loan_amount
            self.interest_amount = self.loan_id.interest_amount


