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

frappe.ui.form.on("Gym Workout Plan Detail", {
	gym_workout: (frm, cdt, cdn) => {
		let row = locals[cdt][cdn];
		if (row.gym_workout) {
			frappe.db.get_doc("Gym Workout", row.gym_workout)
				.then(workout_doc => {
					for (let d of workout_doc.workout_exercise) {
						let child = frm.add_child("workout_exercise");
						child.exercise_name = d.exercise_name;
						child.exercise_rounds = d.exercise_rounds;
						child.exercise_sets = d.exercise_sets;
						child.rest_time_per_round = d.rest_time_per_round;
						child.exercise_type = d.exercise_type;
						child.total_time = d.total_time;
					}
					frm.refresh_field("workout_exercise")
				})
		}
	}
})