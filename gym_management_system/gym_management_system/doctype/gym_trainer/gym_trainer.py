# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GymTrainer(Document):
	def before_insert(self):
		self.full_name = f"{self.first_name} {self.last_name}"
