# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GymTrainer(Document):
	def before_insert(self):
		self.full_name = f"{self.first_name} {self.last_name}"
	
	def after_insert(self):
		self.create_user()

	def create_user(self):
		if frappe.db.exists("Gym Member", self.full_name, self.email):
			return
		
		user = frappe.new_doc("User")
		user.email = self.email
		user.first_name = self.first_name
		user.last_name = self.last_name
		user.gender = self.gender
		user.phone = self.phone_number
		user.mobile = self.phone_number
		user.birth_date = self.birth_date
		user.send_welcome_email = 1
		user.enabled = 1
		user.flags.ignore_permissions = True
		user.save(ignore_permissions=True)
		user.reload()
		user.add_roles("Gym Trainer")	
		frappe.msgprint("User Created Successfully")