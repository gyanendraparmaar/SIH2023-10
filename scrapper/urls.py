departments = {
	# "indian_government": ['govt-advisory', 'indian-government', 'government-of-india'],
	"department_of_personnel_and_training": ['personnel-department', 'government-schemes'],
	"department_of_legal_affair": ['department-of-legal-affairs'],
	"department_of_commerce": ['ministry-of-finance', 'commerce-ministry', 'economic-growth'],
	"department_of_health": ['health-department', 'department-of-health-and-family-welfare'],
	"department_of_food": ['food-ministry', 'department-of-food-and-public-distribution'],
	"department_for_promotion_of_industry": ['dpiit'],
	"department_of_sports": ['government-and-sports-ministry'],
	"department_of_science_and_technology": ['department-of-science-and-technology', 'ministry-of-science-and-technology']
}

[departments.update({dept: list(map(lambda url: "https://economictimes.indiatimes.com/topic/" + url, departments[dept]))}) for dept in departments]