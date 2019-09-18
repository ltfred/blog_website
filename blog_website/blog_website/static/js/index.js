var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {


        notice_list: [], // 公告数据,


    },


    mounted(){
        // 获取购物车数据
        this.get_notices();


    },
    methods: {
        // 获取购物车数据
        get_notices(){
            var url = '/notice/';
            axios.get(url, {
                    responseType: 'json',
                })
                .then(response => {
                    this.notice_list = response.data.notice_list;

                })
                .catch(error => {
                    console.log(error.response);
                })
        },

    }
});