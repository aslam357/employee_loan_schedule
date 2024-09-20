# -*- coding: utf-8 -*-
{
    'name': "employee_loan_schedule",
    'summary': "Employee Loan Management module is developed to help manage employee loans. It can configures loan types and manages loan applications.",
    'author': "Amzsys",
    'website': "https://www.amzsys.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','hr','account', ],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_loan_type.xml',
        'views/employee_loan.xml',
        'views/loan_approval.xml',
        'views/menu_items.xml',
        
    ],

}

