let intervalId;
let intervalTime = 10;

const setTimer = (time) => {
    if (intervalId) {
        clearInterval(intervalId);
    }

    intervalId = setInterval(() => {
        let items = document.querySelectorAll('.css-rp1nxq');
        let btn = document.querySelector('.css-zqm9nz');
        let textContents = Array.from(items).map(item => item.innerText);
        let time = parseInt(textContents.join(''));

        console.log(time);

        if (time >= 3000) {
            intervalTime = 5000;
            setTimer(intervalTime);
        } else if (time >= 1500) {
            intervalTime = 1000;
            setTimer(intervalTime);
        } else {
            intervalTime = 10;
            setTimer(intervalTime);
        }
        

        if (time <= 70) {
            btn.click();
            console.log('Button clicked');
        }
    }, time);
}

setTimer(intervalTime);
