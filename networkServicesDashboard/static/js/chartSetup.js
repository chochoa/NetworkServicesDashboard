/* Globals */
var criticalColor = "#C22313"
var highColor = "#F47321"
var mediumColor = "#FDB813"
var lowColor = "#69AB35"

/* Functions */
function incidentCatBreakdown(critical, high, medium) {
	var pieData = [{
						value: critical,
						color: criticalColor
					},
					{
						value : high,
						color : highColor
					},
					{
						value : medium,
						color : mediumColor
					}];
	var myPie = new Chart(document.getElementById("incidentBreakdown1").getContext("2d")).Pie(pieData, {animationEasing:"easeOutQuart", animateScale:true});
}

function amerChart() {
	var pieData = [{
						value: 1,
						color:"#0000FF"
					},
					{
						value : 0,

						color : "#4C4CFF"
					},
					{
						value : 2,
						color : "#9999FF"
					}];
	var myPie = new Chart(document.getElementById("amerChart").getContext("2d")).Pie(pieData, {animationEasing:"easeOutQuart", animateScale:true});
}

function emearChart() {
	var pieData = [{
						value: 5,
						color:"#FF0000"
					},
					{
						value : 3,

						color : "#FF4C4C"
					},
					{
						value : 1,
						color : "#FF9999"
					}];
	var myPie = new Chart(document.getElementById("emearChart").getContext("2d")).Pie(pieData,{animationEasing:"easeOutQuart", animateScale:true});
}

function ajpcChart() {
	var pieData = [{
						value: 1,
						color:"#00FF00"
					},
					{
						value : 2,

						color : "#4CFF4C"
					},
					{
						value : 10,
						color : "#99FF99"
					}];
	var myPie = new Chart(document.getElementById("ajpcChart").getContext("2d")).Pie(pieData,{animationEasing:"easeOutQuart", animateScale:true});
}

function wirelessIncidentBreakdown(critical, high, medium, low) {
	var pieData = [{
						value: critical,
						color: criticalColor
					},
					{	
						value: high,
						color: highColor
					},
					{	
						value: medium,
						color: mediumColor
					},
					{	
						value: low,
						color: lowColor
					}];
	var myPie = new Chart(document.getElementById("incidentBreakdown").getContext("2d")).Pie(pieData, {animationEasing:"easeOutQuart", animateScale:true});
}

function ionIncidentBreakdown(critical, high, medium, low) {
	var pieData = [{
						value: critical,
						color: criticalColor
					},
					{	
						value: high,
						color: highColor
					},
					{	
						value: medium,
						color: mediumColor
					},
					{	
						value: low,
						color: lowColor
					}];
	var myPie = new Chart(document.getElementById("incidentBreakdown").getContext("2d")).Pie(pieData, {animationEasing:"easeOutQuart", animateScale:true});
}

function cdnIncidentBreakdown(critical, high, medium, low) {
	var pieData = [{
						value: critical,
						color: criticalColor
					},
					{	
						value: high,
						color: highColor
					},
					{	
						value: medium,
						color: mediumColor
					},
					{	
						value: low,
						color: lowColor
					}];
	var myPie = new Chart(document.getElementById("incidentBreakdown").getContext("2d")).Pie(pieData, {animationEasing:"easeOutQuart", animateScale:true});
}