$(document).ready(function(){

    const csrfToken = $('input[name="csrfmiddlewaretoken"]').attr('value');
    console.log(csrfToken)

    const formatDate = function(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); // 월은 0부터 시작하므로 1을 더해줌
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
    
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
    
    // 새로운 div를 추가하는 함수
    const addDiv = function(data) {
        let seq = ""

        if (data['type'] === 'query') {
            let chat = $("<div>").addClass("chat_question")
            seq = $("<div>").addClass("question").text(data['data']);
            chat.append(seq)
            $("#main").append(chat);
        } else {
            let chat = $("<div>").addClass("chat_answer")
            icon = $("<img>").addClass("chat_answer_icon").attr("src", "../../static/assets/chat.jpg");
            chat.append(icon)

            seq = $("<div>").addClass("answer").text(data['result']);
            chat.append(seq)

            $("#main").append(chat);
        }

        adjustTextareaHeight(); // 새로운 div가 추가될 때마다 textarea의 높이를 조절
    }

    // 버튼 클릭 시
    $("#text-button").click(function(event){
        const now = formatDate(new Date());

        let query = {type : 'query', data : $("#question").val()}; // textarea에 입력된 데이터 가져오기
        console.log(query)
        $("#question").val('');

        addDiv(query);

        $.ajax({
            url: "",
            type: "POST",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({question: query.data, time: now}),
            beforeSend: (xhr) => xhr.setRequestHeader("X-CSRFToken", csrfToken), // CSRF 토큰을 헤더에 포함
            success: (data) => addDiv(data),
            error: (error) => console.error("Failed to send POST request:", error)
        });
    });

    // 엔터 키 입력 시
    $("#question").keypress(function(event){
        if(event.keyCode == 13) $("#text-button").click();
    });


    // 입력창의 내용이 변경될 때마다 높이를 조정하는 함수
    function adjustTextareaHeight() {
        var textarea = document.getElementById('question');
        var div = document.getElementById('question-wrapper');

        var newHeight = textarea.scrollHeight; // 입력된 내용의 높이를 가져옴
        div.style.height = newHeight + 'px'; // 높이를 설정
        console.log(div.style.height);
    }

    // 페이지가 로드될 때와 입력창의 내용이 변경될 때마다 함수를 호출하여 높이를 조정
    // window.onload = function() {
    //     adjustTextareaHeight(); // 페이지 로드될 때 호출
    //     document.getElementById('question').addEventListener('input', adjustTextareaHeight); // 입력창 내용이 변경될 때마다 호출
    // };
    $(window).on("load", function() {
        adjustTextareaHeight(); // 페이지 로드될 때 호출
        // 입력창의 내용이 변경될 때마다 textarea의 높이를 조정
        $("#question").on("input", adjustTextareaHeight);
    });
    // // 입력창의 내용이 변경될 때마다 textarea의 높이를 조정
    // $("#question").on("input", adjustTextareaHeight);
});