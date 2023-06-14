# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate
from frappe.model.document import Document

class GymMembershipOption(Document):
	def get_days(self):
		if self.period == "Daily":
			return 1
		elif self.period == "Weekly":
			return 7
		elif self.period == "Monthly":
			return 30
		elif self.period == "Yearly":
			return 365
		else:
			frappe.throw("Please select a period")

