const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value


const SendSearchData = async (series, group_id) => {

    $.ajax({
        'type': 'POST',
        'url': `/group_lists/search_view/${group_id}/`,
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
                            <div class="row align-items-center">
                                <div class="col-1">
                                <input type="checkbox" class="form-check text-center ml-2 pl-2"
                                 name="${series.pk}">
                                </div>
                                <div class="col-2 mt-1 ml-1">
                                    <img src="${series.image}" class="image-circle">
                                </div>
                                <div class="col  mt-1">
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