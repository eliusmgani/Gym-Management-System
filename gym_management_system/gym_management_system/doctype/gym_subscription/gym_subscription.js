// Copyright (c) 2023, Elius Mgani and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Subscription', {
	refresh: (frm) => {
		if (frm.doc.paid == 0 && !frm.doc.__islocal) {
			frm.add_custom_button(__("Make Paymnent"), () => {
				frappe.new_doc("Gym Payment", {
					"payment_for": "Subscription"
				}, doc => {
					doc.gym_member = frm.doc.gym_member;
					doc.gym_trainer = frm.doc.gym_trainer;
					doc.reference_doctype = frm.doc.doctype;
					doc.reference_name = frm.doc.name;
					doc.payment_date = frappe.datetime.now_date();
					doc.payment_time = frappe.datetime.now_time();
					doc.posting_date = frappe.datetime.now_date();
					doc.posting_time = frappe.datetime.now_time();
					doc.actual_price = frm.doc.subscription_amount;
					doc.discount_amount = frm.doc.discount_amount;
					doc.paid_amount = frm.doc.subscription_amount - frm.doc.discount_amount;
				});
			}).removeClass("btn-default").addClass("btn-warning font-weight-bold")
		}
		if (frm.doc.gym_plan) {
			frm.fields_dict["workouts"].$wrapper.html("");
			frm.trigger("gym_plan")
		}

	},
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
