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

        // feedId- is used to get article from specific feed
        let feedId = $('.board-form').find('#feed_id').val();

        console.log('*****************', REQ_URL)

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

// $(document).ready(function() {
//     $(document).on('click', '.submit-board', function(e) {

//         e.preventDefault();
//         let url = $('.board-form').find('#url').val();
//         let sourceId = $('.board-form').find('#source_id').val();
//         let author = $('.board-form').find('#author').val();
//         let title = $('.board-form').find('#title').val();
//         let description = $('.board-form').find('#description').val();
//         let imgURL = $('.board-form').find('#img_url').val();
//         let publishedAt = $('.board-form').find('#published_at').val();
//         let content = $('.board-form').find('#content').val();

//         let boardId = $('.board-form').find('#board_id').val();

//         // feedId- is used to get article from specific feed
//         let feedId = $('.board-form').find('#feed_id').val();

//         let currentURL = $(location).attr('href');
//         // console.log('current url is :', currentURL)
//         if (currentURL.indexOf(`${REQ_URL}/categories`) > -1) {
//             makeRequest(`${REQ_URL}/categories`);
//         }

//         if (currentURL.indexOf(`${REQ_URL}/headlines`) > -1) {
//             makeRequest(`${REQ_URL}/headlines`);
//         }

//         if (currentURL.indexOf(`${REQ_URL}/search`) > -1) {
//             makeRequest(`${REQ_URL}/search`);
//         }

//         if (currentURL.indexOf(`${REQ_URL}/feeds/${feedId}`) > -1) {
//             makeRequest(`${REQ_URL}/feeds/${feedId}`);
//         }

//         async function makeRequest(urlRoute) {
//             await axios.post(urlRoute, {
//                     url: url,
//                     source_id: sourceId,
//                     author: author,
//                     title: title,
//                     description: description,
//                     img_url: imgURL,
//                     published_at: publishedAt,
//                     content: content,
//                     board_id: boardId
//                 })
//                 .then(function(response) {

//                     location.reload();

//                     console.log(response);
//                 })
//                 .catch(function(error) {
//                     console.log(error);
//                 });
//         }

//     });
// });



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