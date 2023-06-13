# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, nowtime, get_url_to_form

class GymMember(Document):
	def before_insert(self):
		self.full_name = self.first_name + " " + self.last_name
	
	def after_insert(self):
		self.create_user()
		self.create_customer()
	
	def validate(self):
		self.calculate_bmi()
	
	def calculate_bmi(self):
		if not self.weight or not self.height:
			return
		self.bmi = self.weight / ((self.height / 100) ** 2)
		
	def create_customer(self):
		customer = frappe.new_doc("Customer")
		customer.customer_name = self.full_name
		customer.customer_group = "Individual"
		customer.territory = "All Territories"
		customer.customer_type = "Individual"
		customer.save(ignore_permissions=True)
		frappe.msgprint("Customer Created Successfully")
	
	def create_user(self):
		if frappe.db.exists('Gym Member', self.full_name, self.email):
			return
		
		user = frappe.new_doc("User")
		user.email = self.email
		user.first_name = self.first_name
		user.last_name = self.last_name
		user.enabled = 1
		user.flags.ignore_permissions = True
		user.save(ignore_permissions=True)
		user.reload()
		user.add_roles("Gym Member")	
		frappe.msgprint("User Created Successfully")

@frappe.whitelist()
def create_gym_member(member_info):
	if frappe.db.exists("Gym Member", {"full_name": member_info.full_name, "email": member_info.email}):
		return frappe.db.get_value("Gym Member", {"full_name": member_info.full_name, "email": member_info.email}, "name")

	gym_member = frappe.new_doc("Gym Member")
	gym_member.update(member_info)
	gym_member.save(ignore_permissions=True)
	gym_member.reload()
	url = get_url_to_form(gym_member.doctype, gym_member.name)
	frappe.msgprint(f"Gym Member: <a href='{url}'><b>{gym_member.name}</b></a> is successfull created")
	return gym_member.name