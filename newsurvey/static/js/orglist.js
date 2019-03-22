$(document).ready(function(){
populate_table();
});

function populate_table(){
//    result_inside = null;
        $("#orgtab_row").empty();
        $.ajax({
           type:"GET",
            url: "/newsurvey/getorgdata",

          success: function(result) {
            console.log("print result",result);
            result_inside = result;
            $.each(result,function(key,value){
            var tr = $("<tr>");

            tr.append("<td>"+(value[0])+"</td>")
            tr.append("<td>"+value[1]+"</td>")
            tr.append("<td>"+value[2]+"</td>")
            tr.append("<td>"+value[3]+"</td>")
            tr.append('<td><i class="fa fa-trash deletebtn" id="org_'+key+'" aria-hidden="true"></i></td>')
//            delete_org(key, value[1]);
            $("#orgtab_row").append(tr);
            })
            $('.deletebtn').on('click',function(){
                alert('hiiiii')
                clicked = $(this);
                key = this.id.split("_")[1];
                $.ajax({
                    type: "GET",
                    url: "/newsurvey/deleteorg/?company_name="+result[key][1],
//                    data: "{company_name:"+result[key][1]+"}",

                    success: function (result){
                        populate_table();
                    },
                    error: function (result){
                        alert("Error");
                        console.log(result);
                    }

                    });
                console.log("thisattt",this.id)
 });
          },
          error: function(result) {
            alert('error');
          }
        });
//    console.log(result_inside);
}

function delete_org(list_id, company_name){
    console.log("-------", list_id);

    $.ajax({
    type: "DELETE",
    url: "/newsurvey/deletedata",
    data: "{company_name:"+company_name+"}",

    success: function (result){
        populate_table();
    },
    error: function (result){
        alert("Error");
    }

    });

}