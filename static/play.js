function update_state(){
    get_hand()
    get_battlefield()
    get_stack()
	count_deck()
	count_graveyard()
    count_hand()
}

function get_stack(){
    url = window.location.href.split('/');
    code = url.at(-2)
    player = url.at(-1)
    $.get('/get_stack/'+code+'/'+player, function(res) {
        $('#stack').html(res)
    });
}

function tap(el){
	url = window.location.href.split('/');    
	code = url.at(-2)
    player = url.at(-1)

    card = el.src

    $.post('/tap/'+code+'/'+player, {url:card}, function(res) {        
        update_state()    
    })
}

function get_battlefield(){
    url = window.location.href.split('/');
    code = url.at(-2)
    player = url.at(-1)
    $.get('/get_battlefield/'+code+'/'+player, function(res) {
        $('#battlefield').html(res)
    });
}

function count_hand(){
	url = window.location.href.split('/');    
	code = url.at(-2)
    player = url.at(-1)

	$.get('/count_hand/'+code+'/'+player, function(res) {
		$('#handcount').html(res)
	})
}

function submit_list(){
    url = window.location.href.split('/');    
    code = url.at(-2)
    deckstring = $("#decklist_entry").val()
    $.post('/update_deck/'+code, {decklist:deckstring}, function(res) {
        update_state()
    })
}

function shuffle(){
	url = window.location.href.split('/');    
	code = url.at(-2)

	$.get('/shuffle/'+code, function(res) {
	})
}

function count_deck(){
	url = window.location.href.split('/');    
	code = url.at(-2)

	$.get('/count_deck/'+code, function(res) {
		$('#deckcount').html(res)
	})
}

function count_graveyard(){
	url = window.location.href.split('/');    
	code = url.at(-2)

	$.get('/count_grave/'+code, function(res) {
		$('#gravecount').html(res)
	})
}

function allowDrop(ev) {
      ev.preventDefault();
}

function remove_from_deck(card) {
    url = window.location.href.split('/');
    code = url.at(-2)

    $.post('/remove_from_deck/'+code, {url:card}, function(res) {
      update_state()
	  var myModalEl = document.getElementById('exampleModal');
      var modal = bootstrap.Modal.getInstance(myModalEl)
      modal.hide();
    })
}

function remove_from_graveyard(card) {
    url = window.location.href.split('/');
    code = url.at(-2)
    $.post('/remove_from_graveyard/'+code, {url:card}, function(res) {
      update_state()
	  var myModalEl = document.getElementById('exampleModal');
      var modal = bootstrap.Modal.getInstance(myModalEl)
      modal.hide();
    })
}

function add_to_battlefield_from_shared(card, source) {
  url = window.location.href.split('/');
  code = url.at(-2)
  player = url.at(-1)
  if(source == 'graveyard'){
    remove_from_graveyard(card)
  }
  else if(source == 'deck'){
    remove_from_deck(card)
  }
  $.post('/add_to_battlefield/'+code+'/'+player, {url:card}, function(res) {
    update_state()
  })
}

function handdrag(ev) {
  ev.dataTransfer.setData("source", ev.srcElement.parentElement.parentElement.id)
  ev.dataTransfer.setData("url", ev.target.src);
}

function battlefielddrag(ev) {
  ev.dataTransfer.setData("source", ev.srcElement.parentElement.parentElement.parentElement.id)
  ev.dataTransfer.setData("url", ev.target.src);
}

function remove_from_battlefield(card) {
    url = window.location.href.split('/');
    code = url.at(-2)
    player = url.at(-1)

    $.post('/remove_from_battlefield/'+code+'/'+player, {url:card}, function(res) {
      update_state()
    })
}

function add_to_graveyard(ev) {
  url = window.location.href.split('/');
  code = url.at(-2)
  ev.preventDefault();
  card = ev.dataTransfer.getData("url")
  source = ev.dataTransfer.getData("source")
  if(source == 'battlefield'){
    remove_from_battlefield(card)
  }
    else if(source == 'stack'){
    remove_from_stack(card)
  }
  else if(source == 'hand'){
    remove_from_hand(card)
  }
  $.post('/add_to_graveyard/'+code, {url:card}, function(res) {
    update_state()
  })
}

