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