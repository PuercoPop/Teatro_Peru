function select_obra( elem ) {
	console.log(elem);
};
function clear_obra() {
	console.log(this);
};

$(document).ready(function() {
    $('#profile-pic').change(function() {
	$('img.profile-pic').src(this.asa);
    });

    $('#titulo').keyup(function(){
	if(this.value.length > 2){
	    $('#obra-related').load('/buscar/obra/titulo','term='+this.value);
	}

    });


    $('#temporada-start').datepicker({ 
	    buttonImage: "/media/static/images/calendar.gif",
	    showOn: "both",
    });

    $('#temporada-end').datepicker({ 
	    buttonImage: "/media/static/images/calendar.gif",
	    showOn: "both",
    });

    /* Validate Ticket
     */
    $('#agregar-entrada').click(function(){
	    $.ajax({
	        headers: {"X-CSRFToken": getCookie("csrftoken") },
	        url:"/validar_entrada/",
	        type: "POST",
	        data: { 'name': $('#entrada-tipo').val(),
	                'cost': $('#entrada-costo').val() },
	        success: function(data){
		        $('#entradas-info').append(data);
		        $('input.entrada-item').click(function(){
		            $(this).parent().remove();
		        });
	        }
	    });
    });

    /*  Validate Cast Member
     */
    $('#agregar-elenco').click(function(){
	    $.ajax({
	        headers: {"X-CSRFToken": getCookie("csrftoken")},
	        url:"/validar_elenco/",
	        type: "POST",
	        data: { 'role': $('#elenco-posicion').val(),
		            'name': $('#elenco-nombre').val(),
		          },
	        success: function(data){
		        $('#elenco-info').append(data);
		        $('input.elenco-item').click(function(){
		            $(this).parent().remove();
		        });
	        }
	    })
    });
});
