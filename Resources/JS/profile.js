var userid;
var apigClient;
var pageNum;
var accessToken;
$('document').ready(function () {
	//var url = window.location.href;
	/*if (url.includes('access_token')) {
		console.log('changing access token');
		accessToken = url.split('#')[1].split('&')[1].split('=')[1];
		window.localStorage.setItem('access-token', accessToken);
	}*/
	var params = {};
	//foundaccessToken = window.localStorage.getItem('found-access-token');
	/*if(foundaccessToken=='1'){
		accessToken = window.localStorage.getItem('access-token');
		window.localStorage.removeItem('found-access-token');
	}else{
		if (url.includes('code')) {
			console.log('changing code token');
			accessToken = url.split('=')[1];
			//window.localStorage.setItem('access-token', accessToken);
			params['token_found']='false'
		}else{
			accessToken = window.localStorage.getItem('access-token');
		}
	}
	*/
	if (window.localStorage.getItem('access-token')==null || window.localStorage.getItem('access-token')=='null')
		window.location = "signout.html";
	userid = window.localStorage.getItem('userid');
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
    apigClient.profileGet(params, body)
        .then(function (result) {
		  jsonobj=JSON.parse(result.data.body);
		  if (result.invalid_access_token=='1' || result.data.invalid_access_token=='1')
			window.location = "https://befitmealdelivery.auth.us-east-1.amazoncognito.com/login?client_id=xxxxxxxxxxxxxxxxxx&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https://mealdeliveryapp.s3.amazonaws.com/Resources/HTML/dashboard.html";
		  populateFields(jsonobj);
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

function populateFields(data) {
	console.log("user id is "+data.user_id);
	//userid = data.user_id;
	//window.localStorage.setItem('userid', data.user_id);
	//window.localStorage.setItem('access-token', data.access_token);
	pageNum = data.completion_level;
	console.log("pageNum type is "+(typeof pageNum));
	console.log("pageNum is "+pageNum);
	//if (pageNum<5)
	//	redirectPage(pageNum);
	if (Object.keys(data).length>2) {

		$('#userName').val(data.userName);
		$('#age').val(data.age);
		$('#gender').val(data.gender);
		$('#ethnicity').val(data.ethnicity);
		$('#height').val(data.height);
		$('#weight').val(data.weight);
		//$('#targetWeight').val(data.targetWeight);
		$('#street').val(data.street);
		$('#city').val(data.city); // 0-Little to no exercise, 1-Light exercise, 2-Moderate exercise, 3-Heavy exercise, 4-Very heavy exercise
		$('#phoneNo').val(data.phoneNo);
		$('#user_state').val(data.user_state); // vegan, ovovegan, lacvegan, lacovovegan, pesce
		$('#activity').val(data.activity);
		$('#medicalCondition').val(data.medicalCondition);
		$('#dietaryPreference').val(data.dietaryPreference);
		$('#allergies').val(data.allergies);
		$('#cuisine').val(data.cuisine);
		$('#bmi').text(data.bmi);
		$('#caloriesConsumption').text(data.calories);
		if(data.mealpreference!=null){
			let myArray = data.mealpreference.split(",");
			for (var i = 0; i < myArray.length; i++) {
				if(myArray[i]!=null && myArray[i]!="")
					$('#'+myArray[i]).prop( "checked", true );
			}
		}
	}
	$('#loading').hide();
}

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

function update() {
	console.log('Line 118 reached')
	$('#loading').show();

	mealpreference="";
	if($("#lowsalt").prop("checked") == true){
		mealpreference=mealpreference+"lowsalt"+",";
    }
	if($("#lowcarb").prop("checked") == true){
		mealpreference=mealpreference+"lowcarb"+",";
    }
	if($("#lowfat").prop("checked") == true){
		mealpreference=mealpreference+"lowfat"+",";
    }
	if($("#lowcholestrol").prop("checked") == true){
		mealpreference=mealpreference+"lowcholestrol"+",";
    }
	if($("#highprotein").prop("checked") == true){
		mealpreference=mealpreference+"highprotein"+",";
    }
	if($("#highfiber").prop("checked") == true){
		mealpreference=mealpreference+"highfiber"+",";
    }
	if($("#lowsugar").prop("checked") == true){
		mealpreference=mealpreference+"lowsugar"+",";
    }
	if($("#lowcalorie").prop("checked") == true){
		mealpreference=mealpreference+"lowcalorie"+",";
    }
	if($("#pescetarian").prop("checked") == true){
		mealpreference=mealpreference+"pescetarian"+",";
    }
	if($(glutenfree).prop("checked") == true){
		mealpreference=mealpreference+"glutenfree"+",";
    }
	var body = {
		"user_id" : userid,
		"page_num" : pageNum,
		"userName" : $('#userName').val(),
		"age" : $('#age').val(),
		"gender" : $('#gender').val(),
		"ethnicity" : $('#ethnicity').val(),
		"height" : $('#height').val(),
		"weight" : $('#weight').val(),
		"targetWeight" : $('#targetWeight').val(),
		"activity" : $('#activity').val(),
		"medicalCondition" : $('#medicalCondition').val(),
		"dietaryPreference" : $('#dietaryPreference').val(),
		"allergies" : $('#allergies').val(),
		"cuisine" : $('#cuisine').val(),
		"street" : $('#street').val(),
		"city" : $('#city').val(),
		"user_state" : $('#user_state').val(),
		"phoneNo" : $('#phoneNo').val(),
		"mealpreference":mealpreference
	};
	console.log("body from update is "+body);
	var username;
	var params = {username: userid, body: body};
	console.log("body 2 is :"+body);
	console.log("params is "+params)
	apigClient.profilePost(params, body)
	.then(function (result) {
	  $('#submitnote').removeAttr('hidden');
	  console.log("pageNum from update is "+pageNum)
	  //window.location.href= 'preferences.html';
	  console.log("result logged is "+result);
	}).catch(function (result) {
	  alert('Permission Denied');
	  setTimeout(function(){ console.log("result 2 is : "+result);}, 150000);
	  console.log("Something went wrong!");
	});
	return false;
}

async function getRecommendation() {
	console.log("inside recommendation")
	$('#loading').show();
	userid = window.localStorage.getItem('userid');
	//console.log(userid);
    // var params = {username : recomuserid, user_id:recomuserid};
    // var additionalParams = {headers: {
    //   'Content-Type':"application/json"
    // }};
	// var body = {
    //     key : "Hello"
    // };
	// apigClient.preferencesGet(params, body)
    //     .then(function (result) {
    //       console.log(result);
	// 	  console.log(typeof result.data);
	// 	  //populateFields(result.data);
    //     }).catch(function (result) {
    //       alert('Permission Denied')
    //       console.log(result);
    //       console.log("Something went wrong!");
    //     });

	console.log("Clicked Recommendation button")
	const response = await fetch("https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/getrecommendations/", {
		method: "GET",
		headers: { "Content-Type": "application/json" }
	});
	const { body } = await response.json();
	console.log("Received orderId");
	console.log(body);
	let url = "https://mealdeliveryapp.s3.amazonaws.com/Resources/HTML/recommendation.html?userId=" + userid

	window.location.replace(url);

}
