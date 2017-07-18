/**
 * Created by Cynthia on 11/3/2016.
 */

//autocomplete search
$(function (){

    var ajax_url = '/ajax_calls/classdata';
    var class_data = {}
    $.get(ajax_url, function(data){
       class_data = data
    });

    function custom_source(request, response) {
        var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
        response($.grep(class_data, function(value) {
            return matcher.test(value.value);
        }).slice(0,5));
    }

    $("#search").autocomplete({
        source: custom_source,
        minLength: 0,
        select: function(event, ui) {
            $('#search').val(ui.item.value);
            $('#id').val(ui.item.id);
            $('#course_search_form'); //.trigger('submit');
        }
    }).autocomplete("instance")._renderItem = function(ul, item) {
        var detail_url = "/course/"+item.id;
        return $( "<li></li>" )
            .data( "item.autocomplete", item )
            .append( "<a class='teacher-profile-pic' href='"+detail_url+"'>" + "<img src='" + item.img + "' />" + item.label+ "</a>" )
            .append( "<a class='course-list-teacher' href='"+detail_url+"'>" + " by " + item.teacher + " ("+ item.category +")" )
            .appendTo( ul );
    };
});
$(function(){
   $("ul.ui-autocomplete").addClass('ui-add-fixed-position');
});
//time picker
//$(function(){
//    $("#id_from_time").timepicker({
//        'minTime': '8:00am',
//        'maxTime': '8:00pm',
//        'step': '60',
//        'timeFormat': 'H:i'
//    });
//    $("#id_to_time").timepicker({
//        'minTime': '8:00am',
//        'maxTime': '8:00pm',
//        'step': '60',
//        'timeFormat': 'H:i'
//    });
//});

//parse data into json when click on add link
//$("#datas").hide();
//$("#add_new").click(function(){
//
//
//    var day = $("#id_int_day").val();
//    var from_time = $("#id_from_time").val();
//    var to_time = $("#id_to_time").val();
//
//    var jsonArray = [];
//    var jsonObj = {};
//    jsonObj.day = day;
//    jsonObj.from_time = from_time;
//    jsonObj.to_time = to_time;
//    jsonArray.push(jsonObj);
//
//    var hidden_data = $('#hidden_data').val();
//    hidden_data = jsonObj
//    console.log(hidden_data);
//    $("#datas").text(hidden_data);
//});
$(function(){
   var existing_time_slot_count = $('#existing_time_slot_count').val();
   if (existing_time_slot_count !=0 && existing_time_slot_count != undefined){
       var exist_data = JSON.parse(atob($("#exist_time_slot").val()));
       for(var i=0;i< existing_time_slot_count;i++) {
           cloneMore('div.table:last', 'edit', exist_data[i][0], exist_data[i][1], exist_data[i][2]);
       }
   }
});
$('#add_new').click(function () {
    cloneMore('div.table:last', 'new', '', '', '');
});
function cloneMore(selector, type, int, from, to) {
    var newElement = $(selector).clone(true);

    if (type == 'edit'){
        var tblID = newElement.attr("id").match(/\d+$/);
        newElement.attr("id", newElement.attr("id").replace(tblID, parseInt(tblID) + 1));
    }
    $(selector).after(newElement);
    if (type == "edit") {
        $("#" + newElement.attr("id")).find("#id_from_time option[value='" + from + "']").prop('selected', true);
        $("#" + newElement.attr("id")).find("#id_to_time option[value='" + to + "']").prop('selected', true);
        $("#" + newElement.attr("id")).find("#id_int_day option[value='" + int + "']").prop('selected', true);
        if (from <= to){
            $("#" + newElement.attr("id") + " label[for='id_to_time']").parent().removeClass('has-error');
            $("#" + newElement.attr("id") + " label[for='id_to_time']").parent().find(".help-block ").html('');
        }
        if (from >= to) {
            $("#" + newElement.attr("id") + " label[for='id_to_time']").parent().addClass('has-error');
            $("#" + newElement.attr("id") + " label[for='id_to_time']").parent().find(".help-block ").html('To Time must be greater than From Time.');
        }
        $("#time_slot_table1").remove();
    }
}

$(function(){
    $('.from_time_slot').on('change', function () {
        var from_time = $(this).val();
        parent_id = $(this).parents('.table').attr('id');
        $("#"+parent_id+" #id_to_time option").each(function () {
            var to_time = $(this).val();
            if (to_time && to_time <= from_time) {
                $(this).hide();
            }
            else {
                $(this).show();
            }
        });
    }).change();
    $('.to_time_slot').on('change', function () {
        var to_time = $(this).val();
        parent_id = $(this).parents('.table').attr('id');
        $("#" + parent_id + " #id_from_time option").each(function () {
            var from_time = $(this).val();
            if (from_time && from_time >= to_time) {
                $(this).hide();
            }
            else {
                $(this).show();
            }
            if (to_time == "") {
                $("#" + parent_id + " #id_from_time option").each(function () {
                    $(this).show();
                })
            }
        });
    }).change();
});

