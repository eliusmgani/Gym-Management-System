# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, nowtime

class GymPayment(Document):
	def before_insert(self):
		self.set_posting_date()
		self.set_payment_date()

	def set_posting_date(self):
		self.posting_date = nowdate()
		self.posting_time = nowtime()
	