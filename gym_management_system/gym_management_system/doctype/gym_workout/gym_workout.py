# Copyright (c) 2023, Elius Mgani and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GymWorkout(Document):
	def before_insert(self):
		self.set_title()

	def validate(self):
		if len(self.workout_exercise) == 0:
			frappe.throw("Please add exercise to workout")
			
		self.set_workout_duration()

	def set_title(self):
		self.title = self.workout_name + "-" + self.workout_level
	
	def set_workout_duration(self):
		self.workout_duration = 0
		for row in self.workout_exercise:
			self.workout_duration += int(row.total_time)
	