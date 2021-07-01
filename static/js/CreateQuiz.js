let app = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data: {
        name : "",
        category : "",
        // csrf : "{{ csrf_token }}"
    },
    // methods : {
    //     createQuiz(){
    //         axios({
    //             method: "POST",
    //             url: "/create-quiz/",
    //             headers: {
    //                 "Content-Type": 'application/json'
    //             },
    //             data: {'user_name': this.user_name ,'category_id' : this.category }
    //         }).then(function (response) {
    //             console.log(response.data);
    //             window.location.href = `/create-question/${response.data.data.quiz_id}/?category=${response.data.data.category}`
    //         })
    //     }
    // }
});