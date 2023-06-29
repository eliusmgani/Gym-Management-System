import frappe
from frappe.utils import nowdate, add_days, getdate


def check_membership_expiry():
	memberships = frappe.get_all("Gym Membership", 
		filters={"status": "Active", "docstatus": 1},
		fields=["name", "end_date"]
	)
	for membership in memberships:
		if getdate(membership.end_date) <= getdate(nowdate()):
			frappe.db.set_value("Gym Membership", membership.name, {
				"status": "Expired",
				"valid_after_end_of_prev_membership": 0
	        })

def check_membership_onhold():
	memberships = frappe.get_all("Gym Membership", 
		filters={"status": "On Hold", "docstatus": 1},
		fields=["name", "start_date"]
	)
	for membership in memberships:
		if getdate(membership.start_date) >= getdate(nowdate()):
			frappe.db.set_value("Gym Membership", membership.name, {
				"status": "Active",
				"valid_after_end_of_prev_membership": 0
			})

def check_subscription_expiry():
	subscriptions = frappe.get_all("Gym Subscription", filters={"subscription_status": "Active", "docstatus": 1})
	
	for subscription in subscriptions:
		sub_doc = frappe.get_doc("Gym Subscription", subscription.name)
		sub_doc.set_subscription_status(caller="check_subscription_expiry")