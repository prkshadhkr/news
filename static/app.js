// side navbar scripts:
const mySliedbar = document.getElementById("mySidebar")
const main = document.getElementById("main")



function openNav() {
    mySliedbar.style.width = "250px";
    main.style.marginLeft = "250px";
}

function closeNav() {
    mySliedbar.style.width = "0";
    main.style.marginLeft = "0";
}


// popover

// $(function() {
//     $('#login').popover({

//         placement: 'bottom',
//         title: 'Popover Form',
//         html: true,
//         content: $('#myForm').html()
//     }).on('click', function() {
//         // had to put it within the on click action so it grabs the correct info on submit
//         $('.btn-primary').click(function() {
//             $('#result').after("form submitted by " + $('#email').val())
//             $.post('/echo/html/', {
//                 email: $('#email').val(),
//                 name: $('#name').val(),
//                 gender: $('#gender').val()
//             }, function(r) {
//                 $('#pops').popover('hide')
//                 $('#result').html('resonse from server could be here')
//             })
//         })
//     })
// })


$(document).ready(function() {
    $('[data-toggle="popover"]').popover({
        html: true,
        content: function() {
            return $('#popover-content').html();
        }
    });
});



// const testBtn = document.getElementById('testBtn');

// testBtn.addEventListener("click", function(e) {
//     var data = e.target.previousElementSibling;

//     console.log('testing', data)
// })