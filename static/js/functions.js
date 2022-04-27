function isNumber(n) { return !isNaN(parseInt(n)) && !isNaN(n - 0) }

var interval = ''

function contador(time) {
    var hr = localStorage.getItem("hr");
    var mm = localStorage.getItem("mm");
    var ss = localStorage.getItem("ss");
    if (!hr || !mm || !ss) {
        hr = Math.floor(time / 3600).toString();
        mm = Math.floor(time / 60).toString();
        ss = (time % 60).toString();
        localStorage.setItem("hr", hr);
        localStorage.setItem("mm", mm);
        localStorage.setItem("ss", ss);
        localStorage.setItem("answers", ["", "", "", "", "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]);
    }
    interval = setInterval(function() {
        ss--;
        if (ss == 0) {
            if (hr <= 0 && mm <= 0) {
               clearInterval(interval);
               window.location.href = document.getElementById('finishExam').href
            } else {
                ss = 59;
                mm--;
                if (mm == 0) {
                   mm = 59;
                   hr--;
                }
            }
        }
        if (ss <= 0) {
            clearInterval(interval);
            window.location.href = document.getElementById('finishExam').href
        }

        if (hr.toString().length < 2) {
            hr = "0" + hr;
        }
        if (mm.toString().length < 2) {
            mm = "0" + mm;
        }
        if (ss.toString().length < 2) {
            ss = "0" + ss;
        }
        $(".time").html('<span class="hours">' + hr + '</span>:<span class="minutes">' + mm + '</span>');
        localStorage.setItem("hr", hr);
        localStorage.setItem("mm", mm);
        localStorage.setItem("ss", ss);}, 1000)
}

function changeActiveElementNext() {
    var element = document.querySelectorAll('ul > li.active');
    var element_next = element.nextSibling;
}


let save_answer = (number) => {
    var answer = document.getElementsByClassName('answer me-2')[number-1].value;
    var answers = localStorage.getItem('answers');
    answers = answers.split(",")
    answers[number-1] = answer;
    console.log(answers)
    localStorage.setItem("answers", answers);
}

let add_number = (number, index) => {
    var numbers = localStorage.getItem("numbers");
    if (!numbers) {
        numbers = ["", "", "", "", "", "", "", "", "", "", "", "", 
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""];
    } else {
        numbers = numbers.split(",")
    }
    numbers[index] = number
    localStorage.setItem("numbers", numbers);
}

let make_table = (right_answers) => {
    var table = document.getElementsByClassName("user_results")[0];
    var answers = localStorage.getItem('answers');
    answers = answers.split(",");
    for (let i = 0; i < rows; i++) {
        var color = "";
        if (answers[i]) {
            if (answers[i] == right_answers[i]) {
                color = "#00FF7F";
            } else {
                color = "#FF4940";
            };
        } else {
            color = "#282828";
        }
        table.insertAdjacentHTML("beforeend", 
        `<td style="text-align: center; font-weight: bold;">${i + 1}</th>
        <td style="text-align: center; font-weight: bold;">${right_answers[i]}</th>
        <td style="text-align: center; font-weight: bold; background-color: ${color}">${answers[i]}</th>`);
    }
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


function showAlert() {
    if (confirm("Вы уверены, что хотите завершить экзамен?")) {
        clearInterval(interval);
        localStorage.setItem("hr", 0);
        localStorage.setItem("mm", 0);
        localStorage.setItem("ss", 0);
        window.location.href = document.getElementById('finishExam').href
    }
    return false
}
