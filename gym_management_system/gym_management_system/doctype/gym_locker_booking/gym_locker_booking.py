# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, nowtime, add_days
from frappe.model.document import Document

class GymLockerBooking(Document):
	def before_insert(self):
		self.set_missing_values()
	
	def validate(self):
		self.validate_membership()
	
	def before_cancel(self):
		gym_payment = frappe.get_value("Gym Payment",
			{ "reference_doctype": self.doctype, "reference_name": self.name, "docstatus": ["<", 2] })
		
		if gym_payment:
			pay_doc = frappe.get_doc("Gym Payment", gym_payment)
			if pay_doc.docstatus == 0:
				pay_doc.delete()
			pay_doc.flags.ignore_links = True
			pay_doc.cancel()
			pay_doc.delete()

	def set_missing_values(self):
		self.posting_date = nowdate()
		self.posting_time = nowtime()
		self.issued_date = nowdate()
	
	def validate_membership(self):
		if self.gym_member:
			membership = frappe.get_all(
				"Gym Membership",
				filters = { "gym_member": self.gym_member, "status": "Active" }, fields = ["name", "status"],
				limit_page_length = 1
			)
			if len(membership) == 0:
				frappe.throw(f"Please activate membership for this member: <strong>{self.gym_member}</strong> first")
