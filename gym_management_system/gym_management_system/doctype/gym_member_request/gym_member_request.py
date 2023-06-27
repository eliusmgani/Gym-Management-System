# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, nowtime
from gym_management_system.gym_management_system.doctype.gym_member.gym_member import create_gym_member

class GymMemberRequest(Document):
    def before_insert(self):
        self.full_name = self.first_name + " " + self.last_name
        self.posting_date = nowdate()
        self.posting_time = nowtime()
    
    def validate(self):
        if frappe.db.exists("Gym Member Request", {"email": self.email, "name": ["!=", self.name], "docstatus": ["<", 2]}):
            frappe.throw("This email is already registered")

    def before_submit(self):
        details = frappe._dict({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "dob": self.dob,
            "gender": self.gender,
            "mobile": self.mobile,
            "weight": self.weight,
            "height": self.height,
            "gym_goal": self.gym_goal,
            "contact_person_name": self.contact_person_name,
            "relationship": self.relationship,
            "phone_no": self.phone_no,
            "streat": self.streat,
            "city": self.city,
            "state": self.state,
            "pobox": self.pobox,
            "profile": self.profile,
            "registration_form": self.name
        })
        create_gym_member(details)
