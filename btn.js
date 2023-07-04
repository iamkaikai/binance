let intervalId;
let intervalTime = 10;
let min = Number.POSITIVE_INFINITY;

const intervalFunc = () => {
    let items = document.querySelectorAll('.css-rp1nxq');
    let btn = document.querySelector('.css-zqm9nz');
    let textContents = Array.from(items).map(item => item.innerText);
    let time = parseInt(textContents.join(''));
    let login = localStorage.getItem('login');
    
    if (time < min) min = time;

    if (!isNaN(time)) {
        console.log(time);
        console.log("lowest time = " + min);
        console.log("login = " + login);
    }

    if (time >= 3000) {
        intervalTime = 5000;
    } else if (time >= 1000) {
        intervalTime = 1000;
    } else {
        intervalTime = 10;
    }

    if (time <= 100) {
        // Add some random delay up to 50 milliseconds before clicking the button
        // let delay = Math.random() * 50;
        // setTimeout(() => {
        //     btn.click();
        //     console.log('Button clicked');
        // }, delay);
        btn.click();
        console.log('Button clicked');
    }

    resetTimer(intervalTime);
};

const setTimer = (time) => {
    intervalId = setInterval(intervalFunc, time);
};

const resetTimer = (time) => {
    clearInterval(intervalId);
    setTimer(time);
};

setTimer(intervalTime);
