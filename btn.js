let intervalId;
let intervalTime = 10;
let min = Number.POSITIVE_INFINITY;
let items = document.querySelectorAll('.css-rp1nxq');
let btn = document.querySelector('.css-zqm9nz');
let count = 0

const intervalFunc = () => {
    
    let textContents = Array.from(items).map(item => item.innerText);
    let time = parseInt(textContents.join(''));
    
    
    if (time < min) min = time;

    if (!isNaN(time)) {
        console.log(time);
        console.log("lowest time = " + min);
    }

    if (time >= 4000) {
        intervalTime = 3000;
    } else if (time >= 1000) {
        intervalTime = 1000;
    }else if (time >= 500) {
        intervalTime = 100;
    } else {
        intervalTime = 10;
    }

    if (time <= 100) {
        // setTimeout(() => {
        //     btn.click();
        //     console.log('Button clicked');
        // }, Math.random() * 50);
        if (count < 2){
            btn.click();
            console.log('Button clicked');
            count +=1;    
        }
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
