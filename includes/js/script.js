
var sectionList = ["mainPage","resume","contact","portfolio"];


function insurance1buttonClick(){

  document.getElementById("insurance1div").classList.remove("hiddenSection");
  document.getElementById("insurance1Editdiv").classList.remove("hiddenSection");

  document.getElementById("insurance2div").classList.add("hiddenSection");
  document.getElementById("insurance2div").classList.remove("row");

  //document.getElementById("insurance2Editdiv").classList.add("hiddenSection");

}

function reloadPageClick(){
  alert("use web service to reload after save");

location.reload();
  //window.reloadPage();
  return false;

}




function showSection(sectionName){

    var i;
    for(i=0;i < sectionList.length;i++){
        //alert(sectionList[i] + "Link");
        document.getElementById(sectionList[i]).classList.remove("visibleSection");
        document.getElementById(sectionList[i]).classList.add("hiddenSection");

        document.getElementById(sectionList[i] + 'Link').classList.remove("activeLink");
        document.getElementById(sectionList[i] + 'Link').classList.add("inactiveLink");

    }

    document.getElementById(sectionName).classList.add("visibleSection");
    document.getElementById(sectionName + 'Link').classList.remove("inactiveLink");
    document.getElementById(sectionName + 'Link').classList.add("activeLink");


}

function contactSubmit(){

    let subject = document.getElementById("contactSubject").value;
    let message = document.getElementById("contactMessage").value;

    alert("Your message:" + message + " has been submitted with subject " + subject);

    document.getElementById("contactSubject").value = "";
    document.getElementById("contactMessage").value = "";

    document.getElementById("submitButton").classList.add("disabledInput");


}

function activateSubmit(){

    document.getElementById("submitButton").classList.remove("disabledInput");

}

function revealEmail(){

    const builtEmailAddyStart = "le" + "a" + "rb@";
    const builtEmailAddyEnd = "u" + "a" + "b." + "edu";



    document.getElementById("emailAddress").innerText=builtEmailAddyStart + builtEmailAddyEnd;

}
