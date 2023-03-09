const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const result_box = document.getElementById('result_box');

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
                            <div id="result-container" >
                                <div class="justify-content-start align-self-center">
                                    <input type="checkbox" class="form-check text-center mx-2 pl-2"
                                     name="${series.pk}">
                                </div>
                                <div class="justify-content-center " id="search-result-img">
                                    <img src="${series.image}" class="circular--landscape">
                                </div>
                                <div class=" p-3">
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