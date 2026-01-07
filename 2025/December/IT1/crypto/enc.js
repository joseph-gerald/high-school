
export function performXor(text, key) {
    let result = "";

    key = parseInt(key);

    for (let i = 0; i < text.length; i++) {
        console.log(text.charCodeAt(i), key, text.charCodeAt(i) + key)
        const newCharCode = text.charCodeAt(i) + key;
        result += String.fromCharCode(newCharCode);
    }

    return result;
}