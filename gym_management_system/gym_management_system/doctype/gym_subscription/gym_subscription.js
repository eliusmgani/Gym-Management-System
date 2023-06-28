// Copyright (c) 2023, Elius Mgani and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Subscription', {
	// refresh: function(frm) {

	// }
	gym_plan: (frm) => {
		if (frm.doc.gym_plan) {
			frappe.db.get_doc("Gym Workout Plan", frm.doc.gym_plan)
				.then(plan_doc => {
					var html = `
						<style>
							.table {border-collapse: collapse; width: 100%;}
							.table th, .table td {border: 1px solid #dddddd; padding: 8px; text-align: left;}
							.table th {background-color: #f2f2f2;}
							.table tbody tr:nth-child(even) {background-color: #f9f9f9;}
							.table tbody tr:hover {background-color: #eaeaea;}
						</style>

						<table class="table table-bordered">
							<thead>
								<tr>
								<th>Gym Workout</th>
								<th>Workout Name</th>
								<th>Workout Purpose</th>
								<th>Exercise</th>
								<th>Reps</th>
								<th>Sets</th>
								<th>Rest</th>
								</tr>
							</thead>
							<tbody>`;
					for (let d of plan_doc.plan_details) {
						console.log("plan", d)
						for (let i of plan_doc.workout_exercise) {
							if (d.gym_workout == i.gym_workout) {
								console.log("table", html)
								html = html + `
									<tr>
										<td style="border: 1px solid #dddddd; padding: 8px;">${d.gym_workout}</td>
										<td style="border: 1px solid #dddddd; padding: 8px;">${d.workout_name}</td>
										<td style="border: 1px solid #dddddd; padding: 8px;">${d.workout_purpose}</td>
										<td style="border: 1px solid #dddddd; padding: 8px;">${i.exercise_name}</td>
										<td style="border: 1px solid #dddddd; padding: 8px;">${i.exercise_rounds}</td>
										<td style="border: 1px solid #dddddd; padding: 8px;">${i.exercise_sets}</td>
										<td style="border: 1px solid #dddddd; padding: 8px;">${i.rest_time_per_round}</td>
									</tr>`;
							}
						}
					}
					html += `</tbody></table>`
					frm.fields_dict["workouts"].$wrapper.html(html);
				})
		} else {
			frm.fields_dict["workouts"].$wrapper.html("");
		}
	},
});
