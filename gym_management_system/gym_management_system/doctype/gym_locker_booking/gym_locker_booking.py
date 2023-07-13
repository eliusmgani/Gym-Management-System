# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, nowtime, add_days
from frappe.model.document import Document

class GymLockerBooking(Document):
	def before_insert(self):
		self.set_missing_values()
	
	def set_missing_values(self):
		self.posting_date = nowdate()
		self.posting_time = nowtime()
		self.issued_date = nowdate()