# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, nowtime, add_days

class GymSubscription(Document):
	def before_insert(self):
		self.set_missing_values()
		
	def validate(self):
		self.validate_membership()
		self.set_subscription_dates()
		self.set_subscription_status()
	
	def before_submit(self):
		self.validate_payments()
	
	def before_cancel(self):
		gym_payment = frappe.get_value("Gym Payment", 
				{"reference_doctype": self.doctype, "reference_name": self.name, "docstatus": ["<", 2]})
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

		if self.gym_plan:
			self.workout_days, self.workout_duration = frappe.get_value(
				"Gym Workout Plan", self.gym_plan, ["workout_days", "workout_duration"]
			)
	
	def validate_membership(self):
		if self.gym_member:
			membership = frappe.get_all(
				"Gym Membership", 
				filters={"gym_member": self.gym_member, "status": "Active"}, fields=["name", "status"],
				limit_page_length=1
			)

			if len(membership) == 0:
				frappe.throw(f"Please activate membership for this member: <strong>{self.gym_member}</strong> first")
	
	def set_subscription_dates(self):
		if self.workout_days:
			if self.payment_date:
				self.start_date = self.payment_date
			else:
				self.start_date = self.posting_date
			self.end_date = add_days(self.start_date, self.workout_days)

	def set_subscription_status(self, caller=None):
		status = ""
		if (
			self.paid == 1 and 
			(
				self.start_date and getdate(nowdate()) >= getdate(self.start_date)
				and self.end_date and getdate(nowdate()) <= getdate(self.end_date)
			)
		):
			status = "Active"
		elif (
			self.paid == 1 and
			(
				self.start_date and 
				getdate(nowdate()) < getdate(self.start_date)
			)
		):
			status = "On Hold"
		elif self.paid == 0:
			status = "Pending"
		
		if not caller:
			self.subscription_status = status
		else:
			frappe.db.set_value("Gym Subscription", self.name, "subscription_status", status)
	
	def validate_payments(self):
		if self.paid == 0:
			frappe.throw("Please pay for this subscription first")
		
		if self.paid_amount == 0:
			frappe.throw("Paid amount cannot be zero")
