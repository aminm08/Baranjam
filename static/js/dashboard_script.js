var start_inp = document.getElementById("id_start");
var end_inp = document.getElementById("id_end");
var general_date_inp = document.getElementById("id_general_date");
var measure_header = document.getElementById("measure-header");
var job_progress = document.getElementById("job-progress");
var bar_job = document.getElementById("bar-job");
var hour_progress = document.getElementById("hour-progress");
var bar_hour = document.getElementById("bar-hour");


let clearInputs = function () {
    start_inp.value = end_inp.value = general_date_inp.value = "";
}


class Goal {
    constructor(goals) {
        this.goals = goals;
        this.dropdown_id = null;
    }

    setId(id) {
        this.dropdown_id = id;
        this.insert_data();

    }

    getGoalDataById() {
        let data = Object
        if (this.dropdown_id != null && this.goals[this.dropdown_id]) {
            data = this.goals[this.dropdown_id];
        } else {

            data = this.goals[Object.keys(this.goals)[0]];
        }
        return data
    }


    insert_data() {
        let data = this.getGoalDataById();
        measure_header.innerText = data[0];

        job_progress.innerText = `${data[1]}%`;
        bar_job.style.width = `${data[1]}%`;
        bar_job.ariaValueNow = data[1];

        hour_progress.innerText = `${data[2]}%`;
        bar_hour.style.width = `${data[2]}%`;
        bar_hour.ariaValueNow = data[2];



    }


}
