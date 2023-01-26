const update_name_form = document.getElementById('update_name_form');
const title = document.getElementById('setting_title');
const button_edit = document.getElementById('edit_button');
const button_update= document.getElementById('update_button');

const form = document.getElementById('search_form');
const search_input = document.getElementById('search_input');
const result_box = document.getElementById('result_box');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value







const SendSearchData = async (series) => {

     $.ajax({
        'type': 'POST',
        'url': '/group_lists/search_view/',
        'data': {
            'csrfmiddlewaretoken': csrf,
            'series': series,
        },
        success: (res) => {
            const data = res.data;

            if (Array.isArray(data)) {
                result_box.innerHTML = '';

                data.forEach(series => {
                    result_box.innerHTML += `
                            <div class="row justify-content-start">
                                <div class="col-2 mt-1 ml-1">
                                    <img src="${series.image}" class="image-circle">
                                </div>
                                <div class="col-9  mt-1">
                                    <p class=fw-bold>${series.username}</p>
                                </div>
                            </div>
                            `
                });
            } else {

                if (search_input.value.lenght > 0) {
                    result_box.innerHTML = `<b>${data}</b>`

                } else {

                    result_box.classList.add('not-visible');
                }
            }
        },

        error: (err) => {
            console.log(err);
        }


    })

}


let setupForUpdate = function () {
    title.setAttribute('style', 'display:none;');
    update_name_form.removeAttribute('style');
}
let backToNormal = function () {
    title.style.removeProperty();
    update_name_form.setAttribute('style', 'display:none;');

}

// edit list name
button_edit.addEventListener('click', setupForUpdate);
button_update.addEventListener('click', backToNormal)




search_input.addEventListener('keyup', e => {


    if (result_box.classList.contains('not-visible')) {
        result_box.classList.remove('not-visible');
    }
    SendSearchData(e.target.value);
})

