let up = document.getElementById('up');
let down = document.getElementById('down');
let left = document.getElementById('left');
let right = document.getElementById('right');
let shift = document.getElementById('shift');
let ctrl = document.getElementById('ctrl');
let throttle = document.getElementById('throttle');

let up_pressed = [false];
let down_pressed = [false];
let left_pressed = [false];
let right_pressed = [false];
let shift_pressed = [false];
let ctrl_pressed = [false];


up.addEventListener('mousedown', () =>update_clicks(up_pressed), {capture: true});
up.addEventListener('mouseup', () =>update_clicks(up_pressed), {capture: true});
up.addEventListener('mouseout', () => check_update(up_pressed), {capture: true});
up.addEventListener('touchstart', () =>update_clicks(up_pressed), );
up.addEventListener('touchend', () =>update_clicks(up_pressed), );
up.addEventListener('click', dummy, {capture: true});

down.addEventListener('mousedown', () =>update_clicks(down_pressed), {capture: true});
down.addEventListener('mouseup', () =>update_clicks(down_pressed), {capture: true});
down.addEventListener('mouseout', () => check_update(down_pressed), {capture: true});
down.addEventListener('touchstart', () =>update_clicks(down_pressed), {capture: true});
down.addEventListener('touchend', () =>update_clicks(down_pressed), {capture: true});
down.addEventListener('click', dummy, {capture: true});

left.addEventListener('mousedown', () =>update_clicks(left_pressed), {capture: true});
left.addEventListener('mouseup', () =>update_clicks(left_pressed), {capture: true});
left.addEventListener('mouseout', () => check_update(left_pressed), {capture: true});
left.addEventListener('touchstart', () =>update_clicks(left_pressed), {capture: true});
left.addEventListener('touchend', () =>update_clicks(left_pressed), {capture: true});
left.addEventListener('click', dummy, {capture: true});

right.addEventListener('mousedown', () =>update_clicks(right_pressed), {capture: true});
right.addEventListener('mouseup', () =>update_clicks(right_pressed), {capture: true});
right.addEventListener('mouseout', () => check_update(right_pressed), {capture: true});
right.addEventListener('touchstart', () =>update_clicks(right_pressed), {capture: true});
right.addEventListener('touchend', () =>update_clicks(right_pressed), {capture: true});
right.addEventListener('click', dummy, {capture: true});

shift.addEventListener('mousedown', () =>update_clicks(shift_pressed), {capture: true});
shift.addEventListener('mouseup', () =>update_clicks(shift_pressed), {capture: true});
shift.addEventListener('mouseout', () => check_update(shift_pressed), {capture: true});
shift.addEventListener('touchstart', () =>update_clicks(shift_pressed), {capture: true});
shift.addEventListener('touchend', () =>update_clicks(shift_pressed), {capture: true});
shift.addEventListener('click', dummy, {capture: true});

ctrl.addEventListener('mousedown', () =>update_clicks(ctrl_pressed), {capture: true});
ctrl.addEventListener('mouseup', () =>update_clicks(ctrl_pressed), {capture: true});
ctrl.addEventListener('mouseout', () => check_update(ctrl_pressed), {capture: true});
ctrl.addEventListener('touchstart', () =>update_clicks(ctrl_pressed), {capture: true});
ctrl.addEventListener('touchend', () =>update_clicks(ctrl_pressed), {capture: true});
ctrl.addEventListener('click', dummy, {capture: true});



document.addEventListener('keydown', () => keyboard_toggle(true));
document.addEventListener('keyup', () => keyboard_toggle(false));

function keyboard_toggle(value) {
    if (event.keyCode === 87 && up_pressed[0] !== value) {
        up_pressed[0] = value;
        update();
    } else if (event.keyCode === 83 && down_pressed[0] !== value) {
        down_pressed[0] = value;
        update();
    } else if (event.keyCode === 68 && right_pressed[0] !== value) {
        right_pressed[0] = value;
        update();
    } else if (event.keyCode === 65 && left_pressed[0] !== value) {
        left_pressed[0] = value;
        update();
    } else if (event.keyCode === 17 && shift_pressed[0] !== value) {
        shift_pressed[0] = value;
        update();
    } else if (event.keyCode === 16 && ctrl_pressed[0] !== value) {
        ctrl_pressed[0] = value;
        update();
    }
}


function update() {
    event.stopPropagation();
    event.preventDefault();

    let xhr = new XMLHttpRequest();
    xhr.timeout = 10000;
    xhr.onload = function () {
        if (xhr.status !== 200) {
            alert('Server error ' + xhr.status);
        } else {
            console.log(xhr.responseText);
            throttle.innerHTML = xhr.responseText
        }
    };
    xhr.onerror = function () {
        alert('Connection is disrupted!');
    };

    xhr.open('POST', '/command/', true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({'up': up_pressed[0], 'down': down_pressed[0],
        'left': left_pressed[0], 'right':right_pressed[0],
        'shift': shift_pressed[0], 'ctrl': ctrl_pressed[0]}));
}

function update_clicks(button) {
    button[0] = !button[0];
    update()
}

function check_update(button) {
    if (button[0] === true) {
        update_clicks(button)
    }
}


function dummy() {
    event.stopPropagation();
    event.preventDefault();
}