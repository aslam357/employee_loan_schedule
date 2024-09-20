from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    _description = 'Employee Loan'
    _inherit = 'mail.thread'

    name = fields.Char(
        string="Loan Reference", 
        required=True, 
        copy=False, 
        readonly=True, 
        default=lambda self: self._generate_default_name()
    )
    employee_id = fields.Many2one(
        'hr.employee', 
        string="Employee", 
        required=True
        )
    department_id = fields.Many2one(
        'hr.department', 
        string="Department", 
        store=True
        )
    department_manager_id = fields.Many2one(
        'hr.employee', 
        string="Department Manager"
        )
    job_id = fields.Many2one(
        'hr.job', 
        string="Job Position"
        )
    loan_type = fields.Many2one(
        'account.account', 
        string="Loan Type", 
        required=True
        )
    
    loan_amount = fields.Float(
        string="Loan Amount"
        )
    interest_rate = fields.Float(
        string="Interest Rate"
        )
    interest_type = fields.Selection(
        [('fixed', 'Fixed'), 
         ('variable', 'Variable'), 
         ('reduce', 'Reduce')], 
        string="Interest Type"
    )
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

    loan_date = fields.Date(
        string="Date", 
        default=fields.Date.today
        )
    payment_method = fields.Selection([
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly')
    ], string="Payment Method")
    installment_count = fields.Integer(
        string="Installments", 
        required=True
        )
    installment_amount = fields.Float(
        string="Installment Amount", 
        compute="_compute_installment_amount", 
        store=True
        )
    interest_amount = fields.Float(
        string="Interest Amount", 
        compute="_compute_interest_amount", 
        store=True)
    paid_amount = fields.Float(
        string="Paid Amount"
        )
    remaining_amount = fields.Float(
        string="Remaining Amount", 
        compute="_compute_remaining_amount", 
        store=True
        )
    start_date = fields.Date(
        string="Start Date"
        )
    end_date = fields.Date(
        string="End Date"
        )
    term = fields.Char(
        string="Term"
        )
    user_id = fields.Many2one(
        'res.users', 
        string="User"
        )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit_request', 'Submit Request'),
        ('department_approval', 'Department Approval'),
        ('hr_approval', 'HR Approval'),
        ('done', 'Done'),
        ('refused', 'Refused'),
    ], string='Status', readonly=True, default='draft')

    installment_line_ids = fields.One2many(
        'loan.installment', 
        'loan_id', 
        string="Installments", 
        readonly=True
        )
    transaction_reason = fields.Text(
        string="Transaction Reason"
        )



    def _generate_default_name(self):
        last_loan = self.search([], order='id desc', limit=1)
        last_number = int(last_loan.name.split(' ')[-1]) if last_loan and last_loan.name else 0
        new_number = last_number + 1
        return f'Loan {new_number:05d}'

    @api.depends('installment_count', 
                 'loan_amount', 
                 'interest_rate'
                 )
    def _compute_installment_amount(self):
        for loan in self:
            if loan.installment_count > 0:
                total_amount = loan._compute_total_amount()
                loan.installment_amount = total_amount / loan.installment_count
            else:
                loan.installment_amount = 0.0

    @api.depends('installment_count', 
                 'loan_amount', 
                 'interest_rate'
                 )
    def _compute_interest_amount(self):
        for loan in self:
            if loan.installment_count > 0:
                total_amount = loan._compute_total_amount()
                loan.interest_amount = (total_amount - loan.loan_amount) / loan.installment_count
            else:
                loan.interest_amount = 0.0

    @api.depends('installment_amount', 
                 'paid_amount', 
                 'installment_count'
                 )
    def _compute_remaining_amount(self):
        for loan in self:
            total_amount_due = loan.installment_amount * loan.installment_count
            loan.remaining_amount = total_amount_due - loan.paid_amount

    def _compute_total_amount(self):
        return self.loan_amount + (self.loan_amount * self.interest_rate / 100)

    def compute_installments(self):
        self.ensure_one()

        self.installment_line_ids = [(5, 0, 0)]
        total_amount = self.loan_amount + self.interest_amount
        if self.installment_count > 0:
            installment_amount = total_amount / self.installment_count
            interest_amount = self.interest_amount / self.installment_count
            installment_vals = []
            for i in range(self.installment_count):
                installment_date = self._get_installment_date(i)
                installment_vals.append((0, 0, {
                    'installment_date': installment_date,
                    'installment_amount': installment_amount,
                    'interest_amount': interest_amount,
                    'employee_id': self.employee_id.id, 
                }))
            self.installment_line_ids = installment_vals

    def _get_installment_date(self, installment_index):
        start_date = fields.Date.from_string(self.start_date)
        if self.payment_method == 'monthly':
            return start_date + relativedelta(months=installment_index)
        elif self.payment_method == 'weekly':
            return start_date + relativedelta(weeks=installment_index)
        return fields.Date.today()

    def action_approve(self):
        self.state = 'submit_request'

    def action_approves(self):
        self.state = 'department_approval'

    def action_reject(self):
        self.state = 'draft'
