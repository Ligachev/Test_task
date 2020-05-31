function fibonacci() {
    const old_div = document.getElementById('message');

    if (old_div){
        old_div.remove()
    }

    const count = document.getElementById('count').value;
    const sum_val = document.querySelectorAll('[name="choice"]');
    let sequence;

    if (count < 1 || count > 33) {
        alert('You have entered incorrect value!');
    } else {
        sequence = fib_seq(count);
    }

    const sum_seq = choice_value(sequence, sum_val)
    let sum_result = sum_seq.reduce((prev, cur) => prev + cur)

    let div = document.createElement('div');
    div.id = 'message'
    div.innerHTML = `Your\'s the Fibonacci sequence will be:<strong> ${sequence}</strong><br>
                    Sum of the even-valued terms is:<strong> ${sum_result}</strong>`;

    document.body.append(div);
    document.getElementById('count').value = '';
}


function choice_value(sequence, sum_val) {
    let res_seq;
    const value = Array.from(sum_val).find(node => node.checked).value;

    switch (value) {
        case 'even':
            res_seq = sequence.filter(item => item % 2 === 0);
            break;
        case 'odd':
            res_seq = sequence.filter(item => item % 2 !== 0);
            break;
        default:
            res_seq = [...sequence];
    }

    return res_seq;
}


function fib_seq (count) {

    let num_one = 1, num_two = 1;
    const sequence  = [];

    if (Number(count) === 1) {
        sequence.push(num_one);
    } else {
        sequence.push(num_one, num_two);
    }

    let i = 0;
    while (i < count - 2) {
        let num_three = num_one + num_two;
        sequence.push(num_three);
        num_one = num_two;
        num_two = num_three;
        i += 1;
    }

    return sequence
}