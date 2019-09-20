var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {

        notice_list: [], // 公告数据,
        top_list: [],  // 点击排行
        recommend_list: [],  // 推荐
        cat_list: []

    },

    mounted(){

        this.get_notices();
        this.get_top();
        this.get_recommend();
        this.get_cat();

    },
    methods: {
        get_notices(){
            var url = '/notices/';
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

        get_top(){
            var url = '/top/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response =>{
                    this.top_list = response.data.top_list;
                })
                .catch(error =>{
                    console.log(error.response)
                })
        },
        get_recommend(){
            var url = '/recommend/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response =>{
                    this.recommend_list = response.data.recommend_list;
                })
                .catch(error =>{
                    console.log(error.response)
                })
        },
        get_cat(){
            var url = '/category/';
            axios.get(url, {
                responseType: 'json',
            })
                .then(response =>{
                    this.cat_list = response.data.cat_list;
                })
                .catch(error =>{
                    console.log(error.response)
                })
        }

    }
});