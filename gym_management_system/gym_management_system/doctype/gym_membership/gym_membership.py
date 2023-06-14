# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, nowdate, getdate

class GymMembership(Document):
	def before_insert(self):
		if not self.membership_option:
			frappe.throw("Please select a membership option")
	
	def validate(self):
		if not self.membership_option:
			frappe.throw("Please select a membership option")
		
		self.membership_duration = frappe.get_doc("Gym Membership Option", self.membership_option).get_days()
		self.set_date_range()

	def set_date_range(self):
		prev_membership = frappe.get_all("Gym Membership", 
			filters={"gym_member": self.gym_member, "status": "Active", "docstatus": 1},
			fields=["name", "start_date", "end_date"],
			order_by="end_date desc", limit_page_length=1
		)
		if len(prev_membership) > 0:
			if not self.valid_after_end_of_prev_membership:
				frappe.throw("This member already has an active membership")
			else:
				self.start_date = prev_membership[0].end_date
				self.end_date = add_days(self.start_date, self.membership_duration)
				self.prev_membership = prev_membership[0].name
		else:
			self.start_date = nowdate()
			self.end_date = add_days(self.start_date, self.membership_duration)
		