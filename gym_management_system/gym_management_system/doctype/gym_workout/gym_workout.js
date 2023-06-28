// Copyright (c) 2023, Elius Mgani and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Workout', {
	// refresh: function(frm) {

	// }
	onload: (frm) => {
		frm.set_workout_duration = (frm) => {
			let workout_time = 5;
			frm.doc.workout_exercise.forEach(row => {
				workout_time += Number(row.total_time)
			});

			if (frm.doc.workout_duration != (workout_time)) {
				frm.set_value("workout_duration", Number(workout_time))
				frm.refresh_field("workout_duration")
			}
		}
	}
});


frappe.ui.form.on("Gym Workout Exercise", {
	total_time: (frm, cdt, cdn) => {
		let row = locals[cdt][cdn];
		if (row.total_time != 0) {
			frm.set_workout_duration(frm)
		}
	}
})