$('#delete_new').click(function(){
    var timeslot_length = $('.table').length;
    if (timeslot_length >1){
    $(this).closest('#'+ $(this).closest('.table').attr('id')).remove();}
});

// Date time for DOB search
//$('#dob_datetimepicker').datetimepicker({
//    useCurrent: false,
//    format: 'YYYY-MM-DD'
//});


$('#from_date_datetimepicker').datetimepicker({
    useCurrent: false,
    format: 'YYYY-MM-DD'
});
$('#to_date_datetimepicker').datetimepicker({
    useCurrent: false,
    format: 'YYYY-MM-DD'
});

// from time and to time for search
$(function(){
    $('#id_search_from_time').on('change', function () {
        var from_time = $(this).val();
        $('#id_search_to_time option').each(function () {
            var to_time = $(this).val();
            if (to_time && to_time <= from_time) {
                $(this).hide();
            }
            else{
                $(this).show();
            }
        });
    }).change();
    $('#id_search_to_time').on('change', function () {
        var to_time = $(this).val();
        $('#id_search_from_time option').each(function () {
            var from_time = $(this).val();
            if (from_time && from_time >= to_time) {
                $(this).hide();
            }
            else {
                $(this).show();
            }
            if (to_time == ""){
                $("#id_search_from_time option").each(function(){
                    $(this).show();
                })
            }
        });
    }).change();
});

//custom notification list
function custom_notification_list(data) {
    var menu = document.getElementById(notify_menu_id);
    if (menu) {
        menu.innerHTML = "";
        for (var i=0; i < data.unread_list.length; i++) {
            var item = data.unread_list[i];
            var message = ""
            if(typeof item.actor !== 'undefined'){
                message = item.actor;
            }
            if(typeof item.verb !== 'undefined'){
                message = message + " " + item.verb;
            }
            //if(typeof item.target !== 'undefined'){
            //    message = message + " " + item.target + ".";

            if(typeof item.description !== 'undefined'){
                message = message + " " + item.description + ".";
            }
            if(typeof item.timestamp !== 'undefined'){
                message = message + " " + timeSince(item.timestamp) + " ago.";
            }
            menu.innerHTML = menu.innerHTML + "<li><a href = ' " + window.notificationURL.replace(0, item.target_object_id) + "'>" + message + "</a></li>";
        }
    }
}
function timeSince(date){
    if (typeof date !== 'object') {
        date = new Date(date);
    }
    var seconds = Math.floor((new Date() - date) / 1000);
    var interval = Math.floor(seconds / 31536000);
    var interval_minute;
    var intervalType;
    var interval_minute_type;

    if (interval >= 1) {
        intervalType = 'year';
    } else {
        interval = Math.floor(seconds / 2592000);
        if (interval >= 1) {
            intervalType = 'month';
        }
        else {
            interval = Math.floor(seconds / 86400);
            if (interval >= 1) {
                intervalType = 'day';
            }
            else {
                interval = Math.floor(seconds / 3600);
                if (interval >= 1) {
                    interval_minute = Math.floor(seconds/60) - (interval * 60); //1hour 52 minutes
                    intervalType = "hour";
                    interval_minute_type = "mintue"
                } else {
                    interval = Math.floor(seconds / 60);
                    if (interval >= 1) {
                        intervalType = "minute";
                    } else {
                        interval = seconds;
                        intervalType = "second";
                    }
                }
            }
        }
    }
    if (interval > 1 || interval === 0) {
        intervalType += 's';
    }
    if (interval_minute > 1 || interval_minute === 0){
        interval_minute_type += 's';
    }
    if (interval_minute) {
        return interval + ' ' + intervalType + ', ' + interval_minute + ' ' + interval_minute_type;
    }else{
        return interval + ' ' + intervalType;
    }
};

//apply now btn events
$(function(){
   $(".apply-btn").click(function(){
       var user_id = $("#user_id").val();
       var course_id = $("#course_id").val();

       var loading = $(".loading")
       var success = $(".success")
       var error = $(".error")
       var existing_student = $(".existing_student")

       $.ajax({
           url: '/ajax/apply/check',
           type: "get",
           dataType: "json",
           data: {"user_id": user_id, "course_id": course_id},

           beforeSend: function(response){
               loading.show();
               success.hide();
               error.hide();
               existing_student.hide();
           },
           success: function(data){
               var message = data.message;
               loading.hide();
               if (message == 'success'){
                   success.show();
               }
               else if(message == 'existing_student'){
                   existing_student.show();
               }
               else{
                   error.show();
               }
           },
           error: function(data){
               loading.hide();
               error.show();
           }
       });
   });
});

