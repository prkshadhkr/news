const REQ_URL = `https://${location.host}`;


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
    $(document).on('click', '.submit-feed', async function(e) {

        e.preventDefault();
        let sourceId = $('.feed-form').find('#source_id').val();
        let feedId = $('.feed-form').find('#feed_id').val();


        await axios.post(`${REQ_URL}/sources`, {
                source_id: sourceId,
                feed_id: feedId
            })
            .then(function(response) {
                location.reload();
            })
            .catch(function(error) {
                console.log(error);
            });
    });

});


/*************************** Boards ****************************/

/** post request from categories **/
$(document).ready(function() {

    $(document).on('click', '.submit-board-categories', async function(e) {

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

        await axios.post(`${REQ_URL}/categories`, {
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
                location.reload();
            })
            .catch(function(error) {
                console.log(error);
            });
    });
});


/** post request from specific feed **/
$(document).ready(function() {

    $(document).on('click', '.submit-board-feeds', async function(e) {

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
        let feedId = $('.board-form').find('#feed_id').val(); // for specific feed

        await axios.post(`${REQ_URL}/feeds/${feedId}`, {
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
                location.reload();
            })
            .catch(function(error) {
                console.log(error);
            });
    });
});


/** post request from headlines **/
$(document).ready(function() {
    $(document).on('click', '.submit-board-headlines', async function(e) {

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

        await axios.post(`${REQ_URL}/headlines`, {
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
                location.reload();
            })
            .catch(function(error) {
                console.log(error);
            });
    });
});


/** post request from search  **/
$(document).ready(function() {
    $(document).on('click', '.submit-board-search', async function(e) {

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

        await axios.post(`${REQ_URL}/search`, {
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
                location.reload();
            })
            .catch(function(error) {
                console.log(error);
            });
    });
});


/************ articles read  *************/

$('.submit-read').click(readArticle)
async function readArticle(e) {
    e.preventDefault()
    let id = $(this).data('id');
    let currentURL = $(location).attr('href');
    console.log('id :', id)

    await axios.patch(`${currentURL}`, {
            id: id
        })
        .then(function(response) {
            location.reload()
            console.log(response);
        })
        .catch(function(error) {
            console.log(error);
        });

}

$('.submit-delete').click(deleteArticle)
async function deleteArticle() {

    let id = $(this).data('id');
    let currentURL = $(location).attr('href');

    await axios.post(`${currentURL}`, {
            id: id
        })
        .then(function(response) {
            console.log(response);
        })
        .catch(function(error) {
            console.log(error);
        });

    // $(this).parent().parent().parent().remove()
    $(this).parents().eq(3).remove()

}