# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, nowtime

class GymPayment(Document):
	def before_insert(self):
		self.set_posting_date()
		self.set_payment_date()

	def validate(self):
		self.validate_membership()
	
	def before_submit(self):
		self.validate_payment_amount()
		self.set_payment_date()
		self.update_references()

	def set_posting_date(self):
		self.posting_date = nowdate()
		self.posting_time = nowtime()

	def validate_membership(self):
		if self.gym_member and self.reference_doctype != "Gym Membership":
			membership = frappe.get_all(
				"Gym Membership", 
				filters={"gym_member": self.gym_member, "status": "Active"}, fields=["name", "status"],
				limit_page_length=1
			)

			if len(membership) == 0:
				frappe.throw(f"Please activate membership for this member: <strong>{self.gym_member}</strong> first")
	
	def validate_payment_amount(self):
		if (float(self.actual_price) - float(self.discount_amount)) != float(self.paid_amount):
			frappe.throw("Paid Amount is not equal to required payment amount, please check and revert.")
	
	def set_payment_date(self):
		self.payment_date = nowdate()
		self.payment_time = nowtime()
	
	def update_references(self):
		doc = frappe.get_doc(self.reference_doctype, self.reference_name)
		doc.discount_amount = self.discount_amount
		doc.paid = 1
		doc.paid_amount = self.paid_amount
		doc.payment_date = nowdate()
		doc.payment_time = nowtime()
		doc.save()
		if doc.paid == 1:
			doc.submit()