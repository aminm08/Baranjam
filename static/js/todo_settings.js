const update_name_form = document.getElementById('update_name_form');
const title = document.getElementById('setting_title');
const button_edit = document.getElementById('edit_button');
const button_update = document.getElementById('update_button');

const form = document.getElementById('search_form');
const search_input = document.getElementById('search_input');

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value


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




