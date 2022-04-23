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