// application process - confirm / reject / cancel/ withdraw class
$(function(){
    $(".confirm-application").click(function(){
        var application_id = $(this).data("id");

        $('#applicationModal').modal();
        $('#applicationModal').find('p').html('<span>Are you sure that you want to confirm course application?</span>');
        $('#applicationModal').one('click', '#btnYes', function(e){
            $.ajax({
                url: '/ajax/application',
                type: 'get',
                dataType: 'json',
                data: {"application_id": application_id, "status": "confirm"},

                success: function(data){
                    $('#applicationModal').modal('hide');
                    $('.icon[for="'+application_id+'"]').html("<i class='fa fa-check-circle'></i>");
                },
                error: function(data){
                    console.log("fail")
                }
            })
        });
    });

    $(".reject-application").click(function(){
        var application_id = $(this).data("id");

        $('#applicationModal').modal();
        $('#applicationModal').find('p').html('<span>Are you sure that you want to reject course application?</span>');
        $('#applicationModal').one('click', '#btnYes', function(e){
           $.ajax({
                url: '/ajax/application',
                type: 'get',
                dataType: 'json',
                data: {"application_id": application_id, "status": "reject"},

                success: function(data){
                    $('#applicationModal').modal('hide');
                    $('.icon[for="'+application_id+'"]').html("<i class='fa fa-times-circle'></i>");
                },
                error: function(data){
                    console.log("fail")
                }
            });
        });

    });

    $(".cancel-application").click(function(){
        var application_id = $(this).data("id");
        console.log("cancel-application:" + application_id);

        $('#applicationModal').modal();
        $('#applicationModal').find('p').html('<span>Are you sure that you want to cancel course application?</span>');
        $('#applicationModal').one('click', '#btnYes', function(e){
            $.ajax({
                url: '/ajax/application',
                type: 'get',
                dataType: 'json',
                data: {"application_id": application_id, "status": "cancel"},

                success: function(data){
                    $('#applicationModal').modal('hide');
                    $('.icon[for="'+application_id+'"]').html("<i class='fa fa-times-circle'></i>");
                },
                error: function(data){
                    console.log("fail");
                }
            });
        });
    });
});

//withdraw from course
$(function(){
    $(".withdraw-course").click(function(){
        var course_id = $(this).data("id");
        var course_name = $(this).data("course-name");

        $('#withdrawModal').modal();
        $('#withdrawModal').find('p').html('<span>Are you sure that you want to withdraw from ' + course_name + '?</span>');
        $('#withdrawModal').one('click', '#btnYes', function(e){
            $.ajax({
               url: '/ajax/withdraw_course',
               type: 'get',
               dataType: 'json',
               data:{"course_id": course_id},

               success: function(data){
                   console.log("course_id: " + data.course_id + " user_id: " + data.user_id + " student_id: " + data.student_id);
                   $('#withdrawModal').modal('hide');
                   $('.icon[for="'+course_id+'"]').html("<i class='fa fa-minus-circle'></i>");
               },
               error: function(data){
                   console.log("withdraw fail");
               }
           });
        });
   });
});

$(function(){
    $("#id_start_time_0_month,#id_start_time_0_day,#id_start_time_0_year,#id_start_time_1," +
    "#id_end_time_0_month,#id_end_time_0_day,#id_end_time_0_year,#id_end_time_1,#id_start_time_delta,#id_end_time_delta," +
    "#id_day_month,#id_day_day,#id_day_year,#id_until_month,#id_until_day,#id_until_year," +
    "#id_count,#id_interval,#id_month_ordinal,#id_month_ordinal_day,#id_year_month_ordinal,#id_year_month_ordinal_day").addClass("form-control");
});

//recommend course
$(function(){
    $(".recommendation-btn").click(function(){
        var course_id = $(this).data("id");
        var student_id = $(this).data("student-id");
        var status = $(this).attr("data-status");
        var a = '{{ course.recommendation.count|safe }}'

        console.log("status: " + status +" course-id:" + course_id);
        if (status == 'like'){
            $.ajax({
                url: '/ajax/recommend_course',
                type: 'get',
                dataType: 'json',
                data:{'course_id': course_id, 'student_id': student_id, 'status': "like"},

                success: function(data){
                    console.log(data.message);
                    if (data.message == 'success'){
                        $('.recommendation-btn[for="' + course_id + '"]').attr('data-status', 'dislike')
                        $('.recommendation-btn[for="' + course_id + '"]').html('<i class="fa fa-thumbs-up text-primary"></i><span>'+ data.count +'</span>');
                    }
                }
            });
        }
        else{
            $.ajax({
                url: '/ajax/recommend_course',
                type: 'get',
                dataType: 'json',
                data:{'course_id': course_id, 'student_id': student_id, 'status': "dislike"},

                success: function(data){
                    if(data.message == 'success'){
                        $('.recommendation-btn[for="' + course_id + '"]').attr('data-status', 'like')
                        $('.recommendation-btn[for="' + course_id + '"]').html('<i class="fa fa-thumbs-o-up text-primary"></i><span>'+ data.count +'</span>');
                    }
                }

            });
        }
    });
});

$(function(){
    $("#lightgallery").lightGallery();
});
$(function(){
    $('ul[class="errorlist"]').addClass('err_color');
});