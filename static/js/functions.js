function isNumber(n) { return !isNaN(parseInt(n)) && !isNaN(n - 0) }

function contador() {
    var hr = localStorage.getItem("hr");
    var mm = localStorage.getItem("mm");
    var ss = localStorage.getItem("ss");
    if (!hr || !mm || !ss) {
        hr = "3";
        mm = "54";
        ss = "59";
        localStorage.setItem("hr", hr);
        localStorage.setItem("mm", mm);
        localStorage.setItem("ss", ss);
    }
    var interval = setInterval(function () {
        if (hr == 0 && mm == 0 && ss == 0) {
            clearInterval(interval);

        }
        ss--;
        if (ss == 0) {
            ss = 59;
            mm--;
            if (mm == 0) {
                mm = 59;
                hr--;
            }
            if (hr == 0) {
                hr = 24;
            }
        }
        if (hr.toString().length < 2) hr = "0" + hr;
        if (mm.toString().length < 2) mm = "0" + mm;
        if (ss.toString().length < 2) ss = "0" + ss;
        $(".time").html('<span class="hours">' + hr + '</span>:<span class="minutes">' + mm + '</span>');
        localStorage.setItem("hr", hr);
        localStorage.setItem("mm", mm);
        localStorage.setItem("ss", ss);}, 1000);
}
window.onload = contador;


let save_answer = (number) => {
    var answer = document.getElementsByClassName('answer me-2')[number-1].value;
    var answers = localStorage.getItem('answers');
    if (!answers) {
        answers = ["", "", "", "", "", "", "", "", "", "", "", "", 
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""];
    } else {
        answers = answers.split(",")
    }
    answers[number-1] = answer;
    localStorage.setItem("answers", answers);
}

let select_all = (deselect = false) => {
    var checkboxes = document.getElementsByName("task_checkbox");
    var inputs = document.getElementsByName("task_input");
    if (deselect) {
        checkboxes.forEach(cb => cb.checked = false);
        inputs.forEach(inp => inp.value = "0");
    } else {
        checkboxes.forEach(cb => cb.checked = true);
        inputs.forEach(inp => inp.value = "1");
    }
}

let select_task = (id) => {
    var checkbox = document.getElementById(`cbx_${id}`);
    var input = document.getElementById(`inp_${id}`);
    checkbox.checked ? input.value = "1" : input.value = "0";
}

let onInputChange = (id) => {
    var input = document.getElementById(`inp_${id}`);
    var checkbox = document.getElementById(`cbx_${id}`);
    if (!isNumber(input.value)) {
        input.value = input.value.slice(0, -1);
    } 
    num = parseInt(input.value);
    if (num <= 0) {
        num = "0";
        checkbox.checked = false;
    } else {checkbox.checked = true;}
    if (!num) {checkbox.checked = false; num = "0"}
    if (num > 20) {
        num = "20";
    }
    input.value = num;
}