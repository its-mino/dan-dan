function createroom(){
	fetch('/createroom')
	  .then(response => response.text())
  	  .then(data => window.location.href = '/play/'+data);
}

function joinroom(){
    code = $('#codejoin').val()
    $.get('/check_code/'+code, function(res) {
        if(res == 'Invalid Code'){
            alert(res)
        }
        else{
            window.location.href = '/play/'+code+'/2';
        }
    });
}
