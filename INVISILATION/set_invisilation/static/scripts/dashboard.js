
let nodeID = null;
let submitNodeButton = document.getElementById("submitNode");
let selected_job = null;

document.getElementById("logoutButton").addEventListener("click",function(){
    $.ajax({
        type: 'POST',
        url: 'http://localhost:3000/logout',
        success:function(resultData){
            window.location.href = resultData.redirect;
        }
    }); 

});

function fetchPendingJobs() {
    document.getElementById("id_nodegui").innerHTML = "";
    nodeID = document.getElementById("id_login").value;
    $.ajax({
        type: 'GET',
        url: 'http://localhost:3000/'+nodeID+'/getjobs',
        success: (data) => {
            document.getElementById("id_pending").innerHTML = data;
            submitNodeButton.setAttribute("form",nodeID+"_form");
        },
        error: function (jqXHR, exception) {
            var msg = '';
            if (jqXHR.status === 0) {
                msg = 'Not connect.\n Verify Network.';
            } else if (jqXHR.status == 404) {
                msg = 'Requested node not found.';
                document.getElementById("id_login").value = "";
            } else if (jqXHR.status == 500) {
                msg = 'Internal Server Error.';
            } else if (exception === 'parsererror') {
                msg = 'Requested JSON parse failed.';
            } else if (exception === 'timeout') {
                msg = 'Time out error.';
            } else if (exception === 'abort') {
                msg = 'Ajax request aborted.';
            } else {
                msg = 'Uncaught Error.\n' + jqXHR.responseText;
            }
            alert(msg);
        }
        
    });
}

function registerInvisilator() {
    document.getElementById("id_pending").innerHTML = "";
    $.ajax({
        type: 'GET',
        url: 'http://localhost:3000/set_invisilation_register/register',
        success: (data) => {
            nodeID = 'set_invisilation_register';
            document.getElementById("id_nodegui").innerHTML = data;
            submitNodeButton.setAttribute("form", nodeID+"_form");
        }
    });
    
}

function renderJob() {
    let choices = document.getElementsByName("job_name");
    for (var i = 0; i < choices.length; i++) {
        if (choices[i].checked) {
            selected_job = choices[i].value;
        }
    }
    if (selected_job == null) {
        alert("Select a job");
        return;
    }
    $.ajax({
        type: 'GET',
        url: 'http://localhost:3000/'+nodeID+'/renderjob/'+ selected_job,
        success: (data) => {
            document.getElementById("id_nodegui").innerHTML = data;
        }
    });

}