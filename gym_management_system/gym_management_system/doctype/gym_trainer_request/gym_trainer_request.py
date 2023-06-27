# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, nowtime, get_url_to_form

class GymTrainerRequest(Document):
	def before_insert(self):
		self.full_name = self.first_name + " " + self.last_name
		self.posting_date = nowdate()
		self.posting_time = nowtime()

	def validate(self):
		if frappe.db.exists("Gym Trainer Request", {"email": self.email, "name": ["!=", self.name], "docstatus": ["<", 2]}):
			frappe.throw("This email is already registered")
	
	def before_submit(self):
		if frappe.db.exists("Gym Trainer", {"full_name": self.full_name, "email": self.email}):
			frappe.throw("Trainer already exists")
		
		doc_info = self.as_dict()
		for key in ["name", "creation", "modified", "modified_by", "doctype", "docstatus"]:
			del doc_info[key]
		
		trainer = frappe.get_doc({
			"doctype": "Gym Trainer",
			**doc_info
		}).insert()
		trainer.reload()

		url = get_url_to_form(trainer.doctype, trainer.name)
		frappe.msgprint(f"Gym Trainer: <a href='{url}'><b>{trainer.name}</b></a> is successfull created")


