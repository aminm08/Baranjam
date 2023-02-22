var start_inp = document.getElementById("id_start");
var end_inp = document.getElementById("id_end");
var general_date_inp = document.getElementById("id_general_date");


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
    }

    getGoalDataById() {
        if (this.dropdown_id) {
            let data = this.goals[this.dropdown_id];
        } else {
            let data = this.goals[Object.keys(this.goals)[0]];
        }
        return data
    }

    getDataGoalByMode(mode) {
        let data = this.getGoalDataById();
        let output_data = null;

        if (mode === 'measure') {
            output_data = data[0];
        } else if (mode === 'jobs') {
            output_data = data[1];
        } else {
            output_data = data[2];
        }
        
        return output_data
    }


}

let getGoalsData = function (goals, mode) {
    console.log(goals);


}