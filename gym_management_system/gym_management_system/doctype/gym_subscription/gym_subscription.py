# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, nowtime

class GymSubscription(Document):
	def before_insert(self):
		self.set_missing_values()
	
	def set_missing_values(self):
		self.posting_date = nowdate()
		self.posting_time = nowtime()

		if self.gym_plan:
			self.workout_days, self.workout_duration = frappe.get_value(
				"Gym Workout Plan", self.gym_plan, ["workout_days", "workout_duration"]
			)
	