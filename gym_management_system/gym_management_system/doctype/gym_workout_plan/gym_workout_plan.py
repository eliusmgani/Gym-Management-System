# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GymWorkoutPlan(Document):
	def validate(self):
		self.set_workout_duration()

	def set_workout_duration(self):
		self.workout_duration = 0
		for row in self.plan_details:
			self.workout_duration += int(row.workout_duration)
	
