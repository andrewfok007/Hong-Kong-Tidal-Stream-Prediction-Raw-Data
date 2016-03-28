function knots_to_power(knots){
    v = knots*0.514;
    return (q*a*Math.pow(v, 3)*cp/2)/1000
}

function update_power_gen_params(){
    cp = $("#cp").val();
    q = $("#q").val();
    a = $("#r").val()*3.14;
}

$(document).ready(function(){
    $('.date i').click(function() {
      $(this).parent().find('input').click();
    });

    function clear_page(){
        $('#data_table').html("");
        $("#visualisation").html("");
        var html = "<tr>"
        html += "<td align=center>Time</td>"
        html += "<td align=center>Interval</td>"
        html += "<td align=center>Knots</td>"
        html += "<td align=center>Degree</td>"
        html += "<td align=center>Latitude(WGS84)</td>"
        html += "<td align=center>Longitude(WGS84)</td>"
        html += "</tr>"
        $('#data_table').append(html);
        counter = 0;
    }

    var counter = 0

    function gen_data_table(from, to){
        from = from.format('DD-MM-YYYY H:mm:00');
        to = to.format('DD-MM-YYYY H:mm:00');
        mode = String($('#hydro_option').val());
        $.ajax({
            type: "GET",
            url: window.location.protocol + "//" + window.location.host +
                    "/updateJSON/?start="+from+"&end="+to+"&mode="+mode,
            dataType: 'json',
            success: function(data) {
                var HTML = "<tr>"
                $.each(data, function(index, element) {                              
                    HTML += "<td align=center>"+String(element.date)+"</td>";
                    HTML += "<td align=center>"+String(element.prediction_interval+counter*1172)+"</td>";
                    HTML += "<td align=center>"+String(element.knots)+"</td>";
                    HTML += "<td align=center>"+String(element.degree)+"</td>";
                    HTML += "<td align=center>"+String(element.latitude)+"</td>";
                    HTML += "<td align=center>"+String(element.longitude)+"</td>";
                    HTML += "</tr>"
                    data[index].prediction_interval = data[index].prediction_interval+counter*1172;
                });
                $('#data_table').append(HTML);
                append_new_data(data);
                counter+=1;
            },
            async: false
        });
    }

    function append_new_data(data){
        graph_data = graph_data.concat(data);
    }

    function updateConfig(){

        var options = {
            timePicker: true,
            timePickerIncrement: 15
        };

        $('#date-picker').daterangepicker(
            options,
            function(start, end, label){
                if (typeof _start == "undefined" && typeof _end == "undefined" || _start != start){
                    clear_page()
                    graph_data = [];
                    _start = moment(start);
                    _end = moment(end);
                    _from = moment(_start);
                    _to = moment(_from).add(15, 'minutes');
                    gen_data_table(_from, _to);
                    update_power_gen_params();
                    update_chart(graph_data);
                }else if(_end != end){
                    if(end.isBefore(_to)){
                        alert("Data is shown already")
                    }else if(end.isAfter(_to)){
                        _end = end;
                    }
                }
            }
        );
    }

    function getDocHeight() {
        var D = document;
        return Math.max(
            D.body.scrollHeight, D.documentElement.scrollHeight,
            D.body.offsetHeight, D.documentElement.offsetHeight,
            D.body.clientHeight, D.documentElement.clientHeight
        );
    }

    var _start = undefined;
    var _end = undefined;
    var _from = undefined;
    var _to = undefined;
    var graph_data = [];
    var q, cp, a;

    updateConfig();

    $(window).scroll(function(){
           if($(window).scrollTop() + $(window).height() == getDocHeight()) {
                if(typeof _from != undefined && typeof _to != undefined && _to.isSame(_end) || _to.isBefore(_end)) {
                    _from = moment(_to);
                    _to = moment(_to).add(15, 'minutes');
                    gen_data_table(_from, _to);
                    update_chart(graph_data);
                }else if(_to.isAfter(_end)){
                    alert("End of Query Data!");
                }
           }
    });

});
