function new_dict() {
    const old_div = document.getElementById('message');

    if (old_div){
        old_div.remove()
    }

    let keys = without_spaces(document.getElementById('keys').value);
    let values = without_spaces(document.getElementById('values').value);

    if (keys.length > values.length) {
        while (keys.length !== values.length) {
            values.push(null)
        }
    }

    const result = keys.reduce((keys, k, v) => (keys[k] = values[v], keys), {})

    let div = document.createElement('div');
    div.id = 'message'
    div.innerHTML = JSON.stringify(result);

    document.body.append(div);
    document.getElementById('keys').value = '';
    document.getElementById('values').value = '';
}


function without_spaces(arg) {
    const new_arr = arg.match(/\w+/gi)

    return new_arr
}