REQ_URL = "http://127.0.0.1:5000"

//*************** side navbar scripts: *****************//
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


//******************** popover ***********************//

$(function() {
    $('[data-toggle="popover"]').popover({
        html: true,
        sanitize: false,
    })
})


//// for auto close the popover if clicked outside the content
$(document).on('click', function(e) {
    $('[data-toggle="popover"],[data-original-title]').each(function() {
        //the 'is' for buttons that trigger popups
        //the 'has' for icons within a button that triggers a popup
        if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
            (($(this).popover('hide').data('bs.popover') || {}).inState || {}).click = false // fix for BS 3.3.6
        }

    });
});


/*************************** Feeds ****************************/

$(document).ready(function() {
    $(document).on('click', '.submit-feed', function(e) {

        e.preventDefault();
        let sourceId = $('.feed-form').find('#source_id').val();
        let feedId = $('.feed-form').find('#feed_id').val();

        axios.post(`${REQ_URL}/sources`, {
                source_id: sourceId,
                feed_id: feedId
            })
            .then(function(response) {
                console.log(response);
            })
            .catch(function(error) {
                console.log(error);
            });
    });

});


/*************************** Boards ****************************/

$(document).ready(function() {
    $(document).on('click', '.submit-board', async function(e) {

        e.preventDefault();
        let url = $('.board-form').find('#url').val();
        let sourceId = $('.board-form').find('#source_id').val();
        let author = $('.board-form').find('#author').val();
        let title = $('.board-form').find('#title').val();
        let description = $('.board-form').find('#description').val();
        let imgURL = $('.board-form').find('#img_url').val();
        let publishedAt = $('.board-form').find('#published_at').val();
        let content = $('.board-form').find('#content').val();

        let boardId = $('.board-form').find('#board_id').val();
        let currentURL = $(location).attr('href');

        await axios.post(`${currentURL}`, {
                url: url,
                source_id: sourceId,
                author: author,
                title: title,
                description: description,
                img_url: imgURL,
                published_at: publishedAt,
                content: content,
                board_id: boardId
            })
            .then(function(response) {
                console.log(response);
            })
            .catch(function(error) {
                console.log(error);
            });
    });

});


/************ articles read  *************/

$('.submit-read').click(readArticle)
$('.submit-delete').click(deleteArticle)


async function readArticle() {

    let id = $(this).data('id');
    // let title = $(this).siblings('#title').val();
    let currentURL = $(location).attr('href');

    await axios.patch(`${currentURL}`, {
            id: id
        })
        .then(function(response) {
            console.log(response);
        })
        .catch(function(error) {
            console.log(error);
        });

}


async function deleteArticle() {

    let id = $(this).data('id');
    // let title = $(this).siblings('#title').val();
    let currentURL = $(location).attr('href');

    await axios.delete(`${currentURL}`, {
            id: id
        })
        .then(function(response) {
            console.log(response);
        })
        .catch(function(error) {
            console.log(error);
        });
}