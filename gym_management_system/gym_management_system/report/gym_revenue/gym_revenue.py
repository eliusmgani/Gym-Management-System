# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns(filters)

	cond = get_conditions(filters)
	
	data = frappe.db.get_all("Gym Payment", filters=cond, fields=["*"])

	report_summary = get_report_summary(data)

	return columns, data, None, None, report_summary

def get_columns(filters):
    columns = [
		{"fieldname": "posting_date", "fieldtype": "Date", "label": _("Posting Date"), "width": "100px"},
		{"fieldname": "posting_time", "fieldtype": "Time", "label": _("Posting Time"), "width": "100px"},
		{"fieldname": "payment_date", "fieldtype": "Date", "label": _("Payment Date"), "width": "100px"}, 
		{"fieldname": "gym_member", "fieldtype": "Link", "label": _("Gym Member"), "options": "Gym Member", "width": "100px"}, 
		{"fieldname": "member_fullname", "fieldtype": "Data", "label": _("Member Fullname"), "width": "100px"}, 
		{"fieldname": "gym_trainer", "fieldtype": "Link", "label": _("Gym Trainer"), "options": "Gym Trainer", "width": "100px"}, 
		{"fieldname": "trainer_name", "fieldtype": "Data", "label": _("Trainer Name"), "width": "100px"}, 
		{"fieldname": "payment_for", "fieldtype": "Data", "label": _("Payment For"), "width": "100px"},
		{"fieldname": "actual_price", "fieldtype": "Float", "label": _("Actual Price"), "width": "100px"},
		{"fieldname": "discount_amount", "fieldtype": "Float", "label": _("Discounted Amount"), "width": "100px"},
		{"fieldname": "paid_amount", "fieldtype": "Float", "label": _("Paid Amount"), "width": "100px"},
	]
    return columns

def get_conditions(filters):
	cond = {"docstatus": 1}
	if filters.from_date:
		cond["payment_date"] = [">=", filters.from_date]
		
	if filters.to_date:
		cond["payment_date"] = ["<=", filters.to_date]
		
	if filters.gym_trainer:
		cond["gym_trainer"] = filters.gym_trainer
		
	#if filters.reference_doctype:
		#cond["reference_doctype"] = filters.reference_doctype
	
	return cond
    
def get_report_summary(records):
	membership_payments = sum([d.paid_amount for d in records if d.payment_for == "Membership"])
	subscription_payments = sum([d.paid_amount for d in records if d.payment_for == "Subscription"])
	locker_payment = sum([d.paid_amount for d in records if d.payment_for == "Locker Booking"])

	return [
		{
			"value": membership_payments,
			"label": "Total Payment for " + str(frappe.bold("Gym Membership")),
			"datatype": "Int",
			"width": "500px"
		},
		{
			"value": subscription_payments,
			"label": "Total Payments for " + str(frappe.bold("Gym Subscription")),
			"datatype": "Int",
			"width": "500px"
		},
		{
			"value": locker_payment,
			"label": "Total Payment for " + str(frappe.bold("Gym Locker Booking")),
			"datatype": "Int",
			"width": "500px"
		},
	]