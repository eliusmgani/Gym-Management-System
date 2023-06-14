# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, nowdate, getdate

class GymMembership(Document):
	def before_insert(self):
		if not self.membership_option:
			frappe.throw("Please select a membership option")
	