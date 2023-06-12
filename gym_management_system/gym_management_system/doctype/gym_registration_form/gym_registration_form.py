# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GymRegistrationForm(Document):
    def before_insert(self):
        self.full_name = self.first_name + " " + self.last_name
    def validate(self):
        if self.weight and self.height:
            self.bmi = (self.weight / (self.height * self.height)) * 10000
    def before_submit(self):
        pass
    def create_gym_member(self):
            pass
    # def create_user(self):
    #     user = frappe.new_doc("User")
	# 	user.email = self.email
	# 	user.first_name = self.first_name
	# 	user.last_name = self.last_name
	# 	user.save()
	# 	user.add_roles("Gym Member")
	# 	user.save()
	# 	self.user = user.name
	# 	self.save()
                        
