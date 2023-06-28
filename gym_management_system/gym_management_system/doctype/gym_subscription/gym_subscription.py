# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, nowtime

class GymSubscription(Document):
	def before_insert(self):
		self.set_missing_values()
		
	def validate(self):
		self.validate_membership()
		self.set_subscription_status()
	
	def before_submit(self):
		self.validate_payments()
	
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
	
	def set_subscription_status(self, caller=None):
		status = ""
		if (
			self.paid == 1 and 
			(
				self.start_date and getdate(nowdate()) > getdate(self.start_date)
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
			self.status = status
		else:
			frappe.db.set_value("Gym Subscription", self.name, "status", status)
	
	
	def validate_payments(self):
		if self.paid == 0:
			frappe.throw("Please pay the subscription first")
		
		if self.paid_amount == 0:
			frappe.throw("Paid amount cannot be zero")