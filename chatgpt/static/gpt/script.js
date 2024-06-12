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
            texts = data['data'].replace(/(?:\r\n|\r|\n)/g, '<br>')
            let chat = $("<div>").addClass("chat_question")
            seq = $("<div>").addClass("question").html(texts);
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
    }

    var is_valid = 1

    if (is_valid == 1) {
        // 버튼 클릭 시
        $("#text-button").click(function(event){
            
            is_valid = 0;
            event.stopPropagation();
            const now = formatDate(new Date());

            let query = {type : 'query', data : $("#question").val()}; // textarea에 입력된 데이터 가져오기
            console.log(query)
            
            addDiv(query);
            
            $("#text-button").prop("disabled", true);

            $.ajax({
                url: "",
                type: "POST",
                contentType: "application/json; charset=utf-8",
                
                data: JSON.stringify({question: query.data, time: now}),
                beforeSend: (xhr) => xhr.setRequestHeader("X-CSRFToken", csrfToken), // CSRF 토큰을 헤더에 포함
                success: (data) => {
                    addDiv(data)
                    $("#text-button").prop("disabled", false);
                    is_valid = 1;
                    },
                error: (error) => console.error("Failed to send POST request:", error)
            });
                    
            $("#question").text('');
        });
    }

    // 엔터 키 입력 시
    $("#question").on('keydown', function(event){
        if (event.shiftKey) {
                if(event.keyCode == 13) {
                    
            }
        } else if (event.keyCode == 13 && is_valid == 1) {
            $("#text-button").click();
        }
    });
});