function add_to_deck(ev) {
  url = window.location.href.split('/');
  code = url.at(-2)
  ev.preventDefault();
  card = ev.dataTransfer.getData("url")
  source = ev.dataTransfer.getData("source")
  if(source == 'battlefield'){
    remove_from_battlefield(card)
  }
    else if(source == 'stack'){
    remove_from_stack(card)
  }
  else if(source == 'hand'){
    remove_from_hand(card)
  }
  $.post('/add_to_deck/'+code, {url:card}, function(res) {
    update_state()
  })
}

function remove_from_stack(card) {
    url = window.location.href.split('/');
    code = url.at(-2)
    player = url.at(-1)

    $.post('/remove_from_stack/'+code+'/'+player, {url:card}, function(res) {
      update_state()
    })
}

function add_to_stack(ev) {
  url = window.location.href.split('/');
  code = url.at(-2)
  player = url.at(-1)
  ev.preventDefault();
  card = ev.dataTransfer.getData("url")
  source = ev.dataTransfer.getData("source")
  if(source == 'battlefield'){
    remove_from_battlefield(card)
  }
    else if(source == 'stack'){
    remove_from_stack(card)
  }
  else if(source == 'hand'){
    remove_from_hand(card)
  }
  $.post('/add_to_stack/'+code+'/'+player, {url:card}, function(res) {
    update_state()
  })
}

function remove_from_hand(card) {
    url = window.location.href.split('/');
    code = url.at(-2)
    player = url.at(-1)

    $.post('/remove_from_hand/'+code+'/'+player, {url:card}, function(res) {
      update_state()
    })
}

function add_to_hand(ev) {
  url = window.location.href.split('/');
  code = url.at(-2)
  player = url.at(-1)
  ev.preventDefault();
  card = ev.dataTransfer.getData("url")
  source = ev.dataTransfer.getData("source")
  if(source == 'battlefield'){
    remove_from_battlefield(card)
  }
    else if(source == 'stack'){
    remove_from_stack(card)
  }
  else if(source == 'hand'){
    remove_from_hand(card)
  }
  $.post('/add_to_hand/'+code+'/'+player, {url:card}, function(res) {
    update_state()
  })
}

function add_to_battlefield(ev) {
  url = window.location.href.split('/');
  code = url.at(-2)
  player = url.at(-1)
  ev.preventDefault();
  card = ev.dataTransfer.getData("url")
  source = ev.dataTransfer.getData("source")
  if(source == 'battlefield'){
    remove_from_battlefield(card)
  }
  else if(source == 'hand'){
    remove_from_hand(card)
  }
    else if(source == 'stack'){
    remove_from_stack(card)
  }
  $.post('/add_to_battlefield/'+code+'/'+player, {url:card}, function(res) {
    update_state()
  })
}

function get_hand() {
    url = window.location.href.split('/');
    code = url.at(-2)
    player = url.at(-1)
    $.get('/get_hand/'+code+'/'+player, function(res) {
        $('#hand').html(res)
    });
}

function view_decklist(){
    url = window.location.href.split('/');
    code = url.at(-2)
    $.get('/get_decklist/'+code, function(res) {
        alert(res)
    });
}

function draw(amount){
    url = window.location.href.split('/');
    code = url.at(-2)
    player = url.at(-1)
    if(amount == -1){
        amount = $('#drawamount').val()
    }
    $.get('/draw/'+code+'/'+player+'/'+amount, function(res) {})
    update_state()
}

function mill(){
    url = window.location.href.split('/');
    code = url.at(-2)
    amount = $('#millamount').val()
    $.get('/mill/'+code+'/'+amount, function(res) {})
	update_state()
}

function view_graveyard(){
    url = window.location.href.split('/');
    code = url.at(-2)        
	$.get('/view_graveyard/'+code, function(res) {       
		$('#modalbody').html('<h5>Graveyard</h5><hr>'+res)
		myModal = new bootstrap.Modal(document.getElementById('exampleModal'))
		myModal.show()
	});
}

function view_deck(){
    url = window.location.href.split('/');
    code = url.at(-2)        
	$.get('/view_deck/'+code, function(res) {       
		$('#modalbody').html('<h5>Deck</h5><hr>'+res)
		myModal = new bootstrap.Modal(document.getElementById('exampleModal'))
		myModal.show()
	});
}

$( document ).ready(function() {
    update_state()
    setInterval(function(){    
        update_state()
    }, 500);
});
