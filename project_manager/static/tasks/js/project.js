function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function project_put_status(project_id, state){
    fetch(`/project/${project_id}/status/put`, {
      method: 'PUT',
      body: JSON.stringify({status: state}),
      headers: { "X-CSRFToken": getCookie('csrftoken') }
    })
}

function project_put_priority(project_id, state){
    fetch(`/project/${project_id}/priority/put`, {
      method: 'PUT',
      body: JSON.stringify({priority: state}),
      headers: { "X-CSRFToken": getCookie('csrftoken') }
    })
}

function milestone_put_status(milestone_id, state){
    fetch(`/milestone/${milestone_id}/status/put`, {
      method: 'PUT',
      body: JSON.stringify({status: state}),
      headers: { "X-CSRFToken": getCookie('csrftoken') }
    })
}

function milestone_put_priority(milestone_id, state){
    fetch(`/milestone/${milestone_id}/priority/put`, {
      method: 'PUT',
      body: JSON.stringify({priority: state}),
      headers: { "X-CSRFToken": getCookie('csrftoken') }
    })
}

function milestone_put_assignment(milestone_id, member){
    fetch(`/milestone/${milestone_id}/assignment/put`, {
      method: 'PUT',
      body: JSON.stringify({assignment: member}),
      headers: { "X-CSRFToken": getCookie('csrftoken') }
    })
}

function milestone_delete(milestone_id){
    fetch(`/milestone/${milestone_id}/remove`, {
      method: 'DELETE',
      headers: { "X-CSRFToken": getCookie('csrftoken') }
    });

    document.getElementById(`milestone-${milestone_id}` ).style.display = "none";

}

function memberProjectAssignmentHandleChange(project_id, user) {
     fetch(`/project/${project_id}/member/put`, {
      method: 'PUT',
      body: JSON.stringify({member: user}),
      headers: { "X-CSRFToken": getCookie('csrftoken') }
    });

}

function openForm() {
  document.getElementById("form-container").style.display = "block";
}

function closeForm() {
  document.getElementById("form-container").style.display = "none";
}

function milestoneAction(milestone_id ) {
  document.getElementById(`${milestone_id}-milestone-actions` ).style.display = "table-cell";
  document.getElementById(`${milestone_id}-milestone-actions-trigger` ).style.display = "none";

}

function milestoneActionHide(milestone_id ) {
  document.getElementById(`${milestone_id}-milestone-actions` ).style.display = "none";
  document.getElementById(`${milestone_id}-milestone-actions-trigger` ).style.display = "table-cell";

}

function navItemActive(nav_id) {
    document.getElementById(`${nav_id}`).classList.add('active');
    document.getElementById(`${nav_id}`).classList.add('bg-gradient-primary');

}

function milestoneTaskHandleChange(task_id) {
     fetch(`/milestone/task/${task_id}/update`, {
      method: 'PUT',
      headers: { "X-CSRFToken": getCookie('csrftoken') }
    }).then(document.location.reload(true));
}