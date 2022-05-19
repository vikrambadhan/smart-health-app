var userid;
var apigClient;
var pageNum;
var accessToken;
$('document').ready(function () {
	var url = window.location.href;
	var params = {};
	foundaccessToken = window.localStorage.getItem('found-access-token');	
	
	if(foundaccessToken=='1'){	
		//accessToken = window.localStorage.getItem('access-token');		
		window.localStorage.removeItem('found-access-token');	
		userid = window.localStorage.getItem('userid');		
	}else{
		if (url.includes('code')) {
			console.log('changing code token');
			userid = url.split('=')[1];
			params['token_found']='false'		
		}else{
			userid = window.localStorage.getItem('userid');	
			//accessToken = window.localStorage.getItem('access-token');	
		}
	}
	
	//else {
	//	accessToken = window.localStorage.getItem('access-token');
	//	params['token_found']='true'
	//}
	params['username']=userid;
	params['user_id']=userid;
	//if (window.localStorage.getItem('access-token')==null || window.localStorage.getItem('access-token')=='null')
	//	window.location = "signout.html";
    apigClient = apigClientFactory.newClient();
    var body = {
        key : "Hello"
    };
    // var params = {username : accessToken, user_id : accessToken, token_found:'true'};
      var additionalParams = {headers: {
      'Content-Type':"application/json"
    }};
	//console.log("username is "+username)
    apigClient.dashboardGet(params, body)
        .then(function (result) {
		  jsonobj=JSON.parse(result.data.body);
		  if(jsonobj.found_access_token=='1'){
			window.localStorage.setItem('access-token', jsonobj.access_token);
			window.localStorage.setItem('userid', jsonobj.user_id);
			window.localStorage.setItem('found-access-token', '1');
			window.location = "dashboard.html";
		  }else if (result.invalid_access_token=='1' || result.data.invalid_access_token=='1')
			window.location = "https://macrochef.auth.us-east-1.amazoncognito.com/login?client_id=cxxxxxxxxxxx&response_type=token&scope=phone+email+openid+aws.cognito.signin.user.admin+profile&redirect_uri=https://macrochef.s3.amazonaws.com/Resources/HTML/profile.html";
		  //populateFields(jsonobj);
        }).catch(function (result) {
          alert('Permission Denied')
          console.log("result on failure is "+result);
          console.log("Something went wrong!");
        });  
	$( '#activity, #sex, #age, #height, #weight').change(function() {
		var sex = document.getElementById("sex").value;
		var age = document.getElementById("age").value;
		var height = document.getElementById("height").value;
		var weight = document.getElementById("weight").value;
		var activity = document.getElementById("activity").value;
		var bmr = 0;
		var dci = 0;
		if(sex == "male"){
			bmr = (10*weight) + (6.25*height) - (5*age) + 5;
		} else if(sex == "female"){
			bmr = (10*weight) + (6.25*height) - (5*age) - 161;
		} else {
			bmr = (10*weight) + (6.25*height) - (5*age) + 5;
		}
		if(activity == "0") {
			dci = bmr*1.2;
		} else if(activity == "1") {
			dci = bmr*1.375;
		} else if(activity == "2") {
			dci = bmr*1.55;
		} else if(activity == "3") {
			dci = bmr*1.725;
		} else if(activity == "4") {
			dci = bmr*1.9;
		} else{
			dci = bmr*1.2;
		}
		dci = Math.round(dci);
		var bmi = Math.round( (weight/Math.pow(height/100, 2)) * 10 ) / 10;
		document.getElementById("calorieintake").placeholder = "Suggested Calorie Intake "+dci+" Kcal/day";
		var note = "Your BMI is "+bmi+" kg/m"+"2".sup()+"\nTo maintain your weight you need "+dci+" Kcal/day\nTo lose 0.5 kg per week you need "+(dci-500)+" Kcal/day\nTo lose 1 kg per week you need	"+(dci-1000)+" Kcal/day\nTo gain 0.5 kg per week you need "+(dci+500)+" Kcal/day<br>To gain 1 kg per week you need "+(dci+1000)+" Kcal/day"
		document.getElementById("calnote").innerHTML = "<pre>" + note + "</pre>"
	});
  });


function redirectPage(pageNum) {
	$('#redirect-bar').remove();
	console.log("redirecting to page "+pageNum);
	if (pageNum==1) {
		window.location = "preferences.html";
	} else if (pageNum==2) {
		window.location = "calendar.html";
	} else if (pageNum==3) {
		window.location = "addressbook.html";
	} else if (pageNum==4) {
		window.location = "billinginfo.html";
	}
}