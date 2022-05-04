function isNumber(n) { return !isNaN(parseInt(n)) && !isNaN(n - 0) }

var interval = '';


function Timer(time) {
    var hr = localStorage.getItem("hr");
    var mm = localStorage.getItem("mm");
    var ss = localStorage.getItem("ss");
    if (!hr || !mm || !ss) {
        hr = Math.floor(time / 3600);
        mm = Math.floor(time % 3600 / 60);
        ss = (time % 60);
        localStorage.setItem("hr", hr);
        localStorage.setItem("mm", mm);
        localStorage.setItem("ss", ss);
        localStorage.setItem("answers", ["", "", "", "", "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]);
    }
    interval = setInterval(function() {
        ss--;
        if (ss <= 0) {
            if (hr <= 0 && mm <= 0) {
                localStorage.setItem("hr", 0);
                localStorage.setItem("mm", 0);
                localStorage.setItem("ss", 0);
                window.location.href = document.getElementById('finishExam').href;
            } else {
                ss = 59;
                mm--;
                if (mm == 0) {
                   mm = 59;
                   hr--;
                }
            }
        }
        if (hr.toString().length < 2) {
            hr = "0" + hr;
        }
        if (mm.toString().length < 2) {
            mm = "0" + mm;
        }
        $(".time").html('<span class="hours">' + hr + '</span>:<span class="minutes">' + mm + '</span>');
        localStorage.setItem("hr", hr);
        localStorage.setItem("mm", mm);
        localStorage.setItem("ss", ss);}, 1000)
}


function changeActiveElementNext() {
    var slidesCount = document.getElementsByClassName("ind").length;
    var element = document.querySelectorAll("ul > li.active")[0];
    if (Number(element.querySelector("button").innerHTML) + 1!=slidesCount) {
        var element_next = element.nextElementSibling;
        element.classList.remove("active");
        element_next.classList.add("active");
    } else {
        var element_next = document.querySelectorAll("ul > li.ind")[0];
        element.classList.remove("active");
        element_next.classList.add("active");
    }
}


function changeActiveElementPrevious() {
    var slidesCount = document.getElementsByClassName("ind").length;
    var elements = document.querySelectorAll("ul > li.ind");
    var element = document.querySelector("ul > li.active");
    var first_element = elements[0];
    if (element === first_element) {
        var element_prev = elements[slidesCount - 1];
        element.classList.remove("active");
        element_prev.classList.add("active");
    } else {
        var element_prev = element.previousElementSibling;
        element.classList.remove("active");
        element_prev.classList.add("active");
    }
}


let save_answer = (number) => {
    if (number == 25) {
        var answers25 = document.getElementsByName("input_25");
        var answer = ``;
        for (let i = 0; i < answers25.length; i+=2) {
            if (answers25[i].value && answers25[i+1].value) {
                answer += `${answers25[i].value} ${answers25[i+1].value}<br/>`;
            } else if (answers25[i].value) {
                answer += `${answers25[i].value}<br/>`;
            }
        }
        answer = answer.slice(0, -5);
    }
    else {
        var answer = document.getElementsByClassName('answer me-2')[number-1].value;
    }
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
    input.value = num;
}


function showAlert() {
    if (confirm("Вы уверены, что хотите завершить экзамен?")) {
        localStorage.setItem("hr", 0);
        localStorage.setItem("mm", 0);
        localStorage.setItem("ss", 0);
        clearInterval(interval);
        window.location.href = document.getElementById('finishExam').href
    }
    return false
}

let showAnswer = (id) => {
    var answer = document.getElementById(`ans_${id}`);
    var text = document.getElementById(`p${id}`)
    if (answer.style.display == "none") {
        answer.style.display = "block";
        text.textContent = "Скрыть ответ"
    } else {
        answer.style.display = "none";
        text.textContent = "Показать ответ"
    }

}


function getAllTasks() {
    window.location.href = '/task_database/?number=' + document.getElementById("egeId").value;
    return false;
  }


function getTask() {
    window.location.href = '/task_database/?id=' + document.getElementById("task_id").value;
    return false;
  }
