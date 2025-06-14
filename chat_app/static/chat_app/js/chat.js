// Отримуємо pk поточної групи через прихованний input
const groupPk = document.getElementById("groupPk").value
// Підклюємо web-сокет по диномічній url-адреси з pk групи
const webSocket = new WebSocket(`ws://${window.location.host}/chat/${groupPk}`)
// Отримуємо дані від методу send від серверу (Отримуємо повідомлення від серверу)
webSocket.onmessage = function(event){
    // Парсимо дані, які були відправлені з серверу
    let data = JSON.parse(event.data)
    // Перевіряємо тип даних
    if (data.type === 'chat' ){
        // Отримуємо повідомлення
        let messages = document.getElementById('messages')
        // Отримуємо дату та час повідомлення
        let dateTime = new Date(data.date_time)
        // Конвертуємо дату та час до локального часового поясу
        dateTime = dateTime.toLocaleString()
        // Відображаємо повідомлення на сторінці
        messages.insertAdjacentHTML(
            'beforeend',
            `<div><p><b>${data.username}(Онлайн): </b>${data.message} (${dateTime})</p><i>Переглядів: ${data.views}</i></div>`
        )
    }
}
// Реалізуємо відправку повідомлення від клієнта до серверу
let messageForm = document.querySelector('#message')
// Створюємо функцію, яка відпрацьовує, якщо форма з повідомленням буде відправлятися
messageForm.addEventListener(
    type = 'submit',
    (event) =>{
        // Виключаємо стандартну "поведінку" (Відправку форми на бекенд)
        event.preventDefault();
        // Отримуємо з форми повідомлення
        let data_message = event.target.message.value;
        // Відправляємо по веб-сокету наше повідомлення
        webSocket.send(JSON.stringify({
            'message': data_message
        }));
    }
)
// Отримуємо час та дату з історії всіх повідомленнь
let isoDateTimeArray = document.querySelectorAll(".iso-date-time")
// Робимо для кожної дати та часу повідомлення функцію конвертації до локального часового поясу
isoDateTimeArray.forEach(dateElem =>{
    // Перетворюємо стандартний час у об'єкт Date
    let newDate = new Date(dateElem.textContent)
    // Конвертуємо до локального часового поясу
    let dateToLocal = newDate.toLocaleString()
    // Замінюємо час на конвертованний (локальний)
    dateElem.textContent = dateToLocal
})