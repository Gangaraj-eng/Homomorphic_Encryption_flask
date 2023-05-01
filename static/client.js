
console.log("Hello")

async function signup()
{
  console.log("slkdfklsjf")
  document.getElementById('signupLoader').style.display="block"
  document.getElementById('singupText').style.display="none"
  firstName=document.getElementById('firstname').value 
  lastName=document.getElementById('lastname').value 
  email=document.getElementById('email').value 
  Password=document.getElementById('password').value 
  confirmPassword=document.getElementById('confirmpassword').value 
 
  if(firstName.toString().length=="")
  {
    displayErrorMsg("Please enter valid First Name","signupLoader","singupText")
    return
  }
  if(lastName.toString().length=="")
  {
    displayErrorMsg("Please enter valid Last Name","signupLoader","singupText")
    return
  }
  if(email.toString().length=="")
  {
    displayErrorMsg("Please enter valid Email","signupLoader","singupText")
    return
  }
  
  if(Password.toString().length<5)
  {
    displayErrorMsg("Password should be atleast five characters","signupLoader","singupText")
    return
  }
  if(Password.toString()!=confirmPassword.toString())
  {
    displayErrorMsg("Password and confirm password should be same","signupLoader","singupText")
    return
  }
  const host=window.location.protocol+'//'+window.location.host;
  const response = await fetch(`${host}/signup`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ firstName, lastName, email,Password })
});

let json = await response.json();
    
if (json.success) {
    window.location.replace(host)
    localStorage['token']='token'

}else {
        displayErrorMsg(json.message,"signupLoader","singupText")
}
}

async function Login()
{
  
  document.getElementById('loginLoader').style.display="block"
  document.getElementById('loginText').style.display="none"
  email=document.getElementById('email').value 
  Password=document.getElementById('password').value 
 
  
  if(email.toString().length=="")
  {
    displayErrorMsg("Please enter valid Email","loginLoader","loginText")
    return
  }
  
  if(Password.toString().length<5)
  {
    displayErrorMsg("Password should be atleast five characters","loginLoader","loginText")
    return
  }
 
  const host=window.location.protocol+'//'+window.location.host;
  const response = await fetch(`${host}/login`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({  email,Password })
});

let json = await response.json();
    
if (json.success) {
    window.location.replace(host)
    localStorage['token']='token'

}else {
 
        displayErrorMsg(json.message,"loginLoader","loginText")
}
}


function displayErrorMsg(msg,idloader,idtext)
{
  console.log(msg,idloader,idtext)
  errorBox=document.getElementById('errormsg')
  errorText=document.getElementById('errorText')
  errorBox.style.visibility="visible"
  document.getElementById(idloader).style.display="none"
  document.getElementById(idtext).style.display="block"
  errorText.innerHTML =msg
  setTimeout(function() {
    errorBox.style.visibility="hidden"
}, 2500);
}


async function GetResults(json_data_excel)
{
   
  console.log(json_data_excel)
  mytableheaders=json_data_excel[0]
  document.getElementById('FetchingResults').style.display="flex"
  document.getElementById('AfterUpload').style.display="none"
  document.getElementById('table_view').style.display="none"
  const host=window.location.protocol+'//'+window.location.host;
  const response = await fetch(`${host}/perFormCalculations`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ json_data_excel })
  })
  let json=await response.json();
  let student_wise_total=JSON.parse(json['student_wise_total'])
  var table_after=document.getElementById("mytable2")
  let i=1
  for(x in json_data_excel)
  {
    if(x==0)continue
    var student_id=json_data_excel[x][0]
    var total_marks=student_wise_total[x-1]
    var avg_margs=total_marks/3
    var grades=['AA','AB','BB','BC','CC','CD','DD','DE','EE','F']
    var grade='AA'
    if(avg_margs>=90 ) grade='AA'
    else if(avg_margs>=80) grade='AB'
    else if(avg_margs>=70) grade='BB'
    else if(avg_margs>=60) grade="BC"
    else if(avg_margs>=50) grade='CC'
    else if(avg_margs>=40) grade='CD'
    else if(avg_margs>=30) grade="DD"
    else if(avg_margs>=20) grade="DE"
    else if(avg_margs>=10) grade="EE"
    else grade="F"
    let row=table_after.insertRow(i)
    i=i+1
    let cell1=row.insertCell(0)
    let cell2=row.insertCell(1)
    let cell3=row.insertCell(2)
    let cell4=row.insertCell(3)
    cell1.innerHTML=student_id
    cell2.innerHTML=total_marks
    cell3.innerHTML=Math.round(avg_margs * 100) / 100
    cell4.innerHTML=grade

  }
  document.getElementById('FetchingResults').style.display="none"
  document.getElementById('AfterResults').style.display="block"
  var subjTable=document.getElementById('mytable3')
  var row1=subjTable.insertRow(1)
  var cell1=row1.insertCell(0)
  cell1.innerHTML=mytableheaders[1]
  var cell2=row1.insertCell(1)
  cell2.innerHTML=json['chemistry_total']/(json_data_excel.length-1)
   row1=subjTable.insertRow(1)
   cell1=row1.insertCell(0)
  cell1.innerHTML=mytableheaders[2]
   cell2=row1.insertCell(1)
  cell2.innerHTML=json['physics_total']/(json_data_excel.length-1)
   row1=subjTable.insertRow(1)
  cell1=row1.insertCell(0)
  cell1.innerHTML=mytableheaders[3]
   cell2=row1.insertCell(1)
  cell2.innerHTML=json['maths_total']/(json_data_excel.length-1)
  
}

