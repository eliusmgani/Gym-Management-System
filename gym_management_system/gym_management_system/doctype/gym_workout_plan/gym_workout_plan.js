// Copyright (c) 2023, Elius Mgani and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Workout Plan', {
	refresh: function (frm) {
		let trainer_levels = {
			"Beginner": "Beginner",
			"Intermediate": "Intermediate",
			"Advance": "Advance",
			"Expert": "Professional"
		}

		frm.set_query("workout_trainer", () => {
			return {
				filters: {
					trainer_level: trainer_levels[frm.doc.plan_level]
				}
			}		
		});

		frm.set_query("gym_workout", "plan_details", () => {
			return {
				filters: {
					workout_level: trainer_levels[frm.doc.plan_level]
				}
			}

		});
	}
